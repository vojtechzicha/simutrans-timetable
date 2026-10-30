"""Pak checkouts -> assets/pak_objects.json: every object name in the Prague bus and ferry packages (build/VZ-DPPraha-bus,
build/VZ-Praha-bus, build/VZ-Praha-water), so the sheet knows which objects exist.

build/ is generated and not in git, and the pak session builds in its own worktrees (the Prague buses were built in
simutrans-custom-czech-pak128-pidops, commit fb42eb7). So this reads the build folders of every worktree of the pak
repository (`git worktree list`) and records, per package, the worktree and commit it came from (the newest build wins).

Usage: python 00_pak_objects.py [--pak C:/Users/vojte/Developer/simutrans-custom-czech-pak128]
"""
import argparse, glob, os, re, subprocess
from common import save, ASSETS

PKGS = ('VZ-DPPraha-bus', 'VZ-Praha-bus', 'VZ-Praha-water', 'VZ-PID-bus')   # VZ-PID-bus: the PID suburban/regional contracts (fleet desk, 30 Oct 2026)

def git(repo, *args):
    return subprocess.run(['git', '-C', repo, *args], capture_output=True, text=True, encoding='utf-8', errors='replace').stdout

ap = argparse.ArgumentParser(); ap.add_argument('--pak', default=r'C:\Users\vojte\Developer\simutrans-custom-czech-pak128')
a = ap.parse_args()
trees = [l[9:].strip() for l in git(a.pak, 'worktree', 'list', '--porcelain').splitlines() if l.startswith('worktree ')] or [a.pak]
names, source = {}, {}
for pkg in PKGS:
    best = None
    for w in trees:
        dats = glob.glob(os.path.join(w, 'build', pkg, '**', '*.dat'), recursive=True)
        if dats:
            mt = max(os.path.getmtime(p) for p in dats)
            if best is None or mt > best[0]: best = (mt, w, dats)
    if not best: continue
    _, w, dats = best
    for p in dats:
        for n in re.findall(r'^name=(\S+)', open(p, encoding='utf-8', errors='replace').read(), flags=re.M):
            names[n] = pkg
    source[pkg] = dict(worktree=w, commit=git(w, 'log', '-1', '--format=%h %cs %s').strip())
commit = '; '.join(f"{p}: {v['commit'].split(' ')[0]}" for p, v in source.items())
save(dict(commit=commit, source=source, objects=dict(sorted(names.items()))), os.path.join(ASSETS, 'pak_objects.json'))
print(commit, len(names), 'objects', {p: sum(1 for v in names.values() if v == p) for p in PKGS})
