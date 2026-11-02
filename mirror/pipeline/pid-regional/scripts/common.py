"""Shared helpers of the PID regional pipeline (stdlib only)."""
import os, re, time, html, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.dirname(HERE)                     # pipeline/pid-regional
PIPE = os.path.dirname(HOME)
RAW = os.path.join(HOME, 'data', 'raw')
DER = os.path.join(HOME, 'data', 'derived')
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/129.0.0.0 Safari/537.36')

def fetch(url, dest, pause=2.5, tries=6):
    """GET url into dest with full browser headers (seznam-autobusu.cz answers 403 to plain clients); on 429 / 5xx back
    off and retry. Returns the bytes."""
    for k in range(tries):
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml,*/*;q=0.8',
                                                   'Accept-Language': 'cs,en;q=0.8'})
        try:
            with urllib.request.urlopen(req, timeout=120) as r: data = r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and k + 1 < tries:
                time.sleep(30 * (k + 1)); continue
            raise
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'wb') as f: f.write(data)
        time.sleep(pause)
        return data

def txt(s): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s or ''))).strip()

def parse_overview(path):
    """seznam-autobusu.cz day overview (vypravenost/pid?datum=D) -> {line: [dict(course, cars=[num], ids=[car id])]}"""
    out = {}
    for sec in open(path, encoding='utf-8').read().split('<div class="route-data">')[1:]:
        m = re.search(r'linka=[^"&]+">([^<]+)</a>', sec)
        if not m: continue
        L = m.group(1).strip(); rows = []
        for it in sec.split('<span class="item">')[1:]:
            c = re.search(r'class="course">([^<]*)<', it)
            vs = re.findall(r'class="context-box" href="https://seznam-autobusu.cz/vuz/(\d+)/vypravenost">([^<]+)</a>', it)
            if vs: rows.append(dict(course=c.group(1).strip() if c else '', cars=[n.strip() for _, n in vs], ids=[i for i, _ in vs]))
        out[L] = rows
    return out
