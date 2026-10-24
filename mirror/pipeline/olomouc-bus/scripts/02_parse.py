"""Parse raw pages into JSON in data/derived/.

  vehicles_<register raw>.json   {fleet number: dict(id, type, full, paint, year, state, active, depot, source)}
                                 DPMO bus register (seznam-autobusu.cz, iddopravce=134) plus the vehicle pages of cars that
                                 turn up in the records but not in the register listing (501 SOR NS 12 electric, 625).
  records_<vehicle date>.json    {line: [record]} per-line vypravenost pages of the vehicle date
  day_<vehicle date>.json        every vehicle number in the day overview (all modes), for the "not out that day" check
  history.json                   {line: [record]} line histories since vypravenost.history_since (all pages)
  coverage.json                  per weekday overview: bus and tram records per line (the day choice)

Usage: python 02_parse.py --state 2026-09-29
"""
import argparse, glob, os, re
from common import state, save, RAW, DER, parse_vypis, parse_register, parse_overview, _txt

DEPOT = {'DH': 'Dolní Hejčínská'}   # register depot code -> garage name (vehicle pages: "garáže Dolní Hejčínská")

def full_type(maker, t):
    t = t.replace('Alpino 8,6', 'Alpino 8.6')
    return f'{maker} {t}'.strip()

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True)
    s = state(ap.parse_args().state); reg = s['register']; D = s['vehicle_date']
    veh = {}
    for tr in reg['tractions']:
        pages = sorted(glob.glob(os.path.join(RAW, 'register', reg['raw'], f'{tr}_*.html')))
        t = ''.join(open(p, encoding='utf-8').read() for p in pages)
        blocks = re.split(r'(?=<tr class="car-line [^"]*first-line" data-car-id)', t)[1:]
        makers = {}
        for b in blocks:
            cid = re.search(r'data-car-id="(\d+)"', b).group(1)
            mt = re.search(r'<td class="manufacturer-type">(.*?)</td>', b, re.S)
            if mt: makers[cid] = _txt(re.sub(r'<b>.*?</b>', '', mt.group(1)))
        depots = {}
        for m in re.finditer(r'data-car-id="(\d+)">\s*<td class=\'plates\'>.*?<td class="no-mobile depots">\s*<b>([^<]*)</b>', t, re.S):
            depots[m.group(1)] = m.group(2)
        for n, v in parse_register(pages).items():
            veh[n] = dict(v, full=full_type(makers.get(v['id'], ''), v['type']), depot=DEPOT.get(depots.get(v['id'], 'DH'), depots.get(v['id'], '?')),
                          active=v['state'] == 'zar', source='register')
    # cars in the records that the register listing does not show
    for p in sorted(glob.glob(os.path.join(RAW, 'car', '*.html'))):
        t = open(p, encoding='utf-8').read(); cid = os.path.splitext(os.path.basename(p))[0]
        txt = _txt(re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S))
        m = re.search(r'Vůz (.+?) #(\d+)(?: [IVX]+)? \( (.+?) \)', txt)
        if not m: continue
        n = m.group(2); ftype = m.group(3)
        st = re.search(r'aktuální stav (\S+(?: odstaven)?)', txt)
        pa = re.findall(r'(?:od výroby|\d{1,2}/\d{4}) dosud ([^.]+?)(?= Vypravenost| Dokumentační|$)', txt)
        yr = re.search(r'rok výroby (\d{4})', txt)
        gar = re.search(r'garáže (.+?) \d{4} - dosud', txt)
        state_ = st.group(1) if st else '?'
        maker = ftype.split(' ')[0]
        veh[n] = dict(id=cid, type=ftype[len(maker) + 1:], types=[ftype], full=ftype, paint=pa[-1].strip() if pa else '',
                      year=yr.group(1) if yr else '', state=state_, active=state_ == 'provozní',
                      depot=gar.group(1) if gar else 'Dolní Hejčínská', source='vehicle page')
    save(veh, os.path.join(DER, f'vehicles_{reg["raw"]}.json'))
    print('vehicles', len(veh), 'active', sum(v['active'] for v in veh.values()))
    rec = {}
    for p in sorted(glob.glob(os.path.join(RAW, 'vypravenost', D, '*.html'))):
        rec[os.path.splitext(os.path.basename(p))[0]] = parse_vypis(p)
    save(rec, os.path.join(DER, f'records_{D}.json'))
    print(D, sum(len(v) for v in rec.values()), 'records on', sum(1 for v in rec.values() if v), 'lines')
    ov = parse_overview(os.path.join(RAW, 'vypravenost', 'overview', f'{D}.html'))
    day = sorted({c for items in ov.values() for _, cs in items for c in cs.split('+') if c})
    save(dict(date=D, cars=day, bus_lines={k[1]: len(v) for k, v in ov.items() if not k[0].startswith('tram')}), os.path.join(DER, f'day_{D}.json'))
    cov = {}
    for p in sorted(glob.glob(os.path.join(RAW, 'vypravenost', 'overview', '*.html'))):
        o = parse_overview(p)
        cov[os.path.splitext(os.path.basename(p))[0]] = dict(
            bus={k[1]: len(v) for k, v in o.items() if not k[0].startswith('tram')},
            tram=sum(len(v) for k, v in o.items() if k[0].startswith('tram')))
    save(cov, os.path.join(DER, 'coverage.json'))
    hist = {}
    for p in sorted(glob.glob(os.path.join(RAW, 'vypravenost', 'history', s['vypravenost']['history_since'], '*.html'))):
        L = os.path.basename(p).split('_')[0]
        hist.setdefault(L, []).extend(parse_vypis(p))
    save(hist, os.path.join(DER, 'history.json'))
    print('history', {k: len(v) for k, v in hist.items()})

if __name__ == '__main__':
    main()
