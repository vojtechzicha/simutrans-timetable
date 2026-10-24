"""Game lines (engine export) vs the current PID timetable -> data/derived/<state>/compare.json

Halt names. Game halts look like "Praha, Zličín [B] / Praha, AN Zličín",
"Praha-Holešovice (Ex5)[S4,R15] <090,091>/ Praha, Nádraží Holešovice [C] / Praha, AN Holešovice" or
"Jesenice, Budějovická". Every " / " part (and the text after a "<…>" rail code) is a candidate; each candidate
loses its "[stand]" suffix and a "Praha, " / "Praha. " prefix, and ", " becomes "," (PID writes "Jesenice,Budějovická").
A game halt is a PID stop of the line when a candidate is equal, or failing that when a candidate is a misspelling or
abbreviation of it (fuzzy: abbreviated tokens "nádr." as prefixes, else accent-free similarity >= 0.85), or listed in
the state's "halt_aliases". Fuzzy/alias matches count as the same stop and are reported as "name fixes".

Directions. A game schedule is one round trip. For every PID pattern p of direction 0 whose two termini are both on the
game line, the round trip is rotated to start at p's origin and split at p's destination: the first half is compared
with the best PID pattern of direction 0, the second half (plus the return to the start) with the best pattern of
direction 1. The split with the highest score wins. Circular lines (one direction) are compared as a whole.
Per half:
  missing  = stops of the PID pattern the game half does not serve,
  extra    = game stops of the half that the PID pattern does not serve,
  replaced = a missing and an extra stop between the same two common neighbours (a renamed, moved or substituted stop),
  order    = the common stops are not in the same order.
A line is "aligned" when both halves have no missing, extra or replaced stops and the order is right.

Usage: python 03_compare.py --state 2026-09-29
"""
import argparse, os, re, collections, unicodedata, difflib
from common import state, load, save, RAW, DER

def cands(name):
    out = []
    for part in re.split(r'/|<[^>]*>', name):
        p = re.sub(r'\([^)]*\)|\[[^\]]*\]', ' ', part).strip()
        p = re.sub(r'^Praha[,.]\s*', '', p)
        p = re.sub(r',\s+', ',', re.sub(r'\s+', ' ', p)).strip(' ,')
        if p and not p.startswith('Praha-'): out.append(p)
    return out

def fold(x):
    x = unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9. ]+', ' ', x).split()

def fuzzy(cand, names):
    best, bs = None, 0
    ct = fold(cand)
    for nm in names:
        nt = fold(nm)
        if len(ct) == len(nt) and all((a.endswith('.') and b.startswith(a[:-1])) or a == b for a, b in zip(ct, nt)):
            return nm
        r = difflib.SequenceMatcher(None, ' '.join(ct), ' '.join(nt)).ratio()
        if r > bs: best, bs = nm, r
    return best if bs >= 0.85 else None

def eq(g, x):
    return x in g            # g: frozenset of PID names a game halt may stand for

def show(g):
    return sorted(g)[0].lstrip('?')

def lcs_pairs(a, b):
    """Longest common subsequence of game stops a (sets) and PID stops b as index pairs."""
    n, m = len(a), len(b)
    T = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            T[i][j] = T[i + 1][j + 1] + 1 if eq(a[i], b[j]) else max(T[i + 1][j], T[i][j + 1])
    i = j = 0; out = []
    while i < n and j < m:
        if eq(a[i], b[j]): out.append((i, j)); i += 1; j += 1
        elif T[i + 1][j] >= T[i][j + 1]: i += 1
        else: j += 1
    return out

def collapse(seq):
    out = []
    for s in seq:
        if not out or out[-1] != s: out.append(s)
    while len(out) > 1 and out[0] == out[-1]: out.pop()
    return out

def compare_half(g, p):
    """g: game stops of one direction (in order), p: PID pattern stops. Returns dict of differences."""
    pairs = lcs_pairs(g, p)
    gi = {i for i, _ in pairs}; pj = {j for _, j in pairs}
    missing = [p[j] for j in range(len(p)) if j not in pj]
    extra = [show(g[i]) for i in range(len(g)) if i not in gi]
    # replaced in place: a gap on both sides between the same two matched neighbours
    replaced = []
    anchors = [(-1, -1)] + pairs + [(len(g), len(p))]
    for (i0, j0), (i1, j1) in zip(anchors, anchors[1:]):
        ge = [show(g[i]) for i in range(i0 + 1, i1)]; pe = [p[j] for j in range(j0 + 1, j1)]
        for a, b in zip(ge, pe): replaced.append([a, b])
    rep_g = {a for a, _ in replaced}; rep_p = {b for _, b in replaced}
    missing = [x for x in missing if x not in rep_p]; extra = [x for x in extra if x not in rep_g]
    ps = set(p)
    common_g = [x for x in g if x & ps]
    order_ok = len(pairs) >= len({show(x) for x in common_g})   # every PID stop the game serves is matched in order
    score = 2 * len(pairs) - len(missing) - len(extra) - len(replaced)
    return dict(missing=missing, extra=extra, replaced=replaced, order_ok=order_ok, score=score, game_stops=len(g), pid_stops=len(p))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True)
    s = state(ap.parse_args().state)
    G = load(os.path.join(RAW, 'game', s['game_raw'], 'lines.json'))
    P = load(os.path.join(DER, s['name'], 'gtfs_lines.json'))['lines']
    aliases = s.get('halt_aliases', {})
    res = []
    for gl in G['lines']:
        pid = str(gl['pid_number']) if gl.get('pid_number') is not None else gl['licence_number'][3:].lstrip('0')
        base = gl['name'].split(' ')[0] == gl['licence_number']
        halts = [e['halt_name'] for e in gl['entries'] if e.get('halt_name')]
        r = dict(line_id=gl['line_id'], name=gl['name'], pid=pid, variant=not base, convoys=gl['convoy_count'], vehicles=gl['vehicle_count'],
                 stop_entries=gl['stop_entry_count'], unique_halts=gl['unique_halt_count'], waypoints=gl['waypoint_count'],
                 wait_for_load=sum(1 for e in gl['entries'] if e.get('minimum_loading_pct')))
        p = P.get(pid)
        if not p or not p.get('patterns'):
            r.update(status='not in the current PID timetable' if not p else 'no PID trips on the service date', aligned=False); res.append(r); continue
        pats = p['patterns']
        pid_names = {re.sub(r',\s+', ',', x): x for pt in pats for x in pt['stops']}
        gseq, name_fix, unknown = [], {}, []
        stands = s.get('layover_stand_words', ['odstav'])
        for h in halts:
            if any(w in h.lower() for w in stands): continue          # layover stand, not a passenger stop
            c = [pid_names[x] for x in cands(h) if x in pid_names]
            if not c:
                al = [aliases[x] for x in cands(h) if x in aliases and aliases[x] in pid_names.values()]
                fz = [f for f in (fuzzy(x, list(pid_names)) for x in cands(h)) if f]
                c = al or [pid_names[f] for f in fz]
                if c: name_fix[h] = c[0]
            if c: gseq.append(frozenset(c))
            else:
                nm = (cands(h) or [h])[-1]; gseq.append(frozenset(['?' + nm])); unknown.append(h)
        gseq = collapse(gseq)
        d0 = [pt for pt in pats if pt['dir'] == '0'] or pats
        d1 = [pt for pt in pats if pt['dir'] == '1']
        best = None
        idx = lambda seq, name: next((i for i, x in enumerate(seq) if name in x), None)
        for po in d0:
            if po['o'] == po['d'] or idx(gseq, po['o']) is None or idx(gseq, po['d']) is None: continue
            k = idx(gseq, po['o']); rot = gseq[k:] + gseq[:k]
            sp = idx(rot, po['d'])
            out_g, ret_g = rot[:sp + 1], rot[sp:] + [rot[0]]
            # terminus hand-over: trips end at one stop and start from another (Letiště / Terminál 1)
            d1_origins = {x['o'] for x in d1}; d1_dests = {x['d'] for x in d1}
            if len(ret_g) > 2 and not (ret_g[0] & d1_origins) and (ret_g[1] & d1_origins): ret_g = ret_g[1:]
            if len(ret_g) > 2 and not (ret_g[-1] & d1_dests) and (ret_g[-2] & d1_dests): ret_g = ret_g[:-1]
            h0 = max((dict(compare_half(out_g, x['stops']), pattern=f"{x['o']} → {x['d']}", n=x['all_day']) for x in d0), key=lambda z: (z['score'], z['n']))
            h1 = max((dict(compare_half(ret_g, x['stops']), pattern=f"{x['o']} → {x['d']}", n=x['all_day']) for x in d1), key=lambda z: (z['score'], z['n'])) if d1 else None
            sc = h0['score'] + (h1['score'] if h1 else 0)
            if best is None or sc > best[0]: best = (sc, [h0] + ([h1] if h1 else []))
        if best is None:          # circular line, or the game line does not reach both PID termini
            def circ(x):
                g = gseq
                k = idx(g, x['o'])
                if k is not None:
                    g = g[k:] + g[:k]
                    if x['o'] == x['d']: g = g + [g[0]]          # a loop ends where it starts
                return dict(compare_half(g, x['stops']), pattern=f"{x['o']} → {x['d']}", n=x['all_day'])
            halves = [max((circ(x) for x in pats), key=lambda z: (z['score'], z['n']))]
            r['split'] = False
        else:
            halves = best[1]; r['split'] = True

        r['halves'] = halves
        r['name_fixes'] = name_fix; r['unknown_halts'] = unknown
        r['aligned'] = all(not h['missing'] and not h['extra'] and not h['replaced'] and h['order_ok'] for h in halves)
        r['status'] = 'aligned' if r['aligned'] else 'stops differ'
        r['pid_need'] = p.get('need'); r['pid_peak'] = p.get('peak')
        res.append(r)
    game_pids = {r['pid'] for r in res}
    absent = [dict(pid=L, long_name=v['long_name'], trips=v['trips'], peak=v.get('peak'), need=v.get('need'), route_type=v['route_type'],
                   operators=v['operators']) for L, v in P.items() if L not in game_pids]
    save(dict(lines=res, absent_in_game=absent, game_source=G['source']), os.path.join(DER, s['name'], 'compare.json'))
    c = collections.Counter(r['status'] for r in res)
    print(dict(c), '| zero vehicles:', [r['name'] for r in res if not r['convoys']], '| PID lines absent in game:', len(absent),
          '| name fixes:', sum(len(r.get('name_fixes', {})) for r in res))

if __name__ == '__main__':
    main()
