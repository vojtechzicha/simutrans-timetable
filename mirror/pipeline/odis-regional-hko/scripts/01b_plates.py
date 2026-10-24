"""Plates seen on the sheet's licences that the Transdev Slezsko register (config.live.fleet) doesn't hold -> data/raw/<snapshot>/
plates.json {plate: {vid, operator, num, type, paint, note}}: the town buses of other operators (ARRIVA in Třinec and Český
Těšín) and the odd unlisted bus, looked up by seznam-autobusu's plate search and the vehicle page (the Havířov/Karviná/
Orlová pipeline's 01d_plates.py method). Plates looked up before, found or not, are kept, so a rebuild makes no request
(--refresh asks again for the ones not found).
"""
import json, os, re, sys
from lib import CONFIG, RAW, rel, load, tramlib

if not CONFIG.get('plate_lookup'): sys.exit(print('plate lookup off for this sheet (config.plate_lookup)'))
out = os.path.join(RAW, 'plates.json')
have = json.load(open(out, encoding='utf-8')) if os.path.exists(out) else {}
fleet = json.load(open(rel(CONFIG['live']['fleet']), encoding='utf-8'))
known = {v['plate'] for v in fleet.values() if v.get('plate')}
lics = {c for x in load('line_class.json').values() for c in x['lics']}
live = json.load(open(os.path.join(RAW, 'live_compact.json'), encoding='utf-8'))['plates']
want = sorted(pl for pl, rows in live.items() if pl not in known and any(r[2] in lics for r in rows))
for pl in want:
    if pl in have and (have[pl] or '--refresh' not in sys.argv): continue      # looked up before; --refresh asks again for the ones not found
    hit = None
    # 1TE 3303; vanity plates, which the register writes number first (the live map's TESIN001 is "001 TESIN")
    for q in (re.sub(r'^(\w{3})(\d{4})$', r'\1 \2', pl), re.sub(r'^([A-Z]+)(\d+)$', r'\2 \1', pl), re.sub(r'^([A-Z]+)(\d+)$', r'\1 \2', pl), pl):
        hits = json.loads(tramlib.http('https://seznam-autobusu.cz/search-autocomplete/plate?text=' + q.replace(' ', '%20')) or '[]')
        hit = next((h for h in hits if h.get('type') == 'Car'), None)
        if hit: break
    if not hit: have[pl] = None; print(pl, 'not found'); continue
    t = tramlib._clean(tramlib.http(f"https://seznam-autobusu.cz/vuz/{hit['id']}"))
    # "Vůz ARRIVA autobusy #71-1101 (SOR NS 12)", or a bus without a fleet number: "Vůz ARRIVA autobusy 1TE 3303 (Škoda Perun 26 BB HE) |"
    m = re.match(r'Vůz (.*?) #(\S+) \((.*?)\)', t) or re.match(r'Vůz (.*?) (\w+ \w+) \((.*?)\) \|', t)
    seg = t[t.find('Přehled nátěrů'):]
    ends = [i for i in (seg.find(m_) for m_ in ('Vypravenost', 'Dokumentační', 'Fotky vozu', 'Našli jste', 'Poslední aktualizace')) if i > 0]
    seg = seg[:min(ends)] if ends else seg[:200]
    # every layer still current: "<from> dosud <paint>" up to the next "<date or 'od výroby'> [<to>] dosud" (a bus wears several:
    # "od výroby dosud bílá 2019 dosud červené logo Transdev 2019 dosud logo dopravy ..."), joined with " & " as the register list writes them
    layers = [re.sub(r'\s+', ' ', m.group(1)).strip() for m in re.finditer(r'dosud (.*?)(?= (?:od výroby|\d{1,2}/\d{4}|\d{4}) (?:\d{1,2}/\d{4} |\d{4} )?dosud|$)', seg)]
    layers = [re.split(r'\s\d{1,2}/\d{4}\b|\sPoslední aktualizace', re.sub(r'\s*(černé zarovnání "hrbu"|poznámka)$', '', l))[0].strip() for l in layers if l]
    paint = ' & '.join(re.sub(r'\s\d{4}$', '', l) for l in layers if l)      # a closed row's start year can trail a layer
    note = re.search(r'poznámka (.*?) (?:výbava|Přehled)', t)
    have[pl] = dict(vid=str(hit['id']), operator=m.group(1) if m else '', num=m.group(2) if m else '', type=m.group(3) if m else '',
                    paint=paint, note=note.group(1) if note else '')
    print(pl, have[pl])
json.dump(have, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(want), 'plates wanted,', sum(1 for p in want if have.get(p)), 'found')
