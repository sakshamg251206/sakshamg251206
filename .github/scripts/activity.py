"""Render assets for the profile README from live GitHub data.

Writes dist/activity.svg: the last year's contribution calendar, a few live
numbers and the language mix across public, non-fork repositories.
Needs GITHUB_TOKEN; pass --demo to render with sample data instead.
"""
import datetime as dt
import json
import os
import random
import sys
import urllib.request

LOGIN = os.environ.get("PROFILE_LOGIN", "sakshamg251206")
OUT = os.environ.get("OUT_DIR", "dist")
SKIP_LANGS = {"Jupyter Notebook", "HTML", "CSS", "SCSS", "Makefile", "Dockerfile", "Procfile", "TeX", "Shell"}

SANS = "'Segoe UI', -apple-system, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
G, CARD, LINE, FG, SUB, MUT = "#39d98a", "#0d1117", "#1d2a24", "#e8f0ec", "#9aa7a1", "#5f6e67"
LEVELS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d98a"]

QUERY = """
query($login: String!) {
  user(login: $login) {
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes { languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } } }
    }
    contributionsCollection {
      contributionCalendar { totalContributions weeks { contributionDays { contributionCount date } } }
    }
  }
}"""


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": "bearer " + os.environ["GITHUB_TOKEN"], "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.load(r)
    if "errors" in body:
        sys.exit("GraphQL error: " + json.dumps(body["errors"]))
    u = body["data"]["user"]
    weeks = [[(d["date"], d["contributionCount"]) for d in w["contributionDays"]]
             for w in u["contributionsCollection"]["contributionCalendar"]["weeks"]]
    langs = {}
    for repo in u["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            name = e["node"]["name"]
            if name in SKIP_LANGS:
                continue
            size, color = langs.get(name, (0, e["node"]["color"] or "#8b949e"))
            langs[name] = (size + e["size"], color)
    return {
        "weeks": weeks,
        "total": u["contributionsCollection"]["contributionCalendar"]["totalContributions"],
        "repos": u["repositories"]["totalCount"],
        "langs": langs,
    }


def demo():
    rnd = random.Random(1)
    start = dt.date.today() - dt.timedelta(days=364)
    start -= dt.timedelta(days=(start.weekday() + 1) % 7)
    days = [(start + dt.timedelta(days=i)).isoformat() for i in range((dt.date.today() - start).days + 1)]
    counts = [max(0, int(rnd.gauss(3, 4))) for _ in days]
    weeks = [list(zip(days[i:i + 7], counts[i:i + 7])) for i in range(0, len(days), 7)]
    langs = {"Python": (900, "#3572A5"), "TypeScript": (300, "#3178c6"), "C++": (160, "#f34b7d"),
             "JavaScript": (120, "#f1e05a"), "Shell": (20, "#89e051")}
    return {"weeks": weeks, "total": sum(counts), "repos": 17, "langs": langs}


def streaks(weeks):
    days = [c for w in weeks for _, c in w]
    best = cur = 0
    for c in days:
        cur = cur + 1 if c else 0
        best = max(best, cur)
    # current streak: allow today to be empty without breaking it
    cur, tail = 0, days[:-1] if days and days[-1] == 0 else days
    for c in reversed(tail):
        if not c:
            break
        cur += 1
    return cur, best


def streak_tile(weeks, best):
    """Longest streak once it is worth showing, otherwise the number of active days."""
    if best >= 7:
        return f"{best} days", "longest streak"
    active = sum(1 for w in weeks for _, c in w if c)
    return str(active), "active days / yr"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(d):
    weeks = d["weeks"][-53:]
    # start the calendar at the first active week so long idle stretches are not shown,
    # then size the cells so the grid always fills the same width
    first = next((i for i, w in enumerate(weeks) if any(c for _, c in w)), 0)
    weeks = weeks[max(0, first - 1):]
    pitch = max(14, min(24, 900 // max(len(weeks), 1)))
    cell, x0, y0 = pitch - 3, 58, 104
    grid_h = 7 * pitch
    W, H = 1280, y0 + grid_h + 136
    b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="{CARD}" stroke="{LINE}" stroke-width="2"/>',
         f'<text x="30" y="46" font-family="{SANS}" font-size="20" font-weight="600" fill="{FG}">Contribution Activity</text>',
         f'<text x="30" y="72" font-family="{MONO}" font-size="14" fill="{SUB}">{d["total"]:,} contributions in the last year</text>']
    nonzero = sorted(c for w in weeks for _, c in w if c)
    q = [nonzero[int(len(nonzero) * p)] for p in (0.25, 0.5, 0.75)] if nonzero else [1, 2, 3]

    def level(c):
        return 0 if not c else 1 + sum(c > t for t in q)

    months_seen = set()
    for wi, week in enumerate(weeks):
        x = x0 + wi * pitch
        for date, c in week:
            day = dt.date.fromisoformat(date)
            wd = (day.weekday() + 1) % 7
            b.append(f'<rect x="{x}" y="{y0 + wd*pitch}" width="{cell}" height="{cell}" rx="3" fill="{LEVELS[level(c)]}"/>')
            if day.day <= 7 and wd == 0 and (day.year, day.month) not in months_seen:
                months_seen.add((day.year, day.month))
                b.append(f'<text x="{x}" y="{y0-10}" font-family="{MONO}" font-size="12" fill="{MUT}">{day.strftime("%b")}</text>')
    for i, lab in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        b.append(f'<text x="{x0-10}" y="{y0 + i*pitch + cell/2 + 4:.0f}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{MUT}">{lab}</text>')
    gy = y0 + grid_h + 8
    lx = x0 + len(weeks) * pitch - 3 - 5 * 17 - 76
    b.append(f'<text x="{lx}" y="{gy+11}" font-family="{MONO}" font-size="12" fill="{MUT}">Less</text>')
    for i, col in enumerate(LEVELS):
        b.append(f'<rect x="{lx + 38 + i*17}" y="{gy}" width="14" height="14" rx="3" fill="{col}"/>')
    b.append(f'<text x="{lx + 38 + 5*17 + 4}" y="{gy+11}" font-family="{MONO}" font-size="12" fill="{MUT}">More</text>')

    # live numbers
    _, best = streaks(weeks)
    sx, th = 990, 60
    tiles = [(f'{d["total"]:,}', "contributions / yr"), (str(d["repos"]), "public repositories"), streak_tile(weeks, best)]
    step = (grid_h + 40 - th) / 2
    for i, (v, lab) in enumerate(tiles):
        y = y0 - 18 + i * step
        b.append(f'<rect x="{sx}" y="{y:.0f}" width="262" height="{th}" rx="12" fill="#0a0f0d" stroke="{G}" stroke-opacity="0.4"/>')
        b.append(f'<text x="{sx+18}" y="{y+39:.0f}" font-family="{SANS}" font-size="26" font-weight="700" fill="{G}">{esc(v)}</text>')
        b.append(f'<text x="{sx+244}" y="{y+37:.0f}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{SUB}">{esc(lab)}</text>')

    # language mix
    total = sum(s for s, _ in d["langs"].values()) or 1
    top = [kv for kv in sorted(d["langs"].items(), key=lambda kv: -kv[1][0])[:6] if kv[1][0] / total >= 0.01]
    bx, by, bw = 30, gy + 62, 1222
    b.append(f'<text x="{bx}" y="{by-14}" font-family="{MONO}" font-size="13" fill="{SUB}">languages across public repos</text>')
    b.append(f'<clipPath id="bar"><rect x="{bx}" y="{by}" width="{bw}" height="12" rx="6"/></clipPath><g clip-path="url(#bar)">')
    x = bx
    shown = sum(s for _, (s, _) in top) or 1
    for name, (size, color) in top:
        w = bw * size / shown
        b.append(f'<rect x="{x:.1f}" y="{by}" width="{w+1:.1f}" height="12" fill="{color}"/>')
        x += w
    b.append("</g>")
    x = bx
    for name, (size, color) in top:
        label = f"{name} {100*size/total:.0f}%"
        b.append(f'<circle cx="{x+5}" cy="{by+33}" r="5" fill="{color}"/>')
        b.append(f'<text x="{x+16}" y="{by+38}" font-family="{SANS}" font-size="14" fill="{FG}">{esc(label)}</text>')
        x += 30 + len(label) * 7.6
    b.append(f'<text x="{W-28}" y="{by+38}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MUT}">updated {dt.date.today().isoformat()}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="Contribution activity"><title>Contribution activity</title>{"".join(b)}</svg>\n')


if __name__ == "__main__":
    data = demo() if "--demo" in sys.argv else fetch()
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "activity.svg"), "w") as f:
        f.write(render(data))
    print("wrote", os.path.join(OUT, "activity.svg"), "total", data["total"], "repos", data["repos"])
