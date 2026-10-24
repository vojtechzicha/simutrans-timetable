"""Fetch seznam-autobusu.cz deployment records (vypravenost/pid/vypis?datum=D&linka=L) into data/raw/vypravenost/<D>/<L>.html.
Lines: every PID line in the state's licence range (from gtfs_lines.json) for the vehicle date; for lines run by an operator
other than DPP also the state's extra days (for the pak: which cars and liveries really run the city lines); for a line
with fewer courses logged on the vehicle date than it needs at 16:00 also the extra days and its history since
history_since (vypis?linka=L&since=D -> history/<line>.html), so 04_courses.py can fill them in with real cars; plus the
day overview of the vehicle date (vypravenost/pid?datum=D -> <date>/overview.html) to check a designed car was free that day.
Usage: python 01_fetch_records.py --state 2026-09-29"""
import argparse, os, re
from common import state, load, fetch, parse_vypis, RAW, DER
ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True); s = state(ap.parse_args().state)
P = load(os.path.join(DER, s['name'], 'gtfs_lines.json'))['lines']
jobs = [(s['vehicle_date'], L) for L in P]
jobs += [(d, L) for d in s.get('extra_days_non_dpp', []) for L, v in P.items() if any(not o.startswith('Dopravní podnik') for o in v['operators'])]
def courses(d, L):
    p = os.path.join(RAW, 'vypravenost', d, f'{L}.html')
    return len({r['course'] for r in parse_vypis(p)}) if os.path.exists(p) else 0
def run(jobs):
    for d, L in jobs:
        dest = os.path.join(RAW, 'vypravenost', d, f'{L}.html')
        if os.path.exists(dest): continue
        try: fetch(f'https://seznam-autobusu.cz/vypravenost/pid/vypis?datum={d}&linka={L}', dest, pause=2.0)
        except Exception as e: print('fail', d, L, e)
run(jobs)
more = [(d, L) for L in P if courses(s['vehicle_date'], L) < (P[L].get('need') or 0) for d in s.get('extra_days_non_dpp', [])]
run(more)
# line history since history_since for lines still short of their need on the vehicle date (designed buses take real cars from it),
# and the day overview of the vehicle date (every PID vehicle out that day: a designed car must not be among them)
short = [L for L in P if courses(s['vehicle_date'], L) < (P[L].get('need') or 0)]
for L in short:
    dest = os.path.join(RAW, 'vypravenost', 'history', f'{L}.html')
    if not os.path.exists(dest):
        try: fetch(f'https://seznam-autobusu.cz/vypravenost/pid/vypis?linka={L}&since={s["history_since"]}', dest, pause=2.0)
        except Exception as e: print('fail history', L, e); continue
    m = re.search(r'celkem\s*(\d+)', open(dest, encoding='utf-8').read())
    for page in range(2, -(-int(m.group(1)) // 50) + 1 if m else 0):   # 50 records a page, ?strana=N
        d2 = os.path.join(RAW, 'vypravenost', 'history', f'{L}_p{page}.html')
        if not os.path.exists(d2):
            try: fetch(f'https://seznam-autobusu.cz/vypravenost/pid/vypis?strana={page}&linka={L}&since={s["history_since"]}', d2, pause=2.0)
            except Exception as e: print('fail history', L, page, e)
# lines with no record since history_since: the latest records from history_fallback_since, up to history_fallback_pages pages
for L in short:
    first = os.path.join(RAW, 'vypravenost', 'history', f'{L}.html')
    if not os.path.exists(first) or 'class="row' in open(first, encoding='utf-8').read(): continue
    for page in range(1, s.get('history_fallback_pages', 3) + 1):
        d2 = os.path.join(RAW, 'vypravenost', 'history', f'{L}_y.html' if page == 1 else f'{L}_y_p{page}.html')
        if not os.path.exists(d2):
            try: fetch(f'https://seznam-autobusu.cz/vypravenost/pid/vypis?strana={page}&linka={L}&since={s["history_fallback_since"]}', d2, pause=2.0)
            except Exception as e: print('fail history', L, page, e); break
        if 'strana=%d&' % (page + 1) not in open(d2, encoding='utf-8').read(): break
dest = os.path.join(RAW, 'vypravenost', s['vehicle_date'], 'overview.html')
if not os.path.exists(dest): fetch(f'https://seznam-autobusu.cz/vypravenost/pid?datum={s["vehicle_date"]}', dest, pause=2.0)
print('done', len(jobs) + len(more))
