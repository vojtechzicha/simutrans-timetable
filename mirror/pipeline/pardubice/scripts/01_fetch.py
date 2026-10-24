"""Download the raw inputs into data/raw/<kind>/<date>/ exactly as fetched.

  python 01_fetch.py --state 2026-09-29 [--jdf] [--jdf-download] [--records] [--register] [--history]
  (no flag = --jdf --records --register --history; files already on disk are not fetched again)

--jdf           Copy DPMP's inner zips (licences 655xxx, operator IČO 63217066) byte for byte out of the CIS JŘ
                exports named in state.jdf.sources into data/raw/jdf/<export date>/<city|bus>/. The exports are the
                ones the Ostrava pipelines already downloaded (the city export holds the trolleybus lines, the
                ~107 MB bus export the bus lines), so nothing is downloaded again.
--jdf-download  Download fresh exports (state.jdf.urls) into the scratch folder data/raw/jdf/_download/ first and
                extract from those instead; delete that folder afterwards (it is large).
--records       seznam-autobusu.cz day records for each day in state.records.days: the list
                vypravenost/<slug>/vypis?datum=D (all pages, vypis_p<N>.html) and the day overview
                vypravenost/<slug>?datum=D (overview.html; every car out that day, by line and kurz).
--register      The DPMP fleet register (iddopravce 47): trakce=trolejbus and trakce=autobus, all pages.
--history       Per-line history vypravenost/<slug>/vypis?linka=<id>&since=<history.since>, all pages, for every
                line in history.lines (designed vehicles come from it) -> data/raw/vypravenost/history/<since>/; for the
                lines in history.fallback_lines (no record since then) the latest records of any date, first
                history.fallback_pages pages -> data/raw/vypravenost/history/latest/.
"""
import argparse, csv, glob, io, os, re, shutil, zipfile
from common import RAW, state, fetch, next_page

ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True)
for f in ('--jdf', '--jdf-download', '--records', '--register', '--history'): ap.add_argument(f, action='store_true')
a = ap.parse_args(); S = state(a.state)
if not any([a.jdf, a.jdf_download, a.records, a.register, a.history]): a.jdf = a.records = a.register = a.history = True
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = S['records']['slug']

def pages(url, dest_fmt):
    """Fetch url, url&strana=2, ... until the page has no link to the next one."""
    p = 1
    while True:
        dest = dest_fmt.format(p=p)
        if os.path.exists(dest): s = open(dest, encoding='utf-8').read()
        else: s = fetch(url + (f'&strana={p}' if p > 1 else ''), dest).decode('utf-8', 'replace'); print('  got', os.path.relpath(dest, RAW))
        if not next_page(s, p): return p
        p += 1

if a.jdf or a.jdf_download:
    J = S['jdf']; out = os.path.join(RAW, 'jdf', J['export_date'])
    srcs = {k: os.path.normpath(os.path.join(BASE, v)) for k, v in J['sources'].items()}
    if a.jdf_download:
        tmp = os.path.join(RAW, 'jdf', '_download'); os.makedirs(tmp, exist_ok=True)
        for k, u in J['urls'].items():
            srcs[k] = os.path.join(tmp, f'{k}_JDF.zip'); fetch(u, srcs[k], pause=1); print('downloaded', k)
    for kind, src in srcs.items():
        z = zipfile.ZipFile(src); n = 0
        for name in z.namelist():
            b = z.read(name)
            try: inner = zipfile.ZipFile(io.BytesIO(b))
            except zipfile.BadZipFile: continue
            ln = [x for x in inner.namelist() if x.lower().startswith('linky')]
            if not ln: continue
            rows = [r for r in csv.reader(io.StringIO(inner.read(ln[0]).decode('cp1250').replace(';\r\n', '\n').replace(';\n', '\n'))) if r]
            if any(r[0].startswith(J['line_prefix']) and r[2] == J['operator_ic'] for r in rows):
                d = os.path.join(out, kind); os.makedirs(d, exist_ok=True)
                open(os.path.join(d, name), 'wb').write(b); n += 1
        print('jdf', kind, n, 'DPMP inner zips from', src)

if a.records:
    for d in S['records']['days']:
        base = f'https://seznam-autobusu.cz/vypravenost/{SLUG}/vypis?datum={d}'
        n = pages(base, os.path.join(RAW, 'vypravenost', d, 'vypis_p{p}.html'))
        dest = os.path.join(RAW, 'vypravenost', d, 'overview.html')
        if not os.path.exists(dest): fetch(f'https://seznam-autobusu.cz/vypravenost/{SLUG}?datum={d}', dest)
        print('records', d, n, 'pages + overview')

if a.register:
    for tr in S['register']['tractions']:
        url = f"https://seznam-autobusu.cz/seznam?prov=1&trakce={tr}&iddopravce={S['register']['iddopravce']}&vcetneSluzebnich=1"
        p = 1
        while True:
            dest = os.path.join(RAW, 'register', S['register_date'], f'{tr}_p{p}.html')
            s = open(dest, encoding='utf-8').read() if os.path.exists(dest) else fetch(url + (f'&page={p}' if p > 1 else ''), dest).decode('utf-8', 'replace')
            if not next_page(s, p): break
            p += 1
        print('register', tr, p, 'pages')

if a.history:
    H = S['history']
    for L in H['lines']:
        lid = H.get('ids', {}).get(L, L)
        base = f"https://seznam-autobusu.cz/vypravenost/{SLUG}/vypis?linka={lid}&since={H['since']}"
        n = pages(base, os.path.join(RAW, 'vypravenost', 'history', H['since'], f'L{L}_p{{p}}.html'))
        print('history', L, n, 'pages')
    # lines with no record since history.since: the latest records of any date (history.fallback_pages pages, newest first)
    for L in H.get('fallback_lines', []):
        lid = H.get('ids', {}).get(L, L)
        for p in range(1, H.get('fallback_pages', 2) + 1):
            dest = os.path.join(RAW, 'vypravenost', 'history', 'latest', f'L{L}_p{p}.html')
            s = open(dest, encoding='utf-8').read() if os.path.exists(dest) else                 fetch(f"https://seznam-autobusu.cz/vypravenost/{SLUG}/vypis?linka={lid}" + (f'&strana={p}' if p > 1 else ''), dest).decode('utf-8', 'replace')
            if not next_page(s, p): break
        print('history (latest records)', L)
