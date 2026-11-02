"""Day overviews of seznam-autobusu.cz PID vypravenost (every vehicle logged that day, by line and course) for the given
dates -> data/raw/vypravenost/<date>/overview.html. Usage: python 01_overviews.py 2026-10-27 2026-10-26 ..."""
import os, sys
from common import fetch, RAW, parse_overview
for d in sys.argv[1:]:
    dest = os.path.join(RAW, 'vypravenost', d, 'overview.html')
    if not os.path.exists(dest): fetch(f'https://seznam-autobusu.cz/vypravenost/pid?datum={d}', dest)
    ov = parse_overview(dest)
    reg = {L: v for L, v in ov.items() if L[:1] in '345678' and L.isdigit() and len(L) == 3}
    print(d, 'lines', len(ov), 'regional', len(reg), 'courses', sum(len(v) for v in reg.values()), flush=True)
