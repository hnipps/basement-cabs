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

    def text_w(self, s, size):
        """Estimated rendered width in px (Menlo/Consolas are ~0.62 em wide)."""
        return len(str(s)) * size * 0.62

    def text(self, x, y, s, size=11, anchor="middle", color=LINE, rotate=0, weight="normal",
             dy=0, box=False):
        """Text at model point; size in px. rotate in degrees about the anchor.
        box=True paints a white rectangle behind the text so a line crossing it never
        strikes the label through (rotated by the same transform)."""
        px, py = self.X(x), self.Y(y) + dy
        tr = f" transform='rotate({rotate} {px:.1f} {py:.1f})'" if rotate else ""
        if box and str(s):
            w = self.text_w(s, size) + 4
            h = size * 1.25
            bx = {"start": px - 2, "end": px - w + 2}.get(anchor, px - w / 2)
            self.parts.append(
                f"<rect x='{bx:.1f}' y='{py - h / 2:.1f}' width='{w:.1f}' height='{h:.1f}' "
                f"fill='white' stroke='none'{tr}/>"
            )
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
    # A dimension is: two witness (extension) lines from the feature to the dimension
    # line, the line itself with 45-degree ticks at both ends, and the value. Text sits
    # along the line when it fits and steps outside one end when it does not, always on a
    # white box so nothing strikes it through.
    TICK = 4      # px, half-length of the 45-degree tick
    GAP = 2       # px, gap between the feature and the start of a witness line

    def _tick(self, px, py, color):
        t = self.TICK * 0.7071
        self.parts.append(
            f"<line x1='{px - t:.1f}' y1='{py + t:.1f}' x2='{px + t:.1f}' y2='{py - t:.1f}' "
            f"stroke='{color}' stroke-width='0.9'/>"
        )

    def _witness_px(self, ax, ay, bx, by, color):
        """Thin extension line between two pixel points, backed off GAP px from a."""
        dx, dy = bx - ax, by - ay
        n = (dx * dx + dy * dy) ** 0.5
        if n < self.GAP + 1:
            return
        ux, uy = dx / n, dy / n
        self.parts.append(
            f"<line x1='{ax + ux * self.GAP:.1f}' y1='{ay + uy * self.GAP:.1f}' "
            f"x2='{bx + ux * 2:.1f}' y2='{by + uy * 2:.1f}' stroke='{color}' stroke-width='0.6' opacity='0.8'/>"
        )

    def dim_h(self, x1, x2, y, text=None, offset_px=-14, size=10, color=DIM, ext=True,
              witness=None, fit="auto", box=True):
        """Horizontal dimension between model x1 and x2, drawn on the line at model y.

        witness: model y of the feature edge (one value, or (y_at_x1, y_at_x2)); a thin
                 extension line is drawn from there to the dimension line at each end.
        offset_px: text offset from the line; negative = above (screen up).
        fit: "auto" puts the text along the line when it fits, else just outside the
             right end; "along" / "right" / "left" force a placement.
        """
        t = frac(abs(x2 - x1)) if text is None else text
        self.line(x1, y, x2, y, stroke=color, sw=0.9)
        p1, p2, py = self.X(x1), self.X(x2), self.Y(y)
        if ext:
            for px in (p1, p2):
                self._tick(px, py, color)
        if witness is not None:
            w1, w2 = witness if isinstance(witness, (tuple, list)) else (witness, witness)
            self._witness_px(p1, self.Y(w1), p1, py, color)
            self._witness_px(p2, self.Y(w2), p2, py, color)
        if not t:
            return
        span = abs(p2 - p1)
        place = fit
        if fit == "auto":
            place = "along" if self.text_w(t, size) + 6 <= span else "right"
        if place == "along":
            self.text((x1 + x2) / 2, y, t, size=size, color=color, dy=offset_px, box=box)
        else:
            px = max(p1, p2) + 6 if place == "right" else min(p1, p2) - 6
            anchor = "start" if place == "right" else "end"
            self._text_px(px, py, t, size, anchor, color, box=box)

    def dim_v(self, y1, y2, x, text=None, offset_px=-12, size=10, color=DIM, ext=True,
              rotate=-90, witness=None, fit="auto", box=True):
        """Vertical dimension between model y1 and y2, drawn on the line at model x.

        witness: model x of the feature edge (one value, or (x_at_y1, x_at_y2)).
        offset_px: text offset from the line; negative = left of it.
        fit: "auto" rotates the text along the line when it fits, else writes it
             horizontally beside the line's midpoint on the offset side; "along" /
             "beside" force a placement.
        """
        t = frac(abs(y2 - y1)) if text is None else text
        self.line(x, y1, x, y2, stroke=color, sw=0.9)
        px, q1, q2 = self.X(x), self.Y(y1), self.Y(y2)
        if ext:
            for py in (q1, q2):
                self._tick(px, py, color)
        if witness is not None:
            w1, w2 = witness if isinstance(witness, (tuple, list)) else (witness, witness)
            self._witness_px(self.X(w1), q1, px, q1, color)
            self._witness_px(self.X(w2), q2, px, q2, color)
        if not t:
            return
        span = abs(q2 - q1)
        place = fit
        if fit == "auto":
            place = "along" if self.text_w(t, size) + 6 <= span else "beside"
        pm = (q1 + q2) / 2
        if place == "along":
            self._text_px(px + offset_px, pm, t, size, "middle", color, rotate=rotate, box=box)
        else:
            anchor = "end" if offset_px < 0 else "start"
            self._text_px(px + (offset_px - 2 if offset_px < 0 else offset_px + 2), pm, t,
                          size, anchor, color, box=box)

    def _text_px(self, px, py, s, size, anchor, color, rotate=0, box=True):
        """Text placed by pixel coordinates (used by the dimension helpers)."""
        tr = f" transform='rotate({rotate} {px:.1f} {py:.1f})'" if rotate else ""
        if box and str(s):
            w = self.text_w(s, size) + 4
            h = size * 1.25
            bx = {"start": px - 2, "end": px - w + 2}.get(anchor, px - w / 2)
            self.parts.append(
                f"<rect x='{bx:.1f}' y='{py - h / 2:.1f}' width='{w:.1f}' height='{h:.1f}' "
                f"fill='white' stroke='none'{tr}/>"
            )
        self.parts.append(
            f"<text x='{px:.1f}' y='{py:.1f}' font-size='{size}' text-anchor='{anchor}' fill='{color}' "
            f"dominant-baseline='middle' {FONT}{tr}>{escape(str(s))}</text>"
        )

    def leader(self, x1, y1, x2, y2, color="#777", dot=True):
        """Leader from a feature point (x1, y1) to a label anchor (x2, y2); dot on the feature."""
        self.line(x1, y1, x2, y2, stroke=color, sw=0.7)
        if dot:
            self.circle(x1, y1, 1.6, fill=color)

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
