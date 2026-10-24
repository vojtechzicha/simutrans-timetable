"""List the VZ-DPPardubice objects in the local pak128 checkout -> assets/pak_installed.json (read only).

  python 00_pak_objects.py [--pak C:/Users/vojte/Developer/simutrans-custom-czech-pak128]

Reads every build/VZ-DPPardubice-*/*.dat, keeps each name= with its length= (car units) and engine_type, and the
checkout's commit. 04_fleet.py marks an object "installed" when its name is in this list and "requested" otherwise.
Run it again after the pak session (simutrans-custom-czech-pak128-bd) reports new objects.
"""
import argparse, glob, os, re, subprocess
from common import ASSETS, save

ap = argparse.ArgumentParser(); ap.add_argument('--pak', default=r'C:\Users\vojte\Developer\simutrans-custom-czech-pak128')
a = ap.parse_args()
objs = {}
for f in sorted(glob.glob(os.path.join(a.pak, 'build', 'VZ-DPPardubice-*', '*.dat'))):
    cur = None
    for line in open(f, encoding='utf-8', errors='replace'):
        k, _, v = line.strip().partition('=')
        if k.lower() == 'name': cur = v; objs[cur] = dict(package=os.path.basename(os.path.dirname(f)), dat=os.path.basename(f))
        elif cur and k.lower() in ('length', 'engine_type', 'intro_year', 'payload'): objs[cur][k.lower()] = v
try: commit = subprocess.run(['git', '-C', a.pak, 'log', '-1', '--format=%h %ad', '--date=short'], capture_output=True, text=True).stdout.strip()
except Exception: commit = '?'
save(dict(pak=a.pak.replace(os.sep, '/'), commit=commit, objects=objs), os.path.join(ASSETS, 'pak_installed.json'))
print(len(objs), 'objects at', commit)
for k in objs: print(' ', k)
