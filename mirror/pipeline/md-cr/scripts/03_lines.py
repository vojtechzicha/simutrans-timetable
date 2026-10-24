"""Assign each trip to a peak line and a variant (distinct Czech path), orient directions.

Line: the state line number carried by most of the trip's Czech stops (R<n> when the line's trains are
mostly R, Ex<n> otherwise). Trips without a line number are commercial and grouped by carrier and
corridor (config commercial_carrier_groups and corridors in lines.json overrides).
Variant: the unordered pair of Czech termini; directions are "out" from the line's A end.
Output: data/derived/lines.json
"""
import json, os, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(ROOT, 'config.json'), encoding='utf-8'))
HUBS = ['Praha', 'Brno', 'Ostrava', 'Plzeň', 'Olomouc', 'Liberec', 'Ústí n. L.', 'Hradec Král.', 'Pardubice',
        'České Budějovice', 'Kolín', 'Cheb', 'Břeclav', 'Bohumín']


def hubrank(name):
    for i, h in enumerate(HUBS):
        if name.startswith(h):
            return i
    return len(HUBS)


def commercial_line(t):
    ru = t['rus'][0][0]
    grp = CFG['commercial_carrier_groups'].get(ru, 'other')
    names = {s['name'] for s in t['stops']}
    if 'Brno hl. n.' in names or 'Břeclav' in names:
        corr = 'BRV'
    elif 'Olomouc hl. n.' in names or 'Ostrava-Svinov' in names or 'Bohumín' in names:
        corr = 'OVA'
    else:
        corr = t['stops'][0]['name'] + '|' + t['stops'][-1]['name']
    return grp + '-' + corr


def main():
    trips = json.load(open(os.path.join(ROOT, 'data', 'derived', 'trips.json'), encoding='utf-8'))
    ov = json.load(open(os.path.join(ROOT, 'overrides.json'), encoding='utf-8'))
    lines = collections.defaultdict(list)
    for t in trips:
        key = None
        for n in t['nums']:
            if n in ov.get('train_line', {}):
                key = ov['train_line'][n]
        if key is None:
            svc_stops = sum(c for _, c in t['svcs'])
            if t['svcs'] and svc_stops * 2 >= len(t['stops']) - 1:
                key = 'S' + t['svcs'][0][0]
            else:
                key = commercial_line(t)
        t['line'] = key
        lines[key].append(t)
    # Rychlík trains filed under an Expres line number (e.g. R Ostrava - Žilina under line 1) form their own line
    for key in list(lines):
        if not key.startswith('S'):
            continue
        ts = lines[key]
        r = [t for t in ts if t['cat'] == 'R']
        if r and len(r) < len(ts) and len(r) >= 4 and len(r) * 2 < len(ts) + len(r):
            lines[key] = [t for t in ts if t['cat'] != 'R']
            lines[key + '-R'] = r
            for t in r:
                t['line'] = key + '-R'
    out = []
    for key, ts in lines.items():
        cats = collections.Counter(t['cat'] for t in ts)
        if key.endswith('-R'):
            code = 'R' + key[1:-2] + '-R'
            kind = 'state'
        elif key.startswith('S'):
            n = key[1:]
            code = ('R' if cats.get('R', 0) * 2 > len(ts) else 'Ex') + n
            kind = 'state'
        else:
            code = key
            kind = 'commercial'
        # variants
        vs = collections.defaultdict(list)
        for t in ts:
            a, b = t['stops'][0]['name'], t['stops'][-1]['name']
            vs[tuple(sorted((a, b)))].append(t)
        main_v = max(vs, key=lambda k: len(vs[k]))
        A = min(main_v, key=hubrank) if hubrank(main_v[0]) != hubrank(main_v[1]) else main_v[0]
        A = ov.get('line_A', {}).get(code, A)
        variants = []
        for k, vt in vs.items():
            for t in vt:
                t['dir'] = 'out' if t['stops'][0]['name'] == A or (k[0] != A and k[1] != A and hubrank(t['stops'][0]['name']) <= hubrank(t['stops'][-1]['name'])) else 'back'
            ends = [t['stops'][0]['name'] for t in vt if t['dir'] == 'out'] + [t['stops'][-1]['name'] for t in vt if t['dir'] == 'back']
            a = collections.Counter(ends).most_common(1)[0][0]
            b = k[1] if a == k[0] else k[0]
            variants.append({'a': a, 'b': b, 'trips': sorted(vt, key=lambda t: t['stops'][0]['dep'])})
        variants.sort(key=lambda v: -len(v['trips']))
        out.append({'key': key, 'code': code, 'kind': kind, 'A': A, 'cats': cats.most_common(),
                    'rus': collections.Counter(r for t in ts for r, _ in t['rus'][:1]).most_common(),
                    'variants': variants})
    out.sort(key=lambda l: (l['kind'] != 'state', l['code'][:1] != 'E', int(''.join(c for c in l['code'] if c.isdigit()) or 0), l['code']))
    json.dump(out, open(os.path.join(ROOT, 'data', 'derived', 'lines.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    for l in out:
        print(l['code'], l['A'], dict(l['cats']), dict(l['rus']))
        for v in l['variants']:
            deps = ' '.join(f"{t['stops'][0]['dep']//60:02d}{t['stops'][0]['dep']%60:02d}{'>' if t['dir']=='out' else '<'}" for t in v['trips'])
            print(f"    {v['a']} - {v['b']} ({len(v['trips'])}): {deps}")


if __name__ == '__main__':
    main()
