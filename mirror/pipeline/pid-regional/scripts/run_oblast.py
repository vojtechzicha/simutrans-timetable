"""Rebuild one oblast's schedule from its hand design and check it: python run_oblast.py <oblast id> [--draft] [--no-audit] [--final]
(--final: the cross-oblast pass with every sibling sheet's coverage; only when no designer is running)

1. 00_config.py <id>: oblasti/<id>/lines.json + shared settings -> oblasti/<id>/config.json
2. 03_read.py <id>: the whole-day reading, reading/<L>.txt
3. --draft: odis-regional-hko/scripts/03b_draft.py (a first guess for lines not yet in lines.json; prints, writes draft.json)
4. odis-regional-hko/scripts/05_schedule.py: the Simutrans lines, their slots, running times, knot checks, needs and the
   coverage check (Step 9) -> data/derived/schedule.json
5. audits (written to oblasti/<id>/data/derived/audit-*.txt and printed in short): audit/step4_regional.py (Step 4: window
   slots vs real departures), audit/branch_check.py (legs read at a midpoint), audit/path_check.py (each slot's trip
   against the modelled stops). Every flag must be fixed in lines.json or explained on the card / in the method check.
"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); HOME = os.path.dirname(HERE); PIPE = os.path.dirname(HOME)
oid = sys.argv[1]; rel = f'pid-regional/oblasti/{oid}'; der = os.path.join(HOME, 'oblasti', oid, 'data', 'derived')
ODIS = os.path.join(PIPE, 'odis-regional-hko', 'scripts')
def run(args, cwd, out=None, env=None):
    r = subprocess.run([sys.executable, '-X', 'utf8'] + args, cwd=cwd, capture_output=bool(out), text=True, encoding='utf-8',
                       env=dict(os.environ, **(env or {})))
    if out:
        open(os.path.join(der, out), 'w', encoding='utf-8').write(r.stdout + r.stderr)
    if r.returncode: print(r.stdout[-3000:] if out else '', r.stderr[-3000:] if out else ''); sys.exit(f'{args[0]} failed')
    return r
run(['00_config.py', oid] + (['--final'] if '--final' in sys.argv else []), HERE); run(['03_read.py', oid], HERE)
if '--draft' in sys.argv: run(['03b_draft.py', '--base', rel], ODIS)
run(['05_schedule.py', '--base', rel], ODIS, out='schedule-log.txt')
log = open(os.path.join(der, 'schedule-log.txt'), encoding='utf-8').read()
print('\n'.join(l for l in log.splitlines() if not l.startswith('coverage:')))
# coverage split by okres (the full list is in the log): this oblast's own stops must all be covered here or explained;
# stops of other okresy are checked across all sheets at the end
import json
S = json.load(open(os.path.join(der, 'schedule.json'), encoding='utf-8')); cov = S.pop('_coverage')
SO = json.load(open(os.path.join(HOME, 'data', 'derived', 'stop_okres.json'), encoding='utf-8'))
pre = json.load(open(os.path.join(HOME, 'oblasti', oid, 'config.json'), encoding='utf-8'))['prefix']
# owner, 2 Nov 2026: "serve every place": stops of this okres and stops outside the Středočeský kraj are this sheet's to
# cover now; stops of another Středočeský okres are covered by that oblast's sheet (checked in the --final pass)
own = {s: v for s, v in cov['uncovered'].items() if SO.get(s) == pre}
# a Prague stop that no city line serves in the afternoon is the regional sheet's to cover too
out_ = {s: v for s, v in cov['uncovered'].items() if SO.get(s) is None}
oth = {s: v for s, v in cov['uncovered'].items() if s not in own and s not in out_}
print(f"\ncoverage: {cov['served']} afternoon stops, {cov['here']} on this sheet, {len(cov['elsewhere'])} on other sheets; uncovered: "
      f"{len(own)} of this okres, {len(out_)} outside the kraj or in Prague with no city line, {len(oth)} of other okresy")
for s, v in list(own.items()) + list(out_.items()):
    print(f"  {'explained' if v['why'] else 'UNCOVERED here'}{(' (Prague, no city line)' if s.startswith('Praha, ') else ' (outside the kraj)') if s in out_ else ''}: {s} ({', '.join(v['lines'])})" + (f" - {v['why']}" if v['why'] else ''))
if oth: print('  uncovered, another Středočeský okres (its sheet covers it; checked in the --final pass): ' + '; '.join(f"{s} ({', '.join(v['lines'])})" for s, v in oth.items()))
# every slot must stand for a real trip: a leg whose window holds no slot passes Step 4 without checking anything
hm = lambda t: '%d:%02d' % (t // 60 % 24, t % 60)
for L, x in S.items():
    for s in x['sim']:
        P = s['every']
        for g in s['legs']:
            if g['untimed']: continue
            ds = [t['d'] for t in g.get('trips', [])]
            for r in g['real']:
                near = min(ds, key=lambda d: min((d - r) % P, (r - d) % P), default=None)
                dev = min((near - r) % P, (r - near) % P) if near is not None else None
                if dev is None or dev > 3:
                    print(f"  SLOT WITHOUT A REAL TRIP: {L} {s['name']} {g['fr']} -> {g['to']}: slot {hm(r)} (every {P}); nearest real trip "
                          + (f"{hm(near)}, {dev} min off" if near is not None else 'none'))
            if not g['window']['slots']:
                print(f"  no slot in the window: {L} {s['name']} {g['fr']} -> {g['to']}: slots {', '.join(hm(r) for r in g['real'])} stand for "
                      + ', '.join(hm(min(ds, key=lambda d: min((d - r) % P, (r - d) % P))) for r in g['real'] if ds) + ' (name the real trip in the line\'s why)')
if '--no-audit' not in sys.argv:
    run([os.path.join(PIPE, 'audit', 'step4_regional.py'), rel, '--md', os.path.join(der, 'audit-step4.md')], PIPE, out='audit-step4.txt')
    run([os.path.join(PIPE, 'audit', 'branch_check.py'), PIPE], PIPE, out='audit-branch.txt', env={'AUDIT_SHEETS': rel})
    run([os.path.join(PIPE, 'audit', 'path_check.py'), PIPE], PIPE, out='audit-path.txt', env={'AUDIT_SHEETS': rel})
    for f in ('audit-step4.txt', 'audit-branch.txt', 'audit-path.txt'):
        t = open(os.path.join(der, f), encoding='utf-8').read()
        print(f'--- {f}:', '\n'.join(l for l in t.splitlines() if l.strip())[:2500])
    print(f'full audits: {der}\\audit-step4.md, audit-branch.txt, audit-path.txt')
