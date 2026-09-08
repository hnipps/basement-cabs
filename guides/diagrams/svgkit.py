"""Tiny dependency-free SVG builder for the build-guide diagrams.

Coordinates are in inches; ``Canvas`` scales them to pixels. Y is down (screen
convention), so elevations pass ``flip_y=True`` to put Z up.

Style is fixed so every diagram in ``guides/diagrams`` reads the same:
black lines on white, one hatch per material, dimension text in a mono font.
"""
from fractions import Fraction
from html import escape

# One fill per material. Keep these in sync with the legend in the guides.
MAT = {
    "spruce58": "#e9d3a8",
    "spruce12": "#f2e2c2",
    "mdf58": "#c9b6a0",
    "mdf12": "#dccdbc",
    "hardboard": "#8b6a4a",
    "2x2": "#f0c070",
    "2x4": "#e0a850",
    "wall": "#d0d0d0",
    "floor": "#b8b8b8",
    "waste": "url(#waste)",
    "none": "none",
}
LINE = "#111"
DIM = "#c0392b"
FONT = "font-family='Menlo, Consolas, monospace'"


def frac(x, denom=64):
    """1.5 -> '1-1/2', 60.203125 -> '60-13/64', 17 -> '17'."""
    # Snap to the nearest 1/denom first; limit_denominator alone would happily
    # print 30.209 as 30-9/43.
    f = Fraction(round(x * denom), denom)
    whole, rem = divmod(f.numerator, f.denominator)
    if rem == 0:
        return str(whole)
    r = Fraction(rem, f.denominator)
    return f"{whole}-{r.numerator}/{r.denominator}" if whole else f"{r.numerator}/{r.denominator}"


class Canvas:
    def __init__(self, w_in, h_in, scale=6.0, margin=0.35, flip_y=False, title=""):
        self.s = scale
        self.m = margin
        self.w_in, self.h_in = w_in, h_in
        self.flip = flip_y
        self.parts = []
        self.title = title

    # --- coordinate mapping -------------------------------------------------
    def X(self, x):
        return (x + self.m) * self.s

    def Y(self, y):
        if self.flip:
            y = self.h_in - y
        return (y + self.m) * self.s

    # --- primitives -----------------------------------------------------------
    def rect(self, x, y, w, h, fill="none", stroke=LINE, sw=1.2, dash=None, opacity=1.0):
        """Axis-aligned box; (x, y) is the min corner in model space."""
        y0 = self.Y(y + h) if self.flip else self.Y(y)
        extra = f" stroke-dasharray='{dash}'" if dash else ""
        self.parts.append(
            f"<rect x='{self.X(x):.1f}' y='{y0:.1f}' width='{w*self.s:.1f}' height='{h*self.s:.1f}' "
            f"fill='{fill}' stroke='{stroke}' stroke-width='{sw}' opacity='{opacity}'{extra}/>"
        )

    def line(self, x1, y1, x2, y2, stroke=LINE, sw=1.0, dash=None):
        extra = f" stroke-dasharray='{dash}'" if dash else ""
        self.parts.append(
            f"<line x1='{self.X(x1):.1f}' y1='{self.Y(y1):.1f}' x2='{self.X(x2):.1f}' y2='{self.Y(y2):.1f}' "
            f"stroke='{stroke}' stroke-width='{sw}'{extra}/>"
        )

    def poly(self, pts, fill="none", stroke=LINE, sw=1.2):
        d = " ".join(f"{self.X(x):.1f},{self.Y(y):.1f}" for x, y in pts)
        self.parts.append(f"<polygon points='{d}' fill='{fill}' stroke='{stroke}' stroke-width='{sw}'/>")

    def circle(self, x, y, r_px, fill=LINE, stroke="none"):
        self.parts.append(
            f"<circle cx='{self.X(x):.1f}' cy='{self.Y(y):.1f}' r='{r_px}' fill='{fill}' stroke='{stroke}'/>"
        )

    def text(self, x, y, s, size=11, anchor="middle", color=LINE, rotate=0, weight="normal", dy=0):
        """Text at model point; size in px. rotate in degrees about the anchor."""
        px, py = self.X(x), self.Y(y) + dy
        tr = f" transform='rotate({rotate} {px:.1f} {py:.1f})'" if rotate else ""
        self.parts.append(
            f"<text x='{px:.1f}' y='{py:.1f}' font-size='{size}' text-anchor='{anchor}' fill='{color}' "
            f"font-weight='{weight}' dominant-baseline='middle' {FONT}{tr}>{escape(str(s))}</text>"
        )

    def label(self, x, y, lines, size=10, anchor="middle", color=LINE, rotate=0):
        """Multi-line centred label at a model point. lines: str or list."""
        if isinstance(lines, str):
            lines = [lines]
        lh = size * 1.25
        off = -(len(lines) - 1) * lh / 2
        for i, s in enumerate(lines):
            self.text(x, y, s, size=size, anchor=anchor, color=color, rotate=rotate, dy=off + i * lh)

    # --- dimensions -----------------------------------------------------------
    def dim_h(self, x1, x2, y, text=None, offset_px=-14, size=10, color=DIM, ext=True):
        """Horizontal dimension between x1 and x2 drawn at model y. Text above."""
        t = frac(abs(x2 - x1)) if text is None else text
        self.line(x1, y, x2, y, stroke=color, sw=0.9)
        if ext:
            for x in (x1, x2):
                px, py = self.X(x), self.Y(y)
                self.parts.append(f"<line x1='{px:.1f}' y1='{py-4:.1f}' x2='{px:.1f}' y2='{py+4:.1f}' stroke='{color}' stroke-width='0.9'/>")
        self.text((x1 + x2) / 2, y, t, size=size, color=color, dy=offset_px)

    def dim_v(self, y1, y2, x, text=None, offset_px=-12, size=10, color=DIM, ext=True, rotate=-90):
        """Vertical dimension between y1 and y2 drawn at model x. Text rotated, left of line."""
        t = frac(abs(y2 - y1)) if text is None else text
        self.line(x, y1, x, y2, stroke=color, sw=0.9)
        if ext:
            for y in (y1, y2):
                px, py = self.X(x), self.Y(y)
                self.parts.append(f"<line x1='{px-4:.1f}' y1='{py:.1f}' x2='{px+4:.1f}' y2='{py:.1f}' stroke='{color}' stroke-width='0.9'/>")
        px, py = self.X(x) + offset_px, self.Y((y1 + y2) / 2)
        self.parts.append(
            f"<text x='{px:.1f}' y='{py:.1f}' font-size='{size}' text-anchor='middle' fill='{color}' "
            f"dominant-baseline='middle' {FONT} transform='rotate({rotate} {px:.1f} {py:.1f})'>{escape(t)}</text>"
        )

    def note(self, x, y, s, size=10, anchor="start", color=LINE):
        self.text(x, y, s, size=size, anchor=anchor, color=color)

    # --- output -----------------------------------------------------------------
    def svg(self):
        W = (self.w_in + 2 * self.m) * self.s
        H = (self.h_in + 2 * self.m) * self.s
        title = f"<title>{escape(self.title)}</title>" if self.title else ""
        defs = (
            "<defs><pattern id='waste' width='8' height='8' patternUnits='userSpaceOnUse' "
            "patternTransform='rotate(45)'><line x1='0' y1='0' x2='0' y2='8' stroke='#999' stroke-width='1'/></pattern></defs>"
        )
        body = "\n".join(self.parts)
        return (
            f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W:.0f} {H:.0f}' width='{W:.0f}' height='{H:.0f}'>"
            f"{title}{defs}<rect width='100%' height='100%' fill='white'/>\n{body}\n</svg>\n"
        )

    def save(self, path):
        with open(path, "w") as f:
            f.write(self.svg())
        return path
