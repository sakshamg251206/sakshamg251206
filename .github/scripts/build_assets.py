"""Generates the static SVG panels for the profile README into assets/.

icons.json holds logo paths and colours from the simple-icons package (CC0).
"""
import json, math, os, random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets")
ICONS = json.load(open(os.path.join(os.path.dirname(__file__), "icons.json")))
os.makedirs(OUT, exist_ok=True)

SANS = "'Segoe UI', -apple-system, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
G = "#39d98a"        # neon green accent
G2 = "#22c55e"
BG = "#07090c"
CARD = "#0d1117"
LINE = "#1d2a24"
FG = "#e8f0ec"
SUB = "#9aa7a1"
MUT = "#5f6e67"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w, h, body, title, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title><defs>{defs}</defs>{body}</svg>\n')


def write(name, s):
    open(os.path.join(OUT, name), "w").write(s)


def icon(key, x, y, size, color=None):
    i = ICONS[key]
    c = color or "#" + i["hex"]
    k = size / 24
    return f'<g transform="translate({x},{y}) scale({k:.4f})"><path d="{i["path"]}" fill="{c}"/></g>'


# Logos that are too dark to read on a near-black background are drawn in white.
DARK_LOGOS = {"pandas", "numpy", "nextdotjs", "github", "cmake"}


def logo(key, x, y, size):
    return icon(key, x, y, size, "#e8f0ec" if key in DARK_LOGOS else None)


def frame(w, h, label=None, glyph=None):
    """Rounded dark panel with a thin green-tinted border and an optional header label."""
    out = [f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="{CARD}" stroke="{LINE}" stroke-width="2"/>']
    if label:
        out.append(f'<rect x="28" y="28" width="16" height="16" rx="4" fill="{G}" fill-opacity="0.18" stroke="{G}" stroke-width="1.5"/>')
        if glyph:
            out.append(glyph)
        out.append(f'<text x="56" y="42" font-family="{SANS}" font-size="20" font-weight="600" fill="{FG}">{esc(label)}</text>')
    return "".join(out)


# --------------------------------------------------------------------------- hero
def hero():
    W, H = 1280, 720
    rnd = random.Random(7)
    d = f'''
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#05060f"/><stop offset="0.45" stop-color="#1a1440"/>
  <stop offset="0.72" stop-color="#4a2a78"/><stop offset="0.8" stop-color="#7a4a9a"/></linearGradient>
<linearGradient id="lake" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#3a2466"/><stop offset="0.5" stop-color="#140f2e"/><stop offset="1" stop-color="#05060d"/></linearGradient>
<radialGradient id="planet" cx="0.38" cy="0.32" r="0.75">
  <stop offset="0" stop-color="#cfe0ff"/><stop offset="0.45" stop-color="#7d8fd6"/><stop offset="0.8" stop-color="#3a3f8f"/><stop offset="1" stop-color="#1c1a4d"/></radialGradient>
<radialGradient id="halo" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0.55" stop-color="#9fb4ff" stop-opacity="0.35"/><stop offset="1" stop-color="#9fb4ff" stop-opacity="0"/></radialGradient>
<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="{G}" stop-opacity="0.75"/><stop offset="1" stop-color="{G}" stop-opacity="0"/></radialGradient>
<linearGradient id="veil" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{BG}" stop-opacity="0.95"/><stop offset="0.36" stop-color="{BG}" stop-opacity="0.78"/>
  <stop offset="0.55" stop-color="{BG}" stop-opacity="0"/></linearGradient>
<linearGradient id="bottomfade" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0.7" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}" stop-opacity="0.75"/></linearGradient>
<clipPath id="clip"><rect x="0" y="0" width="{W}" height="{H}" rx="22"/></clipPath>
<filter id="blur"><feGaussianBlur stdDeviation="2.2"/></filter>
<filter id="soft"><feGaussianBlur stdDeviation="8"/></filter>
'''
    b = [f'<g clip-path="url(#clip)">', f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    # stars
    for _ in range(170):
        x, y = rnd.uniform(0, W), rnd.uniform(0, 400)
        r = rnd.choice([0.6, 0.8, 1.0, 1.3, 1.7])
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" fill-opacity="{rnd.uniform(0.35, 0.95):.2f}"/>')
    # planet with ring
    px, py, pr = 860, 200, 150
    b.append(f'<circle cx="{px}" cy="{py}" r="{pr+70}" fill="url(#halo)"/>')
    b.append(f'<circle cx="{px}" cy="{py}" r="{pr}" fill="url(#planet)"/>')
    for i in range(7):
        b.append(f'<path d="M{px-pr+20} {py-60+i*22} q{pr} {18+i*3} {2*pr-40} {-6+i*2}" stroke="#ffffff" stroke-opacity="0.07" stroke-width="5" fill="none"/>')
    b.append(f'<ellipse cx="{px}" cy="{py+15}" rx="{pr+95}" ry="26" fill="none" stroke="#c9d6ff" stroke-opacity="0.55" stroke-width="3" transform="rotate(-12 {px} {py})"/>')
    b.append(f'<path d="M{px-pr} {py+40} a{pr} {pr} 0 0 0 {2*pr} 0" fill="#1c1a4d" fill-opacity="0.25"/>')
    # candlestick constellation drifting across the sky (decorative)
    cx, base = 470, 300
    rnd2 = random.Random(3)
    lvl = 0
    for i in range(26):
        o = lvl
        lvl += rnd2.uniform(-9, 11)
        hi, lo = max(o, lvl) + rnd2.uniform(2, 9), min(o, lvl) - rnd2.uniform(2, 9)
        x = cx + i * 15
        col = G if lvl >= o else "#ff5d73"
        b.append(f'<line x1="{x}" y1="{base-hi:.1f}" x2="{x}" y2="{base-lo:.1f}" stroke="{col}" stroke-opacity="0.35" stroke-width="1.2"/>')
        b.append(f'<rect x="{x-4}" y="{base-max(o,lvl):.1f}" width="8" height="{max(abs(lvl-o),1.5):.1f}" fill="{col}" fill-opacity="0.35"/>')
    # mountains
    def ridge(seed, y0, amp, color, op=1.0):
        r = random.Random(seed)
        pts = [(0, y0)]
        x = 0
        while x < W:
            x += r.uniform(40, 110)
            pts.append((x, y0 - r.uniform(0, amp)))
        path = "M0 470 " + " ".join(f"L{x:.0f} {y:.0f}" for x, y in pts) + f" L{W} 470 Z"
        return f'<path d="{path}" fill="{color}" fill-opacity="{op}"/>'
    b.append(ridge(11, 440, 120, "#2a1f5c", 0.9))
    b.append(ridge(5, 455, 80, "#1a1440"))
    b.append(ridge(9, 466, 36, "#100c28"))
    # far-shore city lights
    for i in range(60):
        x = 560 + rnd.uniform(0, 520)
        b.append(f'<rect x="{x:.0f}" y="{rnd.uniform(452, 466):.0f}" width="2" height="2" fill="{rnd.choice(["#ffd27a", "#9fd8ff", G])}" fill-opacity="0.8"/>')
    # lake + reflections
    b.append(f'<rect x="0" y="468" width="{W}" height="{H-468}" fill="url(#lake)"/>')
    for i in range(18):
        y = 476 + i * 9
        w = 120 - i * 5
        b.append(f'<rect x="{px - w/2 + rnd.uniform(-8, 8):.0f}" y="{y}" width="{max(w, 10):.0f}" height="2.5" rx="1" fill="#c9d6ff" fill-opacity="{0.45 - i*0.022:.2f}"/>')
    for i in range(40):
        x, y = rnd.uniform(0, W), rnd.uniform(480, 640)
        b.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{rnd.uniform(10, 50):.0f}" height="1.2" fill="#b9a6ff" fill-opacity="0.12"/>')
    # foreground rock + sitting figure with glowing laptop
    b.append(f'<path d="M650 720 C690 610 750 585 830 580 C910 575 990 600 1050 640 C1090 668 1120 700 1130 720 Z" fill="#05050c"/>')
    fx, fy = 880, 588   # seat point
    b.append(f'<g transform="translate({fx} {fy}) scale(1.35) translate({-fx} {-fy})">')
    b.append(f'<ellipse cx="{fx+6}" cy="{fy-40}" rx="70" ry="60" fill="url(#glow)" filter="url(#soft)" opacity="0.6"/>')
    figure = (f'M{fx-48} {fy} C{fx-50} {fy-18} {fx-30} {fy-22} {fx-18} {fy-24} '      # legs to hip
              f'C{fx-26} {fy-50} {fx-22} {fy-78} {fx-6} {fy-92} '                       # back
              f'C{fx+8} {fy-100} {fx+22} {fy-96} {fx+28} {fy-82} '                     # shoulder
              f'C{fx+36} {fy-62} {fx+40} {fy-40} {fx+46} {fy-24} '                     # arm to laptop
              f'C{fx+56} {fy-20} {fx+60} {fy-8} {fx+52} {fy} Z')
    b.append(f'<path d="{figure}" fill="#030308"/>')
    b.append(f'<circle cx="{fx+6}" cy="{fy-110}" r="17" fill="#030308"/>')
    b.append(f'<path d="M{fx-12} {fy-122} q18 -16 34 2" stroke="#030308" stroke-width="8" fill="none"/>')
    b.append(f'<circle cx="{fx+2}" cy="{fy-70}" r="7" fill="{G}" fill-opacity="0.55" filter="url(#blur)"/>')
    b.append(f'<path d="M{fx+30} {fy-30} l34 -6 l-6 26 l-34 4 Z" fill="{G}" fill-opacity="0.85"/>')
    b.append(f'<path d="M{fx+30} {fy-30} l34 -6 l-6 26 l-34 4 Z" fill="{G}" filter="url(#soft)" opacity="0.8"/>')
    b.append(f'<path d="{figure}" fill="none" stroke="#8f7cff" stroke-opacity="0.55" stroke-width="1.4"/>')
    b.append('</g>')
    b.append(f'<path d="M650 720 C690 610 750 585 830 580 C910 575 990 600 1050 640 C1090 668 1120 700 1130 720" fill="none" stroke="#8f7cff" stroke-opacity="0.45" stroke-width="2"/>')
    b.append(f'<rect width="{W}" height="{H}" fill="url(#bottomfade)"/>')
    b.append(f'<rect width="{W}" height="{H}" fill="url(#veil)"/>')
    b.append('</g>')

    # ---- window chrome
    b.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="22" fill="none" stroke="#2b3a33" stroke-width="2"/>')
    for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        b.append(f'<circle cx="{34+i*22}" cy="32" r="7" fill="{c}"/>')
    b.append(icon("github", 112, 22, 20, "#cfd8d3"))
    b.append(f'<text x="142" y="38" font-family="{MONO}" font-size="16" fill="#cfd8d3">sakshamg251206 / README.md</text>')

    # ---- identity block
    x0 = 64
    b.append(f'<text x="{x0}" y="130" font-family="{MONO}" font-size="17" letter-spacing="3" fill="{G}">QUANT RESEARCH · ML · SYSTEMS</text>')
    b.append(f'<text x="{x0-3}" y="208" font-family="{SANS}" font-size="78" font-weight="800" letter-spacing="2" fill="{FG}">SAKSHAM</text>')
    b.append(f'<text x="{x0-3}" y="286" font-family="{SANS}" font-size="78" font-weight="800" letter-spacing="2" fill="{G}">GARG</text>')
    b.append(f'<text x="{x0}" y="330" font-family="{SANS}" font-size="22" fill="#c7d2cc">Quant Research · Machine Learning · Systematic Trading</text>')
    b.append(f'<text x="{x0}" y="358" font-family="{SANS}" font-size="22" fill="#c7d2cc">Software Engineering · C++20 / Python</text>')
    # status pills
    pills = [("Researching", "order flow", "#a78bfa"), ("Building", "C++20 engines", "#60a5fa"), ("Shipping", "ML systems", G)]
    x = x0
    for name, what, col in pills:
        label = f"{name} · {what}"
        w = 42 + len(label) * 9.1
        b.append(f'<rect x="{x}" y="384" width="{w:.0f}" height="32" rx="16" fill="{col}" fill-opacity="0.12" stroke="{col}" stroke-opacity="0.6"/>')
        b.append(f'<circle cx="{x+16}" cy="400" r="5" fill="{col}"/>')
        b.append(f'<text x="{x+28}" y="405" font-family="{MONO}" font-size="15" fill="{FG}">{esc(label)}</text>')
        x += w + 10
    # motto
    b.append(f'<text x="{x0}" y="462" font-family="{MONO}" font-size="17" font-style="italic" fill="#b9c4be">"Out of sample, or it didn\'t happen."</text>')
    # stat tiles
    stats = [("Gold", "WorldQuant BRAIN"), ("1610", "Codeforces Expert"), ("1.58M", "Nasdaq events"), ("14", "open-source projects")]
    x = x0
    for v, l in stats:
        w = 178
        b.append(f'<rect x="{x}" y="500" width="{w}" height="86" rx="12" fill="#0b1210" fill-opacity="0.85" stroke="{G}" stroke-opacity="0.45"/>')
        b.append(f'<text x="{x+18}" y="542" font-family="{SANS}" font-size="32" font-weight="700" fill="{G}">{esc(v)}</text>')
        b.append(f'<text x="{x+18}" y="568" font-family="{SANS}" font-size="14" fill="{SUB}">{esc(l)}</text>')
        x += w + 12

    # ---- right-hand thumbnails (real numbers only)
    tx, tw, th = 1012, 236, 150
    def thumb(y, title):
        return (f'<rect x="{tx}" y="{y}" width="{tw}" height="{th}" rx="12" fill="#090c14" fill-opacity="0.88" stroke="#6d5bd0" stroke-opacity="0.7" stroke-width="1.5"/>'
                f'<text x="{tx+14}" y="{y+24}" font-family="{MONO}" font-size="13" fill="{SUB}">{esc(title)}</text>')
    # 1: order book ladder
    y = 76
    b.append(thumb(y, "L2 book · live depth"))
    asks, bids = [30, 46, 38, 62, 52], [70, 50, 60, 40, 28]
    for i, s in enumerate(asks):
        b.append(f'<rect x="{tx+60}" y="{y+36+i*11}" width="{s*1.9:.0f}" height="8" rx="2" fill="#ff5d73" fill-opacity="{0.35+i*0.12:.2f}"/>')
    b.append(f'<line x1="{tx+14}" y1="{y+94}" x2="{tx+tw-14}" y2="{y+94}" stroke="{G}" stroke-dasharray="3 3"/>')
    for i, s in enumerate(bids):
        b.append(f'<rect x="{tx+60}" y="{y+99+i*9.5:.1f}" width="{s*1.9:.0f}" height="7" rx="2" fill="{G}" fill-opacity="{0.9-i*0.13:.2f}"/>')
    b.append(f'<text x="{tx+16}" y="{y+98}" font-family="{MONO}" font-size="11" fill="{G}">mid</text>')
    # 2: ShadowFill fill-rate bars (real H1 numbers)
    y = 76 + th + 18
    b.append(thumb(y, "ShadowFill · fill @ 60 s"))
    for i, (v, lab, col) in enumerate([(43.3, "truth", G), (16.4, "model", "#ff8a4c")]):
        bw = v / 45 * 118
        yy = y + 52 + i * 44
        b.append(f'<text x="{tx+16}" y="{yy+14}" font-family="{MONO}" font-size="12" fill="{SUB}">{lab}</text>')
        b.append(f'<rect x="{tx+66}" y="{yy}" width="{bw:.0f}" height="20" rx="4" fill="{col}" fill-opacity="0.85"/>')
        b.append(f'<text x="{tx+72+bw:.0f}" y="{yy+15}" font-family="{SANS}" font-size="14" font-weight="700" fill="{FG}">{v}%</text>')
    # 3: terminal with real run numbers
    y = 76 + 2 * (th + 18)
    b.append(thumb(y, "~/shadowfill $"))
    lines = [("$ replay AAPL 2019-12-30", G), ("events   1,581,219", FG), ("orders     791,477", FG), ("engine   C++20 ✓ parity", "#60a5fa"), ("CI 95%  excludes 0", "#a78bfa")]
    for i, (t, c) in enumerate(lines):
        b.append(f'<text x="{tx+16}" y="{y+50+i*20}" font-family="{MONO}" font-size="13" fill="{c}">{esc(t)}</text>')

    # bottom tagline pill
    b.append(f'<rect x="{W-372}" y="{H-70}" width="340" height="40" rx="20" fill="{BG}" fill-opacity="0.8" stroke="{G}" stroke-width="1.5"/>')
    b.append(f'<path d="M{W-346} {H-50} l5 -11 l5 11 l-12 -7 h14 Z" fill="{G}"/>')
    b.append(f'<text x="{W-320}" y="{H-44}" font-family="{MONO}" font-size="16" fill="{FG}">Research. Build. Ship.</text>')
    write("hero.svg", svg(W, H, "".join(b), "Saksham Garg: Quant Research, Machine Learning, Systematic Trading, Software Engineering", d))


# --------------------------------------------------------------------------- tech stack
def stack():
    W, H = 1280, 300
    groups = [
        ("python", "Python"), ("cplusplus", "C++20"), ("typescript", "TypeScript"), ("pytorch", "PyTorch"),
        ("scikitlearn", "scikit-learn"), ("pandas", "pandas"), ("numpy", "NumPy"), ("qiskit", "Qiskit"),
        ("fastapi", "FastAPI"), ("docker", "Docker"), ("nextdotjs", "Next.js"), ("react", "React"),
        ("apacheparquet", "Parquet"), ("langchain", "LangGraph"), ("githubactions", "CI"), ("linux", "Linux"),
    ]
    b = [frame(W, H, "Tech Stack", f'<path d="M31 36 h10 M36 31 v10" stroke="{G}" stroke-width="2"/>')]
    b.append(f'<text x="{W-28}" y="42" text-anchor="end" font-family="{MONO}" font-size="14" fill="{MUT}">quant · ml · systems</text>')
    cols, tw, th, gx, gy = 8, 140, 100, 12, 14
    x0 = (W - (cols * tw + (cols - 1) * gx)) / 2
    for i, (k, name) in enumerate(groups):
        r, c = divmod(i, cols)
        x, y = x0 + c * (tw + gx), 70 + r * (th + gy)
        b.append(f'<rect x="{x:.0f}" y="{y}" width="{tw}" height="{th}" rx="12" fill="#0a0f0d" stroke="{LINE}" stroke-width="1.5"/>')
        b.append(logo(k, x + tw / 2 - 18, y + 16, 36))
        b.append(f'<text x="{x + tw/2:.0f}" y="{y+82}" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="600" fill="{FG}">{esc(name)}</text>')
    write("stack.svg", svg(W, H, "".join(b), "Tech stack: Python, C++20, TypeScript, PyTorch, scikit-learn, pandas, NumPy, Qiskit, FastAPI, Docker, Next.js, React, Parquet, LangGraph, CI, Linux"))


# --------------------------------------------------------------------------- project cards
def ring(cx, cy, r, pct, big, small, col=G):
    c = 2 * math.pi * r
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINE}" stroke-width="9"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="9" stroke-linecap="round" '
            f'stroke-dasharray="{c*pct:.1f} {c:.1f}" transform="rotate(-90 {cx} {cy})"/>'
            f'<text x="{cx}" y="{cy+7}" text-anchor="middle" font-family="{SANS}" font-size="22" font-weight="700" fill="{FG}">{esc(big)}</text>'
            f'<text x="{cx}" y="{cy+r+26}" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{SUB}">{esc(small)}</text>')


def wrap(text, n):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    return lines + [cur]


def card(fname, tag, title, desc, chips, metric, accent=G):
    W, H = 620, 250
    b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="{CARD}" stroke="{LINE}" stroke-width="2"/>',
         f'<rect x="1" y="1" width="6" height="{H-2}" rx="3" fill="{accent}"/>',
         f'<text x="30" y="40" font-family="{MONO}" font-size="15" letter-spacing="1.5" fill="{accent}">{esc(tag)}</text>',
         f'<text x="30" y="78" font-family="{SANS}" font-size="28" font-weight="700" fill="{FG}">{esc(title)}</text>']
    for i, line in enumerate(wrap(desc, 40)[:3]):
        b.append(f'<text x="30" y="{112 + i*26}" font-family="{SANS}" font-size="19" fill="{SUB}">{esc(line)}</text>')
    x = 30
    for ch in chips:
        w = 20 + len(ch) * 8.4
        b.append(f'<rect x="{x}" y="{H-50}" width="{w:.0f}" height="28" rx="14" fill="{accent}" fill-opacity="0.1" stroke="{accent}" stroke-opacity="0.45"/>')
        b.append(f'<text x="{x+9}" y="{H-31}" font-family="{MONO}" font-size="14" fill="{FG}">{esc(ch)}</text>')
        x += w + 8
    kind = metric[0]
    if kind == "ring":
        _, pct, big, small = metric
        b.append(ring(W - 88, 100, 50, pct, big, small, accent))
    else:
        _, big, small = metric
        b.append(f'<text x="{W-88}" y="112" text-anchor="middle" font-family="{SANS}" font-size="40" font-weight="800" fill="{accent}">{esc(big)}</text>')
        b.append(f'<text x="{W-88}" y="142" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{SUB}">{esc(small)}</text>')
    write(fname, svg(W, H, "".join(b), f"{title}: {desc}"))


CARDS = [
    ("card-shadowfill.svg", "MICROSTRUCTURE · EXECUTION", "ShadowFill",
     "Computes exact passive-order fills from Nasdaq market-by-order data to grade the fill models backtests rely on.",
     ["C++20", "Python", "ITCH", "bootstrap"], ("ring", 0.433, "43%", "true fill @ 60 s"), G),
    ("card-ofi.svg", "ORDER FLOW · REPLICATION", "Order-Flow Imbalance",
     "Pre-registered replication of Cont, Kukanov & Stoikov (2014) on Binance BTC, ETH and WLD perpetuals.",
     ["statsmodels", "PyArrow", "pytest"], ("ring", 0.73, "0.73", "median R² explained"), "#60a5fa"),
    ("card-orderbook.svg", "HIGH-FREQUENCY ML · STREAMING", "Order Book ML",
     "Streams the Binance L2 book at 10 Hz into calibrated BUY / HOLD / SELL signals on a live dashboard.",
     ["CatBoost", "XGBoost", "SHAP", "WebSockets"], ("num", "31", "LOB features"), "#a78bfa"),
    ("card-alphalab.svg", "ALPHA RESEARCH · BACKTESTING", "Systematic Alpha Lab",
     "Five systematic strategies on 15 ETFs with execution lag, 15 bps costs and walk-forward and crisis tests.",
     ["pandas", "walk-forward", "Next.js"], ("num", "19y", "of daily data"), "#f59e0b"),
    ("card-entity.svg", "AMAZON ML CHALLENGE 2026", "Entity Resolver",
     "Business entity resolution across three noisy sources: TF-IDF blocking, 54 features and a stacked LightGBM matcher.",
     ["LightGBM", "MLP", "SHAP", "FastAPI"], ("ring", 0.9614, "0.96", "OOF macro F0.5"), G),
    ("card-qkd.svg", "QUANTUM · IIT JODHPUR", "Adaptive QKD",
     "BB84 simulator with an ML eavesdropper detector driving a keep / harden / abort policy against PNS attacks.",
     ["Qiskit", "PyTorch", "scikit-learn"], ("ring", 0.98, "0.98", "attack ROC-AUC"), "#60a5fa"),
    ("card-ragsentry.svg", "GENAI · SECURITY", "RagSentry",
     "Multi-agent auditor that attacks RAG chatbots for prompt injection, data leakage and hallucination.",
     ["LangGraph", "CrewAI", "FAISS"], ("num", "3", "auditor agents"), "#a78bfa"),
    ("card-spamshield.svg", "ML · NLP", "SpamShield",
     "Explainable spam and scam detection with a calibrated linear SVM that also ranks whole .mbox exports.",
     ["scikit-learn", "Streamlit", "mypy"], ("ring", 0.961, "96%", "spam recall"), "#f59e0b"),
]


# --------------------------------------------------------------------------- achievements
def achievements():
    W, H = 1280, 250
    b = [frame(W, H, "Track Record", f'<path d="M36 31 l2 4 4 .5 -3 3 .8 4 -3.8 -2 -3.8 2 .8 -4 -3 -3 4 -.5 Z" fill="{G}"/>')]
    items = [
        ("WorldQuant BRAIN", "Gold", "best alpha: Sharpe 1.72 · fitness 1.77", G),
        ("Codeforces", "Expert · 1610", "max rating", "#60a5fa"),
        ("Amazon ML Challenge", "0.9614", "out-of-fold macro F0.5", "#f59e0b"),
        ("IIT Jodhpur", "Research Intern", "quantum computing & cryptography", "#a78bfa"),
        ("Affy Pharma", "AI/ML Intern", "predictive models for QC data", G),
    ]
    n, gx = len(items), 14
    tw = (W - 56 - (n - 1) * gx) / n
    for i, (org, big, small, col) in enumerate(items):
        x = 28 + i * (tw + gx)
        b.append(f'<rect x="{x:.0f}" y="72" width="{tw:.0f}" height="150" rx="14" fill="#0a0f0d" stroke="{col}" stroke-opacity="0.5" stroke-width="1.5"/>')
        b.append(f'<circle cx="{x+24:.0f}" cy="102" r="6" fill="{col}"/>')
        b.append(f'<text x="{x+38:.0f}" y="107" font-family="{MONO}" font-size="13" fill="{SUB}">{esc(org)}</text>')
        fs = 30 if len(big) <= 8 else 22
        b.append(f'<text x="{x+20:.0f}" y="156" font-family="{SANS}" font-size="{fs}" font-weight="800" fill="{col}">{esc(big)}</text>')
        for j, line in enumerate(wrap(small, 24)[:2]):
            b.append(f'<text x="{x+20:.0f}" y="{186 + j*20}" font-family="{SANS}" font-size="14" fill="{SUB}">{esc(line)}</text>')
    write("achievements.svg", svg(W, H, "".join(b), "Track record: WorldQuant BRAIN Gold, Codeforces Expert 1610, Amazon ML Challenge 0.9614, IIT Jodhpur research intern, Affy Pharma AI/ML intern"))


# --------------------------------------------------------------------------- section headers & footer
def header(fname, text, sub):
    W, H = 1280, 84
    b = [f'<rect x="0" y="22" width="8" height="44" rx="3" fill="{G}"/>',
         f'<text x="26" y="58" font-family="{SANS}" font-size="34" font-weight="800" fill="{G2}">{esc(text)}</text>',
         f'<text x="{W}" y="58" text-anchor="end" font-family="{MONO}" font-size="16" fill="{MUT}">{esc(sub)}</text>',
         f'<line x1="26" y1="78" x2="{W}" y2="78" stroke="{G}" stroke-opacity="0.25" stroke-width="2"/>']
    write(fname, svg(W, H, "".join(b), text))


def footer():
    W, H = 1280, 90
    b = [f'<rect x="{W/2-230}" y="20" width="460" height="50" rx="25" fill="{CARD}" stroke="{G}" stroke-width="2"/>',
         f'<path d="M{W/2-200} 47 l6 -13 l6 13 l-15 -8 h18 Z" fill="{G}"/>',
         f'<text x="{W/2+14}" y="52" text-anchor="middle" font-family="{MONO}" font-size="20" fill="{FG}">Research. Quantify. Build. Ship.</text>']
    write("footer.svg", svg(W, H, "".join(b), "Research. Quantify. Build. Ship."))


def buttons():
    W, H = 210, 52
    items = [("btn-portfolio.svg", "Portfolio", None), ("btn-resume.svg", "Resume", None), ("btn-linkedin.svg", "LinkedIn", None),
             ("btn-email.svg", "Email", "gmail"), ("btn-codeforces.svg", "Codeforces", "codeforces")]
    for fname, label, ic in items:
        b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{CARD}" stroke="{G}" stroke-opacity="0.55" stroke-width="1.5"/>']
        if ic:
            b.append(logo(ic, 22, 15, 22))
        elif label == "LinkedIn":
            b.append(f'<rect x="22" y="15" width="22" height="22" rx="4" fill="#0a66c2"/><text x="33" y="32" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="800" fill="#fff">in</text>')
        elif label == "Resume":
            b.append(f'<path d="M25 13 h12 l6 6 v20 h-18 Z" fill="none" stroke="{G}" stroke-width="2"/><path d="M29 25 h10 M29 30 h10 M29 35 h6" stroke="{G}" stroke-width="2"/>')
        else:
            b.append(f'<circle cx="33" cy="26" r="10" fill="none" stroke="{G}" stroke-width="2"/><path d="M23 26 h20 M33 16 q-7 10 0 20 q7 -10 0 -20" fill="none" stroke="{G}" stroke-width="1.6"/>')
        b.append(f'<text x="{(56 + W - 14) / 2:.0f}" y="33" text-anchor="middle" font-family="{SANS}" font-size="18" font-weight="600" fill="{FG}">{label}</text>')
        write(fname, svg(W, H, "".join(b), label))


if __name__ == "__main__":
    buttons()
    hero(); stack(); achievements(); footer()
    for c in CARDS:
        card(*c)
    header("h-projects.svg", "Featured Projects", "quant research · ml · systems")
