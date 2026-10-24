"""compact review dump: per Simutrans line: every, slots, joint move, fit, afternoon real departures, need vs buses seen"""
import os, sys
os.environ.setdefault('ODIS_BASE', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'odis-regional-hko', 'scripts'))
from lib import load, hm
S = load('schedule.json'); R = load('roster.json')
want = sys.argv[1].split(',') if len(sys.argv) > 1 else [L for L in S if not L.startswith('_')]
def sh(s): return s.split(', ')[-1][:14]
for L in want:
    x = S[L]; ros = {r['name']: r for r in R['lines'].get(L, [])}
    print(f"== {L} {x['name'][:60]} | anchor {hm(x['anchor']['anchor'])}")
    for s in x['sim']:
        P = s['every']; r = ros.get(s['name'], {})
        print(f"  [{s['name']}] every {P} need {s['need']} seen {len(r.get('seen', []))} des {len(r.get('designed', []))} nn {len(r.get('not_needed', []))} win {hm(s['window'][0])}-{hm(s['window'][1])} waits {s['waits']}")
        for g in s['legs']:
            if g['untimed']: print(f"    {sh(g['fr'])}->{sh(g['to'])} untimed rt {g['rt']}"); continue
            sl = [hm(t) for t in range(720, 1170) if t % P in g['real']]
            j = f" JOINT moved {g['joint']['moved']} from {g['joint']['fit']}" if g.get('joint') else ''
            aft = ' '.join(hm(t['d']) + ('' if t['dev'] == 0 else f"/{t['dev']}") for t in sorted(g['trips'], key=lambda t: t['d']) if 720 <= t['d'] < 1170)
            print(f"    {sh(g['fr'])}->{sh(g['to'])} rt {g['rt']}{j} | slots 12-19: {' '.join(sl)}")
            print(f"       real 12-19: {aft}")
