"""Four portfolio charts drawn from repository metadata and public releases."""
from collections import Counter
from datetime import date, timedelta
from html import escape


def dashboard(repos, releases, today):
    start = today - timedelta(days=55)
    weeks = [0] * 8
    for items in releases.values():
        for item in items:
            day = date.fromisoformat(item[:10])
            if start <= day <= today:
                weeks[(day - start).days // 7] += 1
    counts = Counter({name: len(items) for name, items in releases.items()})
    licenses = Counter((r.get('license') or {}).get('spdx_id') or 'Not detected' for r in repos)
    if 'NOASSERTION' in licenses:
        licenses['Unclassified'] += licenses.pop('NOASSERTION')
    years = Counter(r['created_at'][:4] for r in repos)
    panels = [
        ('03', 'Release cadence', f'Eight 7-day periods ending {today} UTC', '#94e2d5'),
        ('04', 'Release archive', 'Published releases per project · highest five', '#fab387'),
        ('05', 'License signals', 'Repository count by GitHub license detection', '#b4befe'),
        ('06', 'Project origins', 'Tracked repositories by year created', '#f5c2e7'),
    ]
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 490" role="img" aria-labelledby="title"><title id="title">MoLik Labs · Release and portfolio observatory</title>']
    summaries = []
    for i, (number, title, subtitle, color) in enumerate(panels):
        x, y = (i % 2) * 424, (i // 2) * 249
        svg.append(f'<g transform="translate({x} {y})" font-family="system-ui,sans-serif" fill="#cdd6f4"><rect width="416" height="241" rx="16" fill="#1e1e2e"/><text x="20" y="35" font-size="20" font-weight="bold" fill="{color}">{number} / {title}</text><text x="20" y="62" font-size="14" fill="#bac2de">{subtitle}</text>')
        if i == 0:
            for j, n in enumerate(weeks):
                h = 90 * n / max(1, max(weeks))
                bx = 22 + j * 47
                svg.append(f'<rect x="{bx}" y="{183-h:.1f}" width="28" height="{h:.1f}" rx="3" fill="{color}"/><text x="{bx+14}" y="{175-h:.1f}" text-anchor="middle">{n}</text>')
            svg.append(f'<path d="M20 184h375" stroke="#585b70"/><text x="20" y="213" font-size="14">{start:%d %b}</text><text x="393" y="213" text-anchor="end" font-size="14">{today:%d %b}</text>')
            summaries.append('**Release cadence**, oldest week first: ' + ' · '.join(map(str, weeks)))
        else:
            if i == 1:
                rows = sorted(counts.items(), key=lambda t: (-t[1], t[0]))[:5]
            elif i == 2:
                rows = sorted(licenses.items(), key=lambda t: (-t[1], t[0]))
            else:
                rows = sorted(years.items(), reverse=True)
            if len(rows) > 5:
                rows = rows[:4] + [('Other', sum(n for _, n in rows[4:]))]
            peak = max([1] + [n for _, n in rows])
            for j, (label, n) in enumerate(rows):
                by = 98 + 29*j
                short = label if len(label) <= 20 else label[:18] + '…'
                svg.append(f'<text x="20" y="{by}" font-size="14">{escape(short)}</text><rect x="194" y="{by-9}" width="159" height="7" rx="3" fill="#45475a"/><rect x="194" y="{by-9}" width="{159*n/peak:.1f}" height="7" rx="3" fill="{color}"/><text x="391" y="{by}" text-anchor="end">{n}</text>')
            if not rows:
                svg.append('<text x="20" y="125">No tracked projects</text>')
            summaries.append(f'**{title}:** ' + (', '.join(f'{label}: {n}' for label,n in rows) or 'no data'))
        svg.append('</g>')
    return '\n'.join(svg + ['</svg>\n']), summaries
