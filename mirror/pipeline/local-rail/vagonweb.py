"""Train compositions (řazení) from vagonweb.cz: planned type and sighted units per date.

Use it to decide whether a line's long and short runs share vehicles (user, 5 Oct 2026: share one Simutrans line only
where the same vehicles really run both parts). Sightings on the same day show how a unit moves between trains.

    python pipeline/local-rail/vagonweb.py CZ-014 22212,22213,22222,22225
    python pipeline/local-rail/vagonweb.py CZ-220 2483,2478 Sp Sázava   (category and train name, for named trains)
    python pipeline/local-rail/vagonweb.py CZ-200 1172,1171 R "" ARV    (operator other than ČD: Arriva = ARV)

The first argument is the vagonweb line (relace) used as referer, e.g. CZ-014 or CZ-235.

Notes on the site:
- zeme must be "ČD" (URL-encoded %C4%8CD); with "CD" the page loads without any composition.
- The composition is only served to a session: get a PHPSESSID cookie first and send a referer, or the page comes back without it.
"""
import re
import subprocess
import sys
import time
from urllib.parse import quote

sys.stdout.reconfigure(encoding='utf-8')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36'
JAR = 'vagonweb_cookies.txt'


def curl(url, referer):
    return subprocess.run(['curl', '-s', '-c', JAR, '-b', JAR, '-A', UA, '-H', 'Accept: text/html',
                           '-H', 'Accept-Language: cs-CZ,cs;q=0.9', '-e', referer, url],
                          capture_output=True).stdout.decode('utf-8', 'replace')


def train(num, relace, year='2026', cat='Os', name='', zeme='ČD'):
    # named trains need their name (R49 = Sp "Sázava"; find it in the relace page's links, e.g. relace CZ-220)
    referer = f'https://www.vagonweb.cz/razeni/razeni.php?rok={year}&relace={relace}'
    h = curl(f'https://www.vagonweb.cz/razeni/vlak.php?zeme={quote(zeme)}&kategorie={cat}&cislo={num}&nazev={quote(name)}&rok={year}', referer)
    t = re.sub(r'<script.*?</script>|<style.*?</style>', '', h, flags=re.S)
    t = re.sub(r'<[^>]+>', ' | ', t)
    t = re.sub(r'(\s*\|\s*)+', ' | ', t)
    t = t[t.find('| Trasa |'):t.find('Údaje jsou bez záruky')]
    route = re.search(r'Trasa \| ([^|]*)', t)
    plan = re.search(r'Plánované řazení(.*?)Vložil', t)
    plan = re.sub(r'\s*\|\s*(&nbsp;\s*\|\s*)*', ' ', plan.group(1)).strip() if plan else '—'
    sights = []
    for d, body in re.findall(r'Skutečné řazení vlaku dne: \| (\S+ [\d.]+)(.*?)Vložil', t):
        units = [re.sub(r'\s+', ' ', x) for x in re.findall(r'95 54 5 \| (\d{3}\s+\d{3})', body)]
        sights.append((d, units))
    return (route.group(1).strip() if route else '?'), plan, sights


def main():
    relace, nums = sys.argv[1], sys.argv[2].split(',')
    cat = sys.argv[3] if len(sys.argv) > 3 else 'Os'
    name = sys.argv[4] if len(sys.argv) > 4 else ''
    zeme = sys.argv[5] if len(sys.argv) > 5 else 'ČD'  # the operator code on vagonweb, e.g. ARV for Arriva (R26)
    curl('https://www.vagonweb.cz/razeni/', 'https://www.vagonweb.cz/')  # session cookie
    for n in nums:
        r, p, s = train(n, relace, cat=cat, name=name, zeme=zeme)
        print(f'{cat} {n}: {r}\n   planned: {p}\n   seen: ' + '; '.join(f"{d} {','.join(u) or '?'}" for d, u in s[:10]))
        time.sleep(0.7)


if __name__ == '__main__':
    main()
