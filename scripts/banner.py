"""Generate the profile banner as Catppuccin Mocha (dark) and Latte (light) SVGs.

Run from the repository root: ``python3 scripts/banner.py``.
GitHub serves README images through <img>, so the SVGs use only SMIL and
inline attributes: no scripts, no external fonts.
"""

from pathlib import Path

MOCHA = {
    "base": "#1e1e2e", "text": "#cdd6f4", "over": "#6c7086",
    "s0": "#313244", "mauve": "#cba6f7", "blue": "#89b4fa", "green": "#a6e3a1",
    "peach": "#fab387", "pink": "#f5c2e7", "teal": "#94e2d5", "yellow": "#f9e2af",
    "lav": "#b4befe", "sky": "#89dceb",
    "role": "#a6adc8", "t_green": "#a6e3a1", "t_mauve": "#cba6f7", "t_blue": "#89b4fa",
}
LATTE = {
    "base": "#eff1f5", "text": "#4c4f69", "over": "#9ca0b0",
    "s0": "#ccd0da", "mauve": "#8839ef", "blue": "#1e66f5", "green": "#40a02b",
    "peach": "#fe640b", "pink": "#ea76cb", "teal": "#179299", "yellow": "#df8e1d",
    "lav": "#7287fd", "sky": "#04a5e5",
    # Latte subtext0, green and blue fall below 4.5:1 as small text on base, so text uses darker shades.
    "role": "#5c5f77", "t_green": "#2f7a1f", "t_mauve": "#8839ef", "t_blue": "#1a5ad8",
}
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
W, H = 830, 224
CX, CY, R = 636, 112, 100

ICONS = {
    "microbe": '<rect x="-10" y="-4" width="14" height="8" rx="4"/><path d="M4 0 q2 -3.5 4 0 t4 0"/>'
    '<circle cx="-6" cy="0" r="0.9"/><circle cx="-1" cy="1" r="0.9"/>',
    "terminal": '<rect x="-10" y="-8" width="20" height="16" rx="3"/><path d="M-6 -2.5 l3.5 2.5 l-3.5 2.5 M0 3.5 h5"/>',
    "keyboard": '<rect x="-11.5" y="-5" width="9.5" height="10" rx="2" transform="rotate(-14 -6.75 0)"/>'
    '<rect x="2" y="-5" width="9.5" height="10" rx="2" transform="rotate(14 6.75 0)"/>'
    '<circle cx="-7.5" cy="-1" r="0.8"/><circle cx="-5" cy="1.5" r="0.8"/>'
    '<circle cx="7.5" cy="-1" r="0.8"/><circle cx="5" cy="1.5" r="0.8"/>',
    "code": '<path d="M-5 -6 l-6 6 l6 6 M5 -6 l6 6 l-6 6 M2 -8 l-4 16"/>',
    "pulse": '<path d="M-12 1 h5 l2.5 -7 l3.5 13 l2.5 -6 h3 l1.5 -2 h6"/>',
}
# Icon nodes as (name, offset from dish centre, accent).
NODES = [
    ("microbe", -54, -46, "green"),
    ("terminal", 44, -54, "blue"),
    ("keyboard", 66, 20, "mauve"),
    ("code", 4, 62, "peach"),
    ("pulse", -62, 30, "pink"),
]
HUB = (-4, -2)
COLONIES = [
    (22, -10, 5, "teal"), (-24, 4, 4, "yellow"), (34, 46, 3.5, "green"),
    (-30, -72, 3, "sky"), (70, -28, 3, "peach"), (-74, -6, 3, "lav"),
]
# The spark walks this closed loop; every hop must also be an edge.
LOOP = ["microbe", "hub", "terminal", "keyboard", "code", "pulse", "microbe"]
EXTRA_EDGES = [("hub", "code"), ("hub", "keyboard"), ("hub", "pulse")]
TAGS = [("microbial ecology", "t_green"), ("AI co-scientists", "t_mauve"), ("agent tooling", "t_blue")]


def pos(name: str) -> tuple[float, float]:
    """Return the absolute position of a node in the dish."""
    if name == "hub":
        return CX + HUB[0], CY + HUB[1]
    dx, dy = next((dx, dy) for n, dx, dy, _ in NODES if n == name)
    return CX + dx, CY + dy


def banner(p: dict[str, str]) -> str:
    """Build the banner SVG for one palette."""
    out = [
        f'<circle cx="{CX}" cy="{CY}" r="{R + 5}" fill="none" stroke="{p["s0"]}" stroke-width="2.5"/>',
        f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="{p["yellow"]}" fill-opacity="0.05"/>',
        f'<ellipse cx="{CX - 40}" cy="{CY - 60}" rx="28" ry="6" fill="{p["text"]}" opacity="0.05" '
        f'transform="rotate(-28 {CX - 40} {CY - 60})"/>',
    ]
    for k, (a, b) in enumerate(list(zip(LOOP, LOOP[1:])) + EXTRA_EDGES):
        (x1, y1), (x2, y2) = pos(a), pos(b)
        out.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{p["over"]}" stroke-width="1.2" opacity="0.35">'
            f'<animate attributeName="opacity" values="0.2;0.55;0.2" dur="{5 + k % 4}s" begin="-{k * 0.9:.1f}s" '
            'repeatCount="indefinite"/></line>'
        )
    for k, (dx, dy, r, c) in enumerate(COLONIES):
        x, y = CX + dx, CY + dy
        out.append(
            f'<circle cx="{x}" cy="{y}" r="{r * 2}" fill="{p[c]}" opacity="0.15">'
            f'<animate attributeName="r" values="{r * 1.6};{r * 2.6};{r * 1.6}" dur="{4 + k % 3}s" begin="-{k}s" '
            'repeatCount="indefinite"/></circle>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{p[c]}" opacity="0.85"/>'
        )
    hx, hy = pos("hub")
    out.append(f'<circle cx="{hx}" cy="{hy}" r="6" fill="{p["text"]}" opacity="0.7"/>')
    path = "M" + " L".join(f"{x} {y}" for x, y in map(pos, LOOP))
    out.append(
        f'<g><animateMotion path="{path}" dur="16s" repeatCount="indefinite"/>'
        f'<circle r="7" fill="{p["yellow"]}" opacity="0.25"/>'
        f'<path d="M0 -5 L1.3 -1.3 L5 0 L1.3 1.3 L0 5 L-1.3 1.3 L-5 0 L-1.3 -1.3 Z" fill="{p["yellow"]}"/></g>'
    )
    # Icons come after the spark so it passes underneath them.
    for k, (name, dx, dy, c) in enumerate(NODES):
        out.append(
            f'<g transform="translate({CX + dx} {CY + dy})"><g>'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -2.5;0 0" dur="{5 + k}s" '
            f'begin="-{k * 1.3:.1f}s" repeatCount="indefinite"/>'
            f'<circle r="23" fill="{p["base"]}" stroke="{p[c]}" stroke-width="1.4"/>'
            f'<g fill="none" stroke="{p[c]}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" '
            f'transform="scale(1.2)">{ICONS[name]}</g></g></g>'
        )
    sep = f'<tspan fill="{p["over"]}"> · </tspan>'
    tags = sep.join(f'<tspan fill="{p[c]}">{t}</tspan>' for t, c in TAGS)
    # The cursor is a glyph inside the text so the font positions it.
    cursor = (
        f'<tspan fill="{p["text"]}"> ▍<animate attributeName="fill-opacity" values="0.8;0" calcMode="discrete" '
        'dur="1.1s" repeatCount="indefinite"/></tspan>'
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Dileep Kishore, postdoc at Berkeley Lab">
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16" fill="{p['base']}" stroke="{p['s0']}"/>
  <text x="40" y="94" font-family="{SANS}" font-size="40" font-weight="700" fill="{p['text']}">Dileep Kishore</text>
  <text x="40" y="126" font-family="{SANS}" font-size="18" fill="{p['role']}">Postdoc at Berkeley Lab</text>
  <text x="40" y="164" font-family="{MONO}" font-size="13">{tags}{cursor}</text>
  {chr(10).join("  " + line for line in out).lstrip()}
</svg>
"""


def main() -> None:
    assets = Path(__file__).resolve().parent.parent / "assets"
    assets.mkdir(exist_ok=True)
    (assets / "banner-dark.svg").write_text(banner(MOCHA))
    (assets / "banner-light.svg").write_text(banner(LATTE))


if __name__ == "__main__":
    main()
