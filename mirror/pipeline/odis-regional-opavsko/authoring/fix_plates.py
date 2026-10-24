"""Re-read the paint of every looked-up plate (data/raw/<snapshot>/plates.json): the shared 01b_plates.py keeps only the last
paint layer that runs "dosud" (to date), but seznam-autobusu lists layers, e.g. "od výroby dosud bílá … 2019 dosud červené logo
Transdev 2019 dosud logo dopravy Moravskoslezského kraje" -> "bílá & červené logo Transdev & logo dopravy Moravskoslezského
kraje" (the register list's own format). Run once after 01b; plates already fixed are skipped (key 'paint_layers')."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ['ODIS_BASE'] = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(HERE, '..', '..', 'odis-regional-hko', 'scripts'))
from lib import RAW, tramlib
p = os.path.join(RAW, 'plates.json'); P = json.load(open(p, encoding='utf-8'))
for pl, x in P.items():
    if not x or x.get('paint_layers'): continue
    t = tramlib._clean(tramlib.http(f"https://seznam-autobusu.cz/vuz/{x['vid']}", pause=1))
    seg = t[t.find('Přehled nátěrů'):]
    seg = seg[:min([i for i in (seg.find(m) for m in ('Vypravenost', 'Dokumentační', 'Fotky vozu', 'Našli jste', 'Poslední aktualizace')) if i > 0] or [300])]
    # each current layer: "<from> dosud <paint>" up to the next "<date or 'od výroby'> dosud"
    layers = [re.sub(r'\s+', ' ', m.group(1)).strip() for m in re.finditer(r'dosud (.*?)(?= (?:od výroby|\d{1,2}/\d{4}|\d{4}) (?:\d{1,2}/\d{4} |\d{4} )?dosud|$)', seg)]
    layers = [re.sub(r'\s*(černé zarovnání "hrbu"|poznámka)$', '', l).strip() for l in layers if l]
    if layers: x['paint'] = ' & '.join(layers); x['paint_layers'] = layers
    print(pl, x.get('num'), '|', x['paint'])
json.dump(P, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
