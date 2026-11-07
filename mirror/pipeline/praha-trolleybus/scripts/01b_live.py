"""Trolleybuses seen on the PID live map -> data/raw/live/<day>/trolleybus.json (an extract the sheet keeps as its own raw data)

The PID regional session polled mapa.pid.cz for the whole PID area every minute (pipeline/pid-regional/scripts/01_live_poll.py,
raw files pipeline/pid-regional/data/raw/live/<day>/polls.jsonl + vehicles.jsonl). From 3 Nov it also kept the trolleybuses.
seznam-autobusu.cz refuses every scripted request since 1 Nov 2026 (kb/sources.md), so this is the only vehicle record for
the lines that changed on 2 Nov. The map has no history: these files cannot be fetched again.

Per vehicle seen on a trolleybus route (route type 11) or on one of the state's live.lines:
  lines        {line: polls seen on it}             first / last   first and last poll seen (any line)
  peak_polls   polls seen 15:00-17:59 per line      peak_first / peak_last  within 15:00-17:59
  windows      the vehicle windows read that day: type, "Vůz, oběh" course (line/course), seznam-autobusu car id
The map drops vehicles for minutes at a time (51/509 is in 11 of the 180 polls 15:00-17:59 while running all peak), so
"not seen" is not "not running".

Usage: python 01b_live.py --state 2026-11-02
"""
import argparse, collections, json, os
from common import state, save, RAW, BASE

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True)
    s = state(ap.parse_args().state); lv = s['live']
    src = os.path.normpath(os.path.join(BASE, lv['source_dir']))
    want = set(lv.get('lines', []))
    for day in lv['days']:
        d = os.path.join(src, day)
        V = collections.defaultdict(lambda: dict(lines=collections.Counter(), peak_polls=collections.Counter(), first=None, last=None,
                                                 peak_first=None, peak_last=None, windows=[]))
        npoll = npeak = 0
        for line in open(os.path.join(d, 'polls.jsonl'), encoding='utf-8'):
            o = json.loads(line); t = o['t'][11:16]; npoll += 1; pk = '15:00' <= t < '18:00'; npeak += pk
            for b in o['buses']:
                rt = b[7] if len(b) > 7 else None
                if rt != 11 and b[1] not in want: continue
                v = V[str(b[0])]; v['lines'][b[1]] += 1
                v['first'] = v['first'] or t; v['last'] = t
                if pk:
                    v['peak_polls'][b[1]] += 1; v['peak_first'] = v['peak_first'] or t; v['peak_last'] = t
        seen = set()
        for line in open(os.path.join(d, 'vehicles.jsonl'), encoding='utf-8'):
            o = json.loads(line); k = str(o['vehicle'])
            if o.get('route_type') != 11 and o.get('seen_route') not in want: continue
            key = (k, o.get('course'), o.get('seen_route'))
            if key in seen: continue
            seen.add(key)
            V[k]['windows'].append(dict(at=o['at'][11:16], route=o.get('seen_route'), route_type=o.get('route_type'), type=o.get('type') or '',
                                        course=o.get('course'), operator=o.get('operator'), car_id=o.get('car_id')))
        out = dict(day=day, source=f'PID live map (mapa.pid.cz), polled by the PID regional session; raw: pipeline/pid-regional/data/raw/live/{day}/',
                   polls=npoll, peak_polls=npeak,
                   vehicles={k: dict(v, lines=dict(v['lines']), peak_polls=dict(v['peak_polls'])) for k, v in sorted(V.items(), key=lambda kv: int(kv[0]))})
        save(out, os.path.join(RAW, 'live', day, 'trolleybus.json'))
        print(day, npoll, 'polls,', len(V), 'vehicles')
        for k, v in out['vehicles'].items():
            print(' ', k.rjust(4), v['first'], v['last'], v['lines'], 'peak', v['peak_polls'], [(w['course'], w['type']) for w in v['windows']])

if __name__ == '__main__':
    main()
