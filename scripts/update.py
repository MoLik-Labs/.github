"""Refresh only the generated part of the organization profile."""
from datetime import datetime, timezone
from observatory import dashboard
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
releases = {}
for repo in repos:
    dates = subprocess.check_output([
        'gh', 'api', '--paginate', f"repos/{repo['full_name']}/releases?per_page=100",
        '--jq', '.[] | select(.draft == false) | .published_at // empty'
    ], text=True)
    releases[repo['name']] = dates.splitlines()
charts, chart_notes = dashboard(repos, releases, today)
(path.parent / 'assets/observatory.svg').write_text(charts)
feature = select(today)
issue = today.strftime('%Y.%m')
url = f'https://github.com/{org}/{feature.project}' + ('/' + feature.path if feature.path else '')
banner = Path(__file__).with_name('masthead.svg.in').read_text()
(path.parent / 'assets/masthead.svg').write_text(banner.replace('@EDITION@', issue)
    .replace('@TRACK@', feature.track.upper()).replace('@PROJECT@', feature.project)
    .replace('@ACCENT@', feature.accent))
svg, summary = render(repos, today)
(path.parent / 'assets/pulse.svg').write_text(svg)
rows = [f'> **Field notes · {issue}** — [{feature.project}]({url}) · {feature.copy}', '',
        f'![{summary}; project language counts](assets/pulse.svg)', '',
        f'**{summary}.** Each repository counts once. We use GitHub’s primary language except for ZMRIG, classified by its Zig miner core.', '',
        '![Release cadence, release archive, detected licenses and repository creation years](assets/observatory.svg)', '',
        '<details><summary>Chart data &amp; reading notes</summary>', '',
        *['- ' + note for note in chart_notes], '',
        'Release charts include published prereleases, not draft releases or bare tags. Creation year is the repository date, not the first upstream commit.', '', '</details>', '',
        '### Recently updated', '', 'Latest five by push date (UTC).', '', *rows]
path.write_text(old.split(start)[0] + '\n'.join([start, *rows, end]) + old.split(end)[1])
