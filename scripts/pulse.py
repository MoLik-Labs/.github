"""Render an organization activity ring and project-language distribution."""
from collections import Counter
from datetime import timedelta, date
from html import escape


def render(repos, today):
    cutoff = today - timedelta(days=29)
    active = sum(1 for r in repos if r['pushed_at'] and
                 cutoff <= date.fromisoformat(r['pushed_at'][:10]) <= today)
    total = len(repos)
    percent = round(100 * active / total) if total else 0
    languages = Counter(r['language'] or 'Unclassified' for r in repos)
    ranked = sorted(languages.items(), key=lambda item: (-item[1], item[0]))
    if len(ranked) > 4:
        ranked = ranked[:3] + [('Other', sum(n for _, n in ranked[3:]))]
    label = f'{active} of {total} repositories pushed in the last 30 UTC days'
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 226" role="img" aria-labelledby="title desc">
<title id="title">MoLik Labs · Activity report</title><desc id="desc">{label}. Project languages: {escape(', '.join(f'{name}: {n}' for name, n in ranked) or 'none')}.</desc>
<rect width="840" height="226" rx="16" fill="#1e1e2e"/>
<g font-family="system-ui,sans-serif" fill="#cdd6f4">
<text x="28" y="39" font-size="17" font-weight="bold" fill="#cba6f7">01 / Activity · 30 days</text>
<circle cx="97" cy="132" r="52" fill="none" stroke="#45475a" stroke-width="12"/>
<circle cx="97" cy="132" r="52" fill="none" stroke="#94e2d5" stroke-width="12" pathLength="100" stroke-dasharray="{percent} {100-percent}" transform="rotate(-90 97 132)"/>
<text x="97" y="140" text-anchor="middle" font-size="25" font-weight="bold">{percent if total else '—'}{'%' if total else ''}</text>
<text x="174" y="126" font-size="28">{active} / {total}</text><text x="174" y="154" font-size="16">repos with a push</text>
<path d="M388 26v174" stroke="#45475a"/><text x="416" y="39" font-size="17" font-weight="bold" fill="#cba6f7">02 / Project languages · repositories</text>''']
    for i, (name, count) in enumerate(ranked):
        y = 77 + 38*i
        color = ('#89b4fa', '#f5c2e7', '#fab387', '#b4befe')[i]
        parts.append(f'<text x="416" y="{y}">{escape(name)}</text><rect x="599" y="{y-10}" width="165" height="8" rx="4" fill="#45475a"/><rect x="599" y="{y-10}" width="{165*count/total:.2f}" height="8" rx="4" fill="{color}"/><text x="798" y="{y}" text-anchor="end">{count}</text>')
    return '\n'.join(parts + ['</g></svg>\n']), label
