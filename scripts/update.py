"""Refresh only the generated part of the organization profile."""
from datetime import datetime, timezone
from pulse import render
from edition import select
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
# The project core can differ from Linguist’s repository-wide byte majority.
for r in repos:
    if r['name'].upper() == 'ZMRIG':
        r['language'] = 'Zig'
rows = ['| Repository | Project language | Last push |', '| :--- | :--- | :--- |']
for r in repos[:5]:
    rows.append(f"| [{r['name']}]({r['html_url']}) | {r['language'] or '—'} | {(r['pushed_at'] or '—')[:10]} |")
path = Path(__file__).resolve().parents[1] / 'profile/README.md'
old = path.read_text()
start, end = '<!-- index:start -->', '<!-- index:end -->'
if old.count(start) != 1 or old.count(end) != 1 or old.index(start) >= old.index(end):
    raise ValueError('Invalid repository index markers')
today = datetime.now(timezone.utc).date()
feature = select(today)
issue = today.strftime('%Y.%m')
url = f'https://github.com/{org}/{feature.project}' + ('/' + feature.path if feature.path else '')
banner = Path(__file__).with_name('masthead.svg.in').read_text()
(path.parent / 'assets/masthead.svg').write_text(banner.replace('@EDITION@', issue)
    .replace('@TRACK@', feature.track.upper()).replace('@PROJECT@', feature.project)
    .replace('@ACCENT@', feature.accent))
svg, summary = render(repos, today)
(path.parent / 'assets/pulse.svg').write_text(svg)
stars = sum(r['stargazers_count'] for r in repos)
forks = sum(r['forks_count'] for r in repos)
rows = [f'> **Field notes · {issue}** — [{feature.project}]({url}) · {feature.copy}', '',
        f'![{summary}; project language counts](assets/pulse.svg)', '',
        f'**{summary}.** Each repository counts once. We use GitHub’s primary language except for ZMRIG, classified by its Zig miner core.', '',
        '| Tracked projects | Stars received | Forks received |',
        '| :--- | :--- | :--- |', f'| {len(repos)} | {stars} | {forks} |', '',
        '### Recently updated', '', 'Latest five by push date (UTC).', '', *rows]
path.write_text(old.split(start)[0] + '\n'.join([start, *rows, end]) + old.split(end)[1])
