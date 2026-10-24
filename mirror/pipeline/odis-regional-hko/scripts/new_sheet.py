"""Skeleton config for a new ODIS regional sheet of this pipeline: python new_sheet.py <spec.json>

The spec names the sheet (folder, title, output_html, areas with prefix/kind/ic/town/branch/depot/fleet, live carriers,
fleet carriers). Everything else is taken from the Těšínsko/Třinecko/Frýdecko sheet's config (JDF, live poll, version
rule, stop-name handling, other sheets), plus:
- towns: the first parts of every stop of the sheet's regional licences in the JDF (a town JDF's stop whose first part is
  not one of them gets the town in front, 02_timetable.py);
- other_sheets.ostrava.lines: the sheet's ODIS numbers that the Ostrava sheet's Hranečník cards already model.
An existing config.json is never overwritten (delete it first to start again).
"""
import csv, io, json, os, re, sys, zipfile
HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); PIPE = os.path.dirname(HOME)
spec = json.load(open(sys.argv[1], encoding='utf-8'))
base = os.path.join(PIPE, spec['folder'])
if os.path.exists(os.path.join(base, 'config.json')): sys.exit(f"{base}/config.json exists")
tfj = json.load(open(os.path.join(PIPE, 'odis-regional-tfj', 'config.json'), encoding='utf-8'))
c = {k: tfj[k] for k in ('snapshot', 'vehicle_day', 'vehicle_day_label_en', 'network_state_label', 'fitwin', 'cycle_lay',
                         'all_termini_are_loops', 'stop_name_expansions', 'stop_name_fixed', 'jdf')}
c['jdf'] = dict(tfj['jdf'])
c.update(title=spec['title'], output_html=spec['output_html'], artifact_url=None, areas=spec['areas'])
c['live'] = dict(tfj['live'], carriers=spec['live_carriers'], fleet='data/derived/fleet.json')
c['fleet'] = dict(carriers=spec['fleet_carriers'])
c['plate_lookup'] = True; c['designed_same_area'] = True
c['terminus_alias'] = {}; c['terminus_alias_why'] = ''
c['lines'] = {}; c['unmodelled'] = {}; c['network_state'] = []; c['owner_checks'] = []
c['texts'] = spec.get('texts', {}); c['pak'] = dict(repo=tfj['pak']['repo'], package='VZ-ODIS-bus', packages=['VZ-ODIS-bus'], why='', types={}, paints=[], special={}, rules=[])
# other sheets: relative to the new folder (a sibling of odis-regional-tfj, so the same relative paths hold)
c['other_sheets'] = json.loads(json.dumps(tfj['other_sheets']))
c['other_sheets']['hko_regional']['lines'] = []
c['other_sheets']['tfj'] = dict(lines=[], label='ODIS Těšínsko Třinecko Frýdecko', short='Těšínsko/Třinecko/Frýdecko sheet',
                                derived='../odis-regional-tfj/data/derived/roster.json', schedule='../odis-regional-tfj/data/derived/schedule.json',
                                url=tfj['artifact_url'])
# JDF scan: the sheet's licences (prefix + operator), their stops' first parts, and the Ostrava cards
zp = os.path.normpath(os.path.join(PIPE, 'odis-regional-tfj', tfj['jdf']['zip']))
outer = zipfile.ZipFile(zp); towns = set(); nums = set()
def tab(inner, name):
    n = [x for x in inner.namelist() if x.lower().startswith(name)]
    return list(csv.reader(io.StringIO(inner.read(n[0]).decode('cp1250').replace(';\r\n', '\n').replace(';\n', '\n')))) if n else []
for n in outer.namelist():
    try: inner = zipfile.ZipFile(io.BytesIO(outer.read(n)))
    except zipfile.BadZipFile: continue
    ln = tab(inner, 'linky')
    if not ln or not ln[0]: continue
    a = next((a for a in spec['areas'] if ln[0][0].startswith(a['prefix']) and ln[0][2] == a.get('ic', spec['operator_ic'])), None)
    if not a: continue
    nums.add(ln[0][0][-3:])
    if a.get('kind') == 'mhd': continue
    for r in tab(inner, 'zastavky'):
        if len(r) > 1 and r[1]: towns.add(r[1].strip())
c['jdf']['operator_ic'] = spec['operator_ic']; c['jdf']['why'] = spec.get('jdf_why', '')
c['towns'] = sorted(towns); c['towns_why'] = 'the first part of every stop of the regional licences (new_sheet.py)'
ost = json.load(open(os.path.join(PIPE, 'ostrava-bus', 'data', 'derived', 'odis.json'), encoding='utf-8'))
c['other_sheets']['ostrava']['lines'] = sorted(set(ost['lines']) & nums)
os.makedirs(os.path.join(base, 'data', 'derived'), exist_ok=True)
json.dump(c, open(os.path.join(base, 'config.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(spec['folder'], len(nums), 'ODIS numbers;', len(towns), 'towns; on the Ostrava sheet:', c['other_sheets']['ostrava']['lines'])
