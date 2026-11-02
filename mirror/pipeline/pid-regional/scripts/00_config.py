"""Write oblasti/<id>/config.json (the ODIS regional config that odis-regional-hko/scripts reads with --base) from the
shared settings here and the oblast's hand design in oblasti/<id>/lines.json.

lines.json (edited by hand, the bus schedule method v4) holds: lines (config.lines of the ODIS scripts: core, note,
anchor, sim[] with legs), unmodelled {L: reason}, terminus_alias {stop: alias}, terminus_alias_why, coverage_exceptions
{stop: reason}, owner_checks [[L, what, slower option]], notes.
Set here, not by hand:
- unmodelled reasons for night lines, rail replacement buses (XS/XR), PID Haló on-demand lines and lines with no trips on the day.
  Bus replacement lines (X315, X384, X390, X391, X438) are designed like any line: they run for months (X390, the Slapy dam
  closure, 2 Mar 2026 - 31 Dec 2027; all five were in the 29 Sep and the 1 Nov feeds), and long works are modelled as they run;
- other_sheets: the Prague bus sheet (its regional companions placed in this oblast are modelled there; every Prague city
  line's afternoon stops count as covered), and every sibling oblast sheet that already has a schedule.json.
usage: python 00_config.py <oblast id> [...]   (all oblasts when none given)
"""
import json, os, sys, unicodedata
from common import HOME, DER, PIPE

CFG = json.load(open(os.path.join(HOME, 'config.json'), encoding='utf-8'))
OB = {o['id']: o for o in CFG['oblasti']}
state = json.load(open(os.path.join(PIPE, CFG['praha_bus']['state']), encoding='utf-8'))
reg = state.get('regional', {})
COMP = {}
for kind in ('through', 'pooled', 'interleaved'):
    for k, v in (reg.get(kind) or {}).items():
        for L in ([k] if kind == 'interleaved' else (v if isinstance(v, list) else list(v) if isinstance(v, dict) else [v])):
            COMP[str(L)] = kind
for L in CFG['praha_bus'].get('companions', []): COMP.setdefault(L, 'companion')

# every Prague city line's afternoon stops, as a schedule the coverage check reads (they are all on the Prague bus sheet)
city = json.load(open(os.path.join(DER, 'city_stops.json'), encoding='utf-8'))
cs = {L: dict(sim=[dict(name=L, legs=[dict(stops=st)])]) for L, st in city.items()}
# written once, atomically: designers run this for their oblasts in parallel, and 05_schedule reads the file
cp = os.path.join(DER, 'praha_city_schedule.json')
if not os.path.exists(cp) or json.load(open(cp, encoding='utf-8')) != cs:
    tmp = cp + f'.{os.getpid()}.tmp'; json.dump(cs, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False); os.replace(tmp, cp)
# --final: the cross-oblast pass, with every sibling sheet's schedule (run when no designer is running). Without it (the
# design phase) no sibling is read: a sibling's schedule.json may be half written by its own designer.
FINAL = '--final' in sys.argv
sys.argv = [a for a in sys.argv if a != '--final']

def auto_unmodelled(oid):
    out = {}
    C = json.load(open(os.path.join(HOME, 'oblasti', oid, 'data', 'derived', 'line_class.json'), encoding='utf-8'))
    for L, c in C.items():
        lab = c.get('label', L)
        if c.get('night'): out[L] = 'Night line: the sheets model the weekday afternoon (owner, 25 Sep 2026: no night lines).'
        elif lab.startswith(('XS', 'XR')):
            out[L] = 'Rail replacement bus (NAD) for engineering works on the railway: the rail sheets model the trains.'
        elif 'Haló' in c.get('name', ''): out[L] = 'PID Haló: an on-demand service with no fixed timetable.'
        elif c['cls'] == 'none': out[L] = 'No trips on the service day (Mon 2 Nov 2026, a school weekday).'
    return out

for oid in (sys.argv[1:] or list(OB)):
    o = OB[oid]; base = os.path.join(HOME, 'oblasti', oid)
    lp = os.path.join(base, 'lines.json')
    if not os.path.exists(lp):
        json.dump(dict(lines={}, unmodelled={}, terminus_alias={}, terminus_alias_why='', coverage_exceptions={}, owner_checks=[], notes=''),
                  open(lp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    H = json.load(open(lp, encoding='utf-8'))
    C = json.load(open(os.path.join(base, 'data', 'derived', 'line_class.json'), encoding='utf-8'))
    comp = sorted((L for L in C if L in COMP), key=lambda x: (len(x), x))
    unm = auto_unmodelled(oid); unm.update(H.get('unmodelled', {}))
    for L in comp: unm.pop(L, None)
    for L in H.get('lines', {}): unm.pop(L, None)        # a designed line (889 Chotutice, X390) is not 'not modelled'
    other = {'praha_bus': dict(lines=comp, label='Prague Bus Lines Check', short='Prague bus sheet', url=CFG['praha_bus']['url'],
                               why='regional companions of the city lines (through, pooled or interleaved), modelled on the Prague bus sheet with their buses (owner, 30 Oct 2026)'),
             'praha_city': dict(lines=[], label='Prague Bus Lines Check (city lines 100-299)', short='Prague bus sheet', url=CFG['praha_bus']['url'],
                                schedule=os.path.relpath(os.path.join(DER, 'praha_city_schedule.json'), base).replace('\\', '/'))}
    for sid, so in OB.items():
        sp = os.path.join(HOME, 'oblasti', sid, 'data', 'derived', 'schedule.json')
        if FINAL and sid != oid and os.path.exists(sp):
            other[sid] = dict(lines=[], label=f"PID {so['name']}", short=f"{so['name']} sheet", url=None,
                              schedule=os.path.relpath(sp, base).replace('\\', '/'))
    cfg = dict(
        title=f"PID {o['name']}", oblast=oid, oblast_name=o['name'], okres=o['okres'], prefix=o['prefix'],
        output_html="PID " + unicodedata.normalize('NFKD', o['name']).encode('ascii', 'ignore').decode() + ".html",   # ASCII file names, as the ODIS sheets
        artifact_url=H.get('artifact_url'), snapshot=CFG['vehicle_day'], vehicle_day=CFG['vehicle_day'],
        vehicle_day_label_en=CFG['vehicle_day_label_en'], network_state_label=CFG['network_state_label'],
        gtfs=CFG['gtfs'], areas=[dict(id=oid, name=o['name'], prefix=o['prefix'], kind='regional')],
        fitwin=[300, 1380], cycle_lay=3, all_termini_are_loops=True,
        stop_name_expansions=[], stop_name_fixed={}, terminus_alias=H.get('terminus_alias', {}),
        terminus_alias_why=H.get('terminus_alias_why', ''), coverage_exceptions=H.get('coverage_exceptions', {}),
        lines=H.get('lines', {}), unmodelled=unm, owner_checks=H.get('owner_checks', []), notes=H.get('notes', ''),
        other_sheets=other, hubs=H.get('hubs', []))
    tmp = os.path.join(base, f'config.json.{os.getpid()}.tmp')
    json.dump(cfg, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); os.replace(tmp, os.path.join(base, 'config.json'))
    print(f"{oid}: {len(C)} lines, {len(cfg['lines'])} designed, {len(unm)} not modelled, {len(comp)} on the Prague bus sheet ({', '.join(comp)}), siblings {len(other) - 2}")
