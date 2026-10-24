"""Proposed halt renames for the save game: game stop names that are misspellings of the PID name -> data/derived/<state>/halt_renames.tsv
in the save-game session's format (KIND<TAB>ID<TAB>OLD NAME<TAB>NEW NAME, see README). Only the misspelt part changes; names where PID
itself abbreviates (VÚ Běchovice) are left alone, so the game keeps the full words. Nothing is sent: the user decides.

Usage: python 07_halt_renames.py --state 2026-09-29
"""
import argparse, os
from common import state, load, RAW, DER

KEEP = {'VÚ Běchovice'}          # PID abbreviates; the game's full name stays

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True); s = state(ap.parse_args().state)
    G = load(os.path.join(RAW, 'game', s['game_raw'], 'lines.json'))
    C = load(os.path.join(DER, s['name'], 'compare.json'))
    ids = {e['halt_name']: e['halt_id'] for l in G['lines'] for e in l['entries'] if e.get('halt_name')}
    fixes = {a: b for r in C['lines'] for a, b in r.get('name_fixes', {}).items() if b not in KEEP}
    rows = ['# Proposed by pipeline/praha-bus/scripts/07_halt_renames.py: game stop names that misspell the PID name', '# KIND\tID\tOLD NAME\tNEW NAME']
    for old, pid in sorted(fixes.items()):
        parts = old.split(' / ')
        k = next((i for i, p in enumerate(parts) if p.startswith('Praha, ')), None)
        if k is None: continue
        head = 'Praha, '; body = parts[k][len(head):]
        stand = body[body.index(' ['):] if ' [' in body else ''
        parts[k] = head + pid + stand
        rows.append(f'halt\t{ids[old]}\t{old}\t{" / ".join(parts)}')
    out = os.path.join(DER, s['name'], 'halt_renames.tsv')
    open(out, 'w', encoding='utf-8').write('\n'.join(rows) + '\n')
    print(len(rows) - 2, 'renames ->', out)

if __name__ == '__main__':
    main()
