"""Plates seen in the live feed on the sheet's lines that the register list (prov=1) doesn't hold -> data/raw/<snapshot>/
plates.json {plate: {vid, num, type, paint, note}}, looked up by seznam-autobusu's plate search and the vehicle page
(e.g. Orlová Dekstra 448, which the register list leaves out but which ran 501/503 on 20 Oct 2026). Run after 03_fleet.py
(it reads live.json 'unknown'); 03_fleet.py then merges them into the fleet."""
import json, os, re
from lib import RAW, http, load, tramlib

out = os.path.join(RAW, 'plates.json')
have = json.load(open(out, encoding='utf-8')) if os.path.exists(out) else {}
for pl in load('live.json')['unknown']:
    if pl in have: continue
    q = re.sub(r'^(\w{3})(\d{4})$', r'\1 \2', pl)
    hits = json.loads(http('https://seznam-autobusu.cz/search-autocomplete/plate?text=' + q.replace(' ', '%20')) or '[]')
    hit = next((h for h in hits if h.get('type') == 'Car'), None)
    if not hit: have[pl] = None; print(pl, 'not found'); continue
    t = tramlib._clean(http(f"https://seznam-autobusu.cz/vuz/{hit['id']}"))
    m = re.match(r'Vůz (.*?) #(\S+) \((.*?)\)', t)
    seg = t[t.find('Přehled nátěrů'):]
    ends = [i for i in (seg.find(m) for m in ('Vypravenost', 'Dokumentační', 'Fotky vozu', 'Našli jste')) if i > 0]   # a bus with no records has no Vypravenost table
    seg = seg[:min(ends)] if ends else seg[:200]
    paint = seg.rsplit('dosud ', 1)[-1].strip() if 'dosud' in seg else ''
    note = re.search(r'poznámka (.*?) (?:výbava|Přehled)', t)
    have[pl] = dict(vid=str(hit['id']), operator=m.group(1) if m else '', num=m.group(2) if m else '', type=m.group(3) if m else '',
                    paint=paint, note=note.group(1) if note else '')
    print(pl, have[pl])
json.dump(have, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
