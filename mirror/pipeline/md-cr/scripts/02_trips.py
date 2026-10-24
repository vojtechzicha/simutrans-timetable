"""Build the long-distance trips that run on the service day (config.json) from data/derived/trains.json.

A trip keeps its Czech passenger stops on the long-distance part of its run. A stop belongs to that part
when the train arrives or departs there as one of the included categories. The first foreign station on
either side and the header's foreign origin or destination are kept as text.
Output: data/derived/trips.json and data/derived/excluded.json.
"""
import json, os, datetime as D, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(ROOT, 'config.json'), encoding='utf-8'))
CAT = CFG['categories']
INC = set(CFG['included_categories'])
PAX = set(CFG['passenger_activities'])


def runs(t, day):
    i = (day - D.date.fromisoformat(t['start'])).days
    return 0 <= i < len(t['bitmap']) and t['bitmap'][i] == '1'


def build(t):
    L = t['locs']
    keep = []
    for i, l in enumerate(L):
        prev = L[i - 1]['ctt'] if i else None
        on_ld = l['ctt'] in INC or (prev in INC and 'dep' not in l) or (prev in INC and l['ctt'] is None)
        if not on_ld or not (set(l['act']) & PAX):
            continue
        keep.append((i, l))
    cz = [(i, l) for i, l in keep if l['cc'] == 'CZ']
    if len(cz) < 2:
        return None
    fi, li = cz[0][0], cz[-1][0]
    before = [l for i, l in keep if i < fi and l['cc'] != 'CZ']
    after = [l for i, l in keep if i > li and l['cc'] != 'CZ']
    stops = []
    for i, l in cz:
        stops.append({'name': l['name'], 'code': l['code'],
                      'arr': round(l['arr']) if 'arr' in l else None,
                      'dep': round(l['dep']) if 'dep' in l else None,
                      'req': '0030' in l['act'], 'svc': l['svc'], 'ru': l['ru'],
                      'cat': CAT.get(l['ctt']) if l['ctt'] in INC else None, 'num': l['num']})
    # the last stop's departure and the first stop's arrival are not part of the trip
    # a train that continues abroad keeps its real stay at the border-side station (engine or crew change)
    stops[0]['cont_arr'] = stops[0]['arr'] if before else None
    stops[-1]['cont_dep'] = stops[-1]['dep'] if after else None
    stops[0]['arr'] = None
    stops[-1]['dep'] = None
    if stops[0]['dep'] is None:
        stops[0]['dep'] = stops[0]['arr']
    passing = [l['code'] for l in L[fi:li + 1]]
    # stops without passengers where the train waits (crossing, engine or crew change): kept for the long-stop list
    pax_idx = {i for i, _ in cz}
    tech = []
    for i in range(fi + 1, li):
        l = L[i]
        if i in pax_idx or 'arr' not in l or 'dep' not in l or l['cc'] != 'CZ':
            continue
        if l['dep'] - l['arr'] >= 1:
            tech.append({'name': l['name'], 'arr': round(l['arr']), 'dep': round(l['dep']), 'act': l['act'], 'after': sum(1 for j in pax_idx if j < i)})
    cats = [s['cat'] for s in stops[:-1] if s['cat']]
    return {
        'file': t['file'], 'pa': t['ids'].get('PA'),
        'nums': sorted({s['num'] for s in stops}, key=lambda x: int(x) if x.isdigit() else 0),
        'cats': sorted(set(cats)), 'cat': collections.Counter(cats).most_common(1)[0][0],
        'rus': collections.Counter(s['ru'] for s in stops[:-1]).most_common(),
        'svcs': collections.Counter(s['svc'] for s in stops[:-1] if s['svc']).most_common(),
        'from_foreign': (before[0]['name'] if before else None),
        'to_foreign': (after[-1]['name'] if after else None),
        'origin': t['foreign'].get('CZForeignOriginLocation'),
        'destination': t['foreign'].get('CZForeignDestinationLocation'),
        'stops': stops, 'passing': passing, 'tech': tech,
    }


def main():
    day = D.date.fromisoformat(CFG['service_day'])
    T = json.load(open(os.path.join(ROOT, 'data', 'derived', 'trains.json'), encoding='utf-8'))
    trips, excluded = [], []
    for t in T:
        if not runs(t, day):
            continue
        ctts = {l['ctt'] for l in t['locs']}
        if not ctts & set(CAT):
            continue
        if not ctts & INC:
            l = next(l for l in t['locs'] if l['ctt'] in CAT)
            excluded.append({'num': l['num'], 'cat': CAT[l['ctt']], 'why': CFG['excluded_categories_note'][l['ctt']],
                             'from': t['locs'][0]['name'], 'to': t['locs'][-1]['name'],
                             'origin': t['foreign'].get('CZForeignOriginLocation'),
                             'destination': t['foreign'].get('CZForeignDestinationLocation')})
            continue
        r = build(t)
        if r is None:
            l = next(l for l in t['locs'] if l['ctt'] in INC)
            excluded.append({'num': l['num'], 'cat': CAT[l['ctt']],
                             'why': 'fewer than two Czech stops on the long-distance part',
                             'from': t['locs'][0]['name'], 'to': t['locs'][-1]['name'],
                             'origin': t['foreign'].get('CZForeignOriginLocation'),
                             'destination': t['foreign'].get('CZForeignDestinationLocation')})
            continue
        trips.append(r)
    trips.sort(key=lambda r: r['stops'][0]['dep'])
    out = os.path.join(ROOT, 'data', 'derived')
    json.dump(trips, open(os.path.join(out, 'trips.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    json.dump(excluded, open(os.path.join(out, 'excluded.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(trips), 'trips,', len(excluded), 'excluded')


if __name__ == '__main__':
    main()
