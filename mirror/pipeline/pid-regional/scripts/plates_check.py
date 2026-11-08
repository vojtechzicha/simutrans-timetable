"""Plates check for the passing audit: python plates_check.py <oblast id> [YYYY-MM-DD ...]  ->  data/derived/audit-plates.txt
For every line flagged in the oblast's audit-passing.txt (run passing_check first), the trips it lists as off the pattern and
what their buses did next on the live map (every poll day, or the days given): ended the day (home), ran another line, or
came back on the same line, on a slot or off the pattern too. Counted per direction (→ / ← as in audit-passing.txt).
A card that calls the surplus "buses going home" (sleep, garage) must have the plates for it: CHECK where, in the direction
with most trips off the pattern, more buses came back on the line than went home or on. Every CHECK gets a verdict (the card
is right about other trips, or the card is corrected); buses that come back empty are peak extras, not buses going home. Off-pattern round
trips at a repeating minute are the 381 Zásmuky sign (3 Nov 2026: 9372 out 14:30 to Zásmuky, back 16:21); 402's Zruč trips
are the true case (7925, 7671, 7672 leave Zruč 4:24, 4:36, 6:29 and end their day there on the 15:20, 17:35, 18:20)."""
import collections, json, os, re, sys
from common import HOME
sys.stdout.reconfigure(encoding='utf-8')
O = sys.argv[1]
tm = lambda s: int(s.split(':')[0]) * 60 + int(s.split(':')[1]); hm = lambda t: '%d:%02d' % (t // 60 % 24, t % 60)
SH = json.load(open(os.path.join(HOME, 'config.json'), encoding='utf-8'))
LIVE = os.path.join(HOME, SH['live']['dir'])
import datetime   # working days only: the sheets are the working-day timetable
DAYS = sys.argv[2:] or sorted(d for d in os.listdir(LIVE) if os.path.exists(os.path.join(LIVE, d, 'polls.jsonl'))
                             and datetime.date.fromisoformat(d).weekday() < 5)
DER = os.path.join(HOME, 'oblasti', O, 'data', 'derived')
CARDS = json.load(open(os.path.join(HOME, 'oblasti', O, 'lines.json'), encoding='utf-8'))['lines']
CLAIM = re.compile(r'going home|sleep|garage', re.I)
TRIP = {}            # tid -> (oblast, line key, dep, fr, to), every oblast: a bus may run on into the next okres
for o in sorted(os.listdir(os.path.join(HOME, 'oblasti'))):
    p = os.path.join(HOME, 'oblasti', o, 'data', 'derived', 'trips.json')
    if not os.path.exists(p): continue
    for k, tr in json.load(open(p, encoding='utf-8')).items():
        for t in tr: TRIP[t['tid']] = (o, k, t['dep'], t['fr'], t['to'])
idx = collections.defaultdict(list)
for tid, (o, k, dep, fr, to) in TRIP.items():
    if o == O: idx[(k, dep % 1440, fr, to)].append(tid)
FLAG = []            # [kind, line, stop, [(arrow, dep, fr, to, tids)]]
hd = re.compile(r'^\[(EACH WAY|ONE WAY)\] (\S+) \((.*?)\): .* at (.*); off the pattern there:')
tr_re = re.compile(r'^\s+(→|←|·) (\d+:\d\d) (.*?) → (.*)$')
for ln in open(os.path.join(DER, 'audit-passing.txt'), encoding='utf-8'):
    m = hd.match(ln)
    if m: FLAG.append([m.group(1), m.group(2), m.group(4), []]); continue
    m = tr_re.match(ln)
    if m and FLAG:
        to = m.group(4).strip()
        FLAG[-1][3].append((m.group(1), m.group(2), m.group(3), to, idx.get((FLAG[-1][1], tm(m.group(2)), m.group(3), to), [])))
OFF = {tid for f in FLAG for x in f[3] for tid in x[4]}
out = [f'Plates check, {O}: live-map days {", ".join(DAYS)}. Per flagged line and direction: home = the trip was the bus\'s last of '
       'the day; on = it then ran another line; back = it came back on this line (on a slot / OFF the pattern too).']
checks = []
for day in DAYS:
    seen = {}
    for ln in open(os.path.join(LIVE, day, 'polls.jsonl'), encoding='utf-8'):
        r = json.loads(ln); t = tm(r['t'][11:16])
        for v, route, tid, stp, *_ in r['buses']:
            if stp in ('on_track', 'at_stop') and (v, tid) not in seen: seen[(v, tid)] = t
    seq = collections.defaultdict(list); by_tid = collections.defaultdict(list)
    for (v, tid), t in seen.items(): seq[v].append((t, tid)); by_tid[tid].append(v)
    for v in seq: seq[v].sort()
    out.append(f'\n======== {day}')
    for kind, line, stop, trips in FLAG:
        cnt = collections.defaultdict(collections.Counter); rows = []
        for arrow, dep, fr, to, tids in trips:
            vs = [(v, tid) for tid in tids for v in by_tid.get(tid, [])]
            if not vs: rows.append(f'      {arrow} {dep} {fr} → {to}: not seen'); cnt[arrow]['unseen'] += 1
            for v, tid in vs:
                s = seq[v]; i = [x[1] for x in s].index(tid); nxt = s[i + 1] if i + 1 < len(s) else None
                if nxt is None: what, c = 'last trip of the day', 'home'
                else:
                    nt = TRIP.get(nxt[1]); nl = nxt[1].split('_')[0]
                    if (nt and nt[1] == line) or nl == line:
                        c = 'back OFF' if nxt[1] in OFF else 'back on slot'
                        what = f'back on {line} {hm(nt[2])} {nt[3]} → {nt[4]}' if nt else f'back on {line} at {hm(nxt[0])}'
                        what += ' (off the pattern too)' if nxt[1] in OFF else ''
                    else:
                        c = 'on'; what = f'then {nl}' + (f' {hm(nt[2])} {nt[3]} → {nt[4]}' if nt else f' at {hm(nxt[0])}')
                rows.append(f'      {arrow} {dep} {fr} → {to}: {v}, {what}'); cnt[arrow][c] += 1
        main = max(cnt, key=lambda a: sum(cnt[a].values()), default=None)
        flag = ''
        note = re.sub(r'not (the )?buses going home', '', CARDS.get(line, {}).get('note', ''))   # "peak extras, not buses going home"
        if main and CLAIM.search(note):
            back = cnt[main]['back OFF'] + cnt[main]['back on slot']; gone = cnt[main]['home'] + cnt[main]['on']
            if back > gone:
                flag = f'  CHECK: the card says the buses go home / sleep out; {back} of {back + gone} came back on {line}'
                checks.append(f'{day} {line}: {back} of {back + gone} {main} came back')
        out.append(f'[{kind}] {line} at {stop}: ' + '; '.join(f'{a} ' + ', '.join(f'{k} {n}' for k, n in sorted(c.items()))
                                                          for a, c in sorted(cnt.items())) + flag)
        out += rows
out.insert(1, 'CHECK lines: ' + ('; '.join(checks) if checks else 'none'))
open(os.path.join(DER, 'audit-plates.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(out[1])
