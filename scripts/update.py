"""Refresh only the generated part of the organization profile."""
import json
from pathlib import Path
import subprocess

org = 'MoLik-Labs'
lines = subprocess.check_output([
    'gh', 'api', '--paginate', '--jq', '.[] | @json', f'orgs/{org}/repos?per_page=100&type=public'
]).splitlines()
repos = sorted((r for r in map(json.loads, lines) if not (
    r['private'] or r['fork'] or r['archived'] or r['name'] == '.github'
)), key=lambda r: (r['pushed_at'] or '', r['name']), reverse=True)
rows = ['| Repository | Language | Last push |', '| :--- | :--- | :--- |']
for r in repos[:5]:
    rows.append(f"| [{r['name']}]({r['html_url']}) | {r['language'] or '—'} | {(r['pushed_at'] or '—')[:10]} |")
path = Path(__file__).resolve().parents[1] / 'profile/README.md'
old = path.read_text()
start, end = '<!-- index:start -->', '<!-- index:end -->'
if old.count(start) != 1 or old.count(end) != 1 or old.index(start) >= old.index(end):
    raise ValueError('Invalid repository index markers')
path.write_text(old.split(start)[0] + '\n'.join([start, *rows, end]) + old.split(end)[1])
