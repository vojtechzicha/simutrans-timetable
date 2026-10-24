import os, sys
os.environ.setdefault('ODIS_BASE', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'odis-regional-hko', 'scripts'))
from lib import load, hm
S = load('schedule.json')
def short(s): return s.split(', ', 1)[-1][:22]
for L in sys.argv[1].split(','):
    x = S[L]; a = x['anchor']
    print(f"== {L} anchor {hm(a['anchor'])}" + (f" busiest {hm(a['busiest'][0])}-{hm(a['busiest'][1])}" if a.get('busiest') else ''))
    for s in x['sim']:
        print(f"  [{s['name']}] every {s['every']} need {s['need']} window {hm(s['window'][0])}-{hm(s['window'][1])} {s['how']} waits {s['waits']}")
        for g in s['legs']:
            if g['untimed']: print(f"    {short(g['fr'])} -> {short(g['to'])}: untimed, rt {g['rt']}"); continue
            P = g['every']; sl = sorted(g['real'])
            print(f"    {short(g['fr'])} -> {short(g['to'])}" + (f" (knot {short(g['knot']['stop'])} +{g['knot']['rt']})" if g.get('knot') else '') + f": slots {[hm(r) if P > 60 else ':%02d' % r for r in sl]} rt {g['rt']} lay {g['lay']} | exact {g['stat']['exact']} w3 {g['stat']['w3']} of {g['stat']['n']}")
            row = []
            for t in sorted(g['trips'], key=lambda t: t['d']):
                if not 300 <= t['d'] < 1380: continue
                m = '' if t['dev'] == 0 else ('~' if t['dev'] <= 3 else '!')
                row.append(f"{hm(t['d'])}{m}{t['dev'] if t['dev'] else ''}" + ('' if t['line'] == L else f"[{t['line']}]"))
            print('      ', ' '.join(row))
            print('       window slots:', ' '.join(hm(t) + ('(-)' if t in g['window']['empty'] else '') for t in g['window']['slots']), '| real in window:', ' '.join(hm(d) for d in g['window']['deps']))
