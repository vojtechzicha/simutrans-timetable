"""Rebuild data/provenance.json from the local Claude Code transcripts.

Every sheet was built in a Claude Code session and published as a claude.ai artifact. The transcripts in
~/.claude/projects/*/ record each publish ("Published <path> at https://claude.ai/artifact/<id> (Version N"),
so they tell when each sheet first appeared, how often it was republished and under which URL.

    python -I tools/mine_transcripts.py            # writes data/provenance.json

Only publishes of files inside the Simutrans-Timetable project folder are kept. The current repo's own
project folder is skipped (its transcripts quote earlier publish lines and would fake new dates).
User messages are never written out: the repo is public.
"""
import glob
import json
import os
import re
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')
PROJ = os.path.expanduser('~/.claude/projects')
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, 'data', 'provenance.json')
SKIP = 'Developer-simutrans-timetable'          # this repo's own sessions
PUB = re.compile(r'Published (.+?\.html) at (https://claude\.ai/artifact/[A-Za-z0-9]+) \(Version (\d+)')


def text_of(content):
    if isinstance(content, str):
        return content
    out = []
    for b in content or []:
        if isinstance(b, dict):
            if b.get('type') == 'text':
                out.append(b.get('text', ''))
            elif b.get('type') == 'tool_result':
                out.append(text_of(b.get('content')))
    return '\n'.join(out)


def rel(path):
    """Path inside the project folder, for sheets only (root or archive/), else None (templates, assets)."""
    path = path.replace('\\', '/')
    if 'Simutrans-Timetable/' not in path:
        return None
    r = path.split('Simutrans-Timetable/', 1)[1]
    return r if '/' not in r or r.startswith('archive/') else None


pubs, writes = [], []
files = glob.glob(os.path.join(PROJ, '*', '*.jsonl')) + glob.glob(os.path.join(PROJ, '*', '*', 'subagents', '*.jsonl'))
for f in files:
    if SKIP in f:
        continue
    parts = os.path.relpath(f, PROJ).split(os.sep)
    project, session = parts[0], parts[1].removesuffix('.jsonl')
    with open(f, encoding='utf-8', errors='replace') as fh:
        for line in fh:
            if 'Simutrans-Timetable' not in line:
                continue
            try:
                o = json.loads(line)
            except ValueError:
                continue
            ts = o.get('timestamp', '')
            content = (o.get('message') or {}).get('content')
            if not isinstance(content, list):
                continue
            for b in content:
                if not isinstance(b, dict):
                    continue
                if o.get('type') == 'user' and b.get('type') == 'tool_result':
                    for m in PUB.finditer(text_of(b.get('content'))):
                        r = rel(m.group(1))
                        if r:
                            pubs.append((ts, r, m.group(2), int(m.group(3)), project, session))
                elif o.get('type') == 'assistant' and b.get('type') == 'tool_use' and b.get('name') in ('Write', 'Edit'):
                    r = rel((b.get('input') or {}).get('file_path', ''))
                    if r and r.endswith('.html'):
                        writes.append((ts, r, project, session))

by = defaultdict(lambda: {'publishes': [], 'writes': []})
for ts, r, url, ver, project, session in sorted(pubs):
    by[os.path.basename(r)]['publishes'].append({'at': ts, 'path': r, 'url': url, 'version': ver, 'session': session})
for ts, r, project, session in sorted(writes):
    by[os.path.basename(r)]['writes'].append({'at': ts, 'path': r, 'session': session})

result = {}
for name, d in sorted(by.items()):
    p, w = d['publishes'], d['writes']
    stamps = [x['at'] for x in p + w if x['at']]
    result[name] = {
        'firstSeen': min(stamps) if stamps else None,
        'firstPublished': p[0]['at'] if p else None,
        'lastPublished': p[-1]['at'] if p else None,
        'publishCount': len(p),
        'latestVersion': max((x['version'] for x in p), default=None),
        'artifactUrls': sorted({x['url'] for x in p}),
        'sessions': sorted({x['session'] for x in p + w}),
        'paths': sorted({x['path'] for x in p + w}),
    }

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', encoding='utf-8') as fh:
    json.dump({'_doc': __doc__.strip().splitlines()[0], 'sheets': result}, fh, ensure_ascii=False, indent=1)
print(f'{len(result)} sheets, {len(pubs)} publishes -> {os.path.relpath(OUT, REPO)}')
