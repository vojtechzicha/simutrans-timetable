"""Change state: carry the base state's trams over to the new network -> data/derived/<state>/courses.json

Used instead of 04_courses.py when the state has a "changes" block (user, 13 Oct: "be smart with the changes,
I'll be redoing it in game, so reduce the workload"). The trams are the ones already in the game (the base
state's courses.json); nothing is re-rostered from new records. Only the state's lists change them:

  group_map   old line group -> new group (9 -> 9/10 circle, 10 -> 10/9 circle): same trams, new schedule
  moves       {from: old course, to: new course}: the tram changes Simutrans line
  withdraw    {from: old course, why}: the tram goes back to the depot (uncertain = 'withdrawn', not counted)
  cancelled   whole line groups that disappear; each of their trams must be in moves or withdraw

Each course gets change = None (stays), 'in' (moved here, with moved_from), or 'withdrawn'. The list
"leaving" holds every tram that leaves a group, so the old line's card can say where it went.

Usage: python 04b_rebase.py --state 2026-10-12
"""
import argparse, copy, os
from common import state, load, save, DER

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True)
    s = state(ap.parse_args().state); ch = s['changes']
    base = load(os.path.join(DER, ch['base'], 'courses.json'))
    CO = base['courses']; by_id = {c['id']: c for c in CO}
    gmap = ch.get('group_map', {})
    moves = {m['from']: m for m in ch.get('moves', [])}
    wd = {w['from']: w for w in ch.get('withdraw', [])}
    for k in list(moves) + list(wd):
        assert k in by_id, f'unknown course {k}'
        assert by_id[k]['uncertain'] not in ('spare', 'am'), f'{k} is not in the game (not needed / not counted)'
    cancelled = set(ch.get('cancelled', {}))
    for c in CO:     # every counted tram of a cancelled line must be placed
        if c['group'] in cancelled and c['uncertain'] not in ('spare', 'am'):
            assert c['id'] in moves or c['id'] in wd, f'{c["id"]} of cancelled line {c["group"]} has no move or withdrawal'

    out, leaving = [], []
    for c in CO:
        n = copy.deepcopy(c); n['change'] = None
        old_group = c['group']
        n['group'] = gmap.get(old_group, old_group)
        if c['id'] in moves:
            to = moves[c['id']]['to']; L, k = to.split('/')
            leaving.append(dict(id=c['id'], group=n['group'], to=to, set=c['final'], why=moves[c['id']].get('why', '')))
            # the new group: line L itself, or the pool recorded under L (10 -> the 10/9 circle)
            grp = next((g for g in s['line_order'] if g == L or s.get('pools', {}).get(g, {}).get('recorded_as') == L), L)
            n.update(id=to, line=L, course=int(k), pm_line=L, group=grp, change='in', moved_from=c['id'], transfer=None,
                     split=False, swap=False, uncertain='', chain=[c['final']], veh=[v for v in c['veh'] if v['set'] == c['final']],
                     note=moves[c['id']].get('why', ''))
        elif c['id'] in wd:
            leaving.append(dict(id=c['id'], group=n['group'], to=None, set=c['final'], why=wd[c['id']]['why']))
            n.update(change='withdrawn', uncertain='withdrawn', note=wd[c['id']]['why'])
        if n['group'] in cancelled and n['change'] is None:      # not needed / not counted cars of a cancelled line
            n['change'] = 'gone'
        out.append(n)
    ids = [c['id'] for c in out if c['change'] != 'withdrawn']
    dup = {i for i in ids if ids.count(i) > 1}
    assert not dup, f'course ids used twice: {dup}'
    save(dict(courses=out, shared_sets=base.get('shared_sets', {}), leaving=leaving, base=ch['base']),
         os.path.join(DER, s['name'], 'courses.json'))
    cnt = lambda g: sum(1 for c in out if c['group'] == g and c['uncertain'] not in ('spare', 'am', 'withdrawn') and c['change'] != 'gone')
    print('moves', len(moves), 'withdrawn', len(wd), '| counted per group:', {g: cnt(g) for g in s['line_order']})

if __name__ == '__main__':
    main()
