"""Register pages -> data/derived/vehicles_<register date>.json, keyed by the register's car id (data-car-id).

Sources (seznam-autobusu.cz, in-service buses, trakce=autobus): DPP (dpp_bus_*.html) and the other PID city operators
(op_<slug>_*.html); single car pages (vuz_<id>.html) fill in cars the lists miss (e.g. DPP electric buses).
Per car: number, maker_type, type, operator, garage (the register's short code expanded by bus_types.json "garages"),
paint (current), year, state.

Usage: python 02_register.py --state 2026-09-29
"""
import argparse, glob, os, re, collections
from common import state, load, save, RAW, DER, ASSETS, _txt

OPS = {'dpp': 'DPP', 'arriva-city': 'ARRIVA CITY', 'stenbus': 'STENBUS', 'about-me': 'ABOUT ME', 'csad-stredni-cechy': 'ČSAD Střední Čechy',
       'martin-uher': 'MARTIN UHER', 'csad-polkost': 'ČSAD POLKOST', 'vega-tour': 'Vega Tour', 'arriva-stredni-cechy': 'ARRIVA STŘEDNÍ ČECHY',
       'umbrella-city-lines': 'UMBRELLA CITY LINES', 'csad-benesov': 'ČSAD Benešov'}

def parse_list(t, operator, garages):
    out = {}
    for b in re.split(r'(?=<tr class="car-line [^"]*first-line" data-car-id)', t)[1:]:
        cid = re.search(r'data-car-id="(\d+)"', b).group(1)
        num = re.search(r'<span class="bold 1 number"><!--\s*-->([\w-]+)', b)
        mt = re.search(r'<td class="manufacturer-type">(.*?)</td>', b, re.S)
        dp = re.search(r'<td class="depots">(.*?)</td>', b, re.S)
        pm = re.search(r'<span class="label">nátěr:</span>(.*?)</span>', b, re.S)
        yr = re.search(r'<td class="font085">(\d{4})', b)
        code = _txt(dp.group(1)).rstrip('*').strip() if dp else ''
        out[cid] = dict(num=num.group(1) if num else '', maker_type=_txt(mt.group(1)) if mt else '', operator=operator,
                        garage=garages[code] if code in garages else code, paint=_txt(pm.group(1)).rstrip('*').strip() if pm else '',
                        year=yr.group(1) if yr else '', state=re.search(r'<tr class="car-line (\w+)', b).group(1), source='list')
    return out

def parse_car(t):
    t = re.sub(r'<style.*?</style>|<script.*?</script>', '', t, flags=re.S)
    ty = re.search(r'class="types">.*?<b>\s*<a[^>]*>(.*?)</a>', t, re.S)
    op = re.search(r'<tr class="active">.*?class="operator-name"><a[^>]*>(.*?)</a>', t, re.S)
    pa = re.search(r'<tr class="active">\s*<td class="since">.*?<td class="paint">(.*?)</td>', t, re.S)
    txt = _txt(t[t.find('car-detail-control'):])
    dm = re.findall(r'([A-ZČŘŠŽÝÁÍÉÚ][^0-9]{2,40}?) (?:\d{1,2}/)?\d{4} - dosud', txt)
    num = re.findall(r'(\d{3,5}) (?:I{1,3} )?od (?:\d{1,2}/)?\d{4}', txt)
    yr = re.search(r'rok výroby (\d{4})', txt)
    opn = _txt(op.group(1)) if op else ''
    return dict(num=num[-1] if num else '', maker_type=_txt(ty.group(1)) if ty else '', operator='DPP' if opn.startswith('Dopravní podnik') else opn,
                garage=dm[0].strip() if dm else '', paint=_txt(pa.group(1)) if pa else '', year=yr.group(1) if yr else '', state='zar', source='car page')

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True); s = state(ap.parse_args().state)
    garages = load(os.path.join(ASSETS, 'bus_types.json'))['garages']
    d = os.path.join(RAW, 'register', s['register_raw'])
    veh = {}
    for p in sorted(glob.glob(os.path.join(d, 'dpp_bus_*.html'))):
        veh.update(parse_list(open(p, encoding='utf-8').read(), 'DPP', garages))
    for p in sorted(glob.glob(os.path.join(d, 'op_*.html'))):
        slug = re.match(r'op_(.+)_\d+\.html', os.path.basename(p)).group(1)
        veh.update(parse_list(open(p, encoding='utf-8').read(), OPS[slug], garages))
    for p in sorted(glob.glob(os.path.join(d, 'vuz_*.html'))):
        cid = re.search(r'vuz_(\d+)', p).group(1)
        if cid not in veh: veh[cid] = parse_car(open(p, encoding='utf-8').read())
    save(veh, os.path.join(DER, f'vehicles_{s["register_raw"]}.json'))
    print(len(veh), 'vehicles', collections.Counter(v['operator'] for v in veh.values()))

if __name__ == '__main__':
    main()
