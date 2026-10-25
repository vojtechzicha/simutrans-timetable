"""Changed text of a sheet against its snapshot: htmldiff.py OLD.html NEW.html -> the differing table rows / blocks, as text."""
import difflib, html, re, sys
sys.stdout.reconfigure(encoding='utf-8')
def lines(p):
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'(?s)<style.*?</style>|<script.*?</script>', '', s)
    s = re.sub(r'</(tr|p|li|h[1-6]|div|article|header|details|summary|table)>', '\n', s)
    s = re.sub(r'<(td|th)[^>]*>', ' | ', s); s = re.sub(r'<[^>]+>', '', s)
    return [re.sub(r'\s+', ' ', html.unescape(l)).strip() for l in s.split('\n') if l.strip()]
a, b = lines(sys.argv[1]), lines(sys.argv[2])
d = [l for l in difflib.unified_diff(a, b, lineterm='', n=0) if not l.startswith(('---', '+++', '@@'))]
print(len([l for l in d if l.startswith('-')]), 'lines out,', len([l for l in d if l.startswith('+')]), 'lines in')
for l in d[:int(sys.argv[3]) if len(sys.argv) > 3 else 60]: print(l[:240])
