"""Diagrams for guide 4 (doors, hinges, shelf pins).

Two sheets, ported from the reference drawings A-1 (front elevation, doors closed)
and A-5 (hinge plan detail at a divider). The reference was drawn for an older
option (6 dividers in 5/8 MDF, doors 30-1/32, wall 199-11/16); every number below
comes from CUTLIST.md or guides/04-doors-hinges-shelves.md instead, cited on the
line that defines it, and the geometry and the labels are produced from the same
constants so the drawing cannot disagree with its text.

  04-doors-closed-elevation.svg  the whole wall as the room sees it
  04-hinge-plan-detail.svg       the 9 mm / 1/8 cover split at a divider, and door 1

All lengths are snapped to 64ths by ``q()``: ``svgkit.frac`` snaps to 64ths before
printing, so a value must already be an exact 64th before it is labelled.
"""
import math

from svgkit import Canvas, MAT, frac, LINE, DIM


def q(x):
    """Snap to the nearest 1/64 (shop resolution, and what frac() can print)."""
    return round(x * 64) / 64.0


def f(x):
    return frac(q(x))


# --------------------------------------------------------------------------------------
# Constants.  Fractions are written as exact binary sums so nothing rounds.
# --------------------------------------------------------------------------------------

# CUTLIST.md header: "wall 199-3/8, tall cabinet 18-3/8 W x 82-11/16 H x 24-7/16 D,
#                     TV run 181 W x 15 H x 16 D, 4-15/16 kick under both"
WALL_W = 199 + 3 / 8.0          # between the two end walls
TALL_W = 18 + 3 / 8.0           # tall cabinet outside width, at the left wall
TALL_H = 82 + 11 / 16.0         # tall cabinet height
TV_W = 181.0                    # TV run width
TV_H = 15.0                     # TV run height, line A to line F

# guide 3 "TV ladder" height table (heights above the finished floor at the high spot)
LINE_A = 4 + 15 / 16.0          # underside of the bottom stringers = kick top = door bottom
LINE_C = 6 + 15 / 16.0          # top of the 1/2 bottoms = divider bottom
LINE_F = 19 + 15 / 16.0         # slab top
SLAB_T = 0.5                    # CUTLIST "1/2 MDF (TV top slab)"
SLAB_BOT = q(LINE_F - SLAB_T)   # 19-7/16
KICK_H = LINE_A                 # CUTLIST "kick, tall / kick, TV" 4-15/16 wide
KICK_RECESS = 2.5               # CUTLIST notes: "The TV kick is recessed 2-1/2"
TALL_TOP = q(LINE_A + TALL_H)   # 87-5/8 -- the tall cabinet stands on line A

# CUTLIST "5/8 MDF (paint-grade faces)" table
T58 = 0.625                     # 5/8 MDF doors, tall sides, packer
T12 = 0.5                       # 1/2 spruce dividers (12.7 mm)
TALL_DOOR_W = 18 + 1 / 8.0      # tall door 82-11/16 x 18-1/8
TALL_DOOR_H = TALL_H
DOOR_W = 29 + 63 / 64.0         # TV doors 29-63/64 x 14-3/8
DOOR_H = 14 + 3 / 8.0
DOOR_BOT = LINE_A               # guide 4: bottom flush with the front stringer underside
DOOR_TOP = q(DOOR_BOT + DOOR_H)  # 19-5/16
REVEAL = 0.125                  # CUTLIST notes "Doors": 1/8 between doors and under the slab
END_GAP = 0.25                  # 1/4 at the right wall and at the tall cabinet

# CUTLIST "TV divider positions": door left edges from the left wall
DOOR_LEFT = [q(18 + 5 / 8.0), q(48 + 47 / 64.0), q(78 + 53 / 64.0),
             q(108 + 15 / 16.0), q(139 + 3 / 64.0), q(169 + 9 / 64.0)]
# and the divider LEFT faces from the left wall (same table)
DIV_LEFT = [q(48 + 37 / 64.0), q(78 + 11 / 16.0), q(108 + 51 / 64.0),
            q(138 + 57 / 64.0), 169.0]

# guide 4 "Hinge cups" / "Mounting plates"
CUP_D = 35 / 25.4               # 35 mm Forstner
CUP_R = CUP_D / 2
CUP_DEPTH = 12.5 / 25.4         # 12.5 mm deep in 5/8 MDF
CUP_OFF = 22.5 / 25.4           # cup centre 7/8 (22.5 mm) in from the hinge edge
CUP_END = 3.5                   # TV doors: cups 3-1/2 from the top and bottom edges
TALL_CUPS = [3.5, q(22 + 7 / 16.0), q(41 + 3 / 8.0), q(60 + 1 / 4.0), q(79 + 3 / 16.0)]
COVER = 9 / 25.4                # half overlay, 9 mm nominal cover -- all 17 hinges,
                                # one SKU; as built the shop's 64ths land the cover
                                # between 11/32 and 23/64, inside the hinge's own
                                # cover adjustment
PLATE_BACK = 1 + 15 / 32.0      # plate holes 1-15/32 (37 mm) back from the panel front
                                # edge -- guide 4 "Mounting plates" writes 1-15/32, and
                                # 15-3/8 - 1-15/32 = 13-29/32, the figure in that table
PLATE_LEN = 1.75                # mounting plate body, drawing choice (~44 mm)
PLATE_T = 3 / 25.4              # plate thickness off the face, drawing choice
DIV_PLATES = [1.5, q(8 + 7 / 8.0)]   # plate centres above the divider bottom (= line C)

# guide 4 "Which edge gets the hinges": the packer under door 1
PACKER_T = T58                  # 5/8 spruce offcut
PACKER_W = 3.0                  # 3 wide (in the depth direction)
# The packer runs from line C up to the underside of the bay 1 top-front stringer's 2x2
# end block, which occupies the top 1-1/2 of the bay (line E - 1-1/2 = 17-15/16):
# 17-15/16 - 6-15/16 = 11 tall (guide 4 "Which edge gets the hinges").
END_BLOCK_H = 1.5               # 2x2 end block above the packer
PACKER_TALL = q(SLAB_BOT - END_BLOCK_H - LINE_C)
TALL_PAST_DOOR = q(8 + 7 / 16.0)  # "the face carries on 8-7/16 past the door"

# The remainder of the divider left of the reveal, once the hinged door has taken its
# 9 mm cover and the 1/8 reveal has been set: 12.7 - 9 - 3.175 = 0.525 mm.
REMAIN = q(T12 - COVER - REVEAL)      # 1/64 as drawn
REMAIN_MM = (T12 - COVER - REVEAL) * 25.4   # 0.525 mm exactly

CAP = 9.5
NOTE = 9.0


class Sheet(Canvas):
    """Canvas with a model-space origin shift so dimension stacks can sit outside
    the part without leaving the viewBox."""

    def __init__(self, *a, x_off=0.0, y_off=0.0, **kw):
        super().__init__(*a, **kw)
        self.x_off, self.y_off = x_off, y_off

    def X(self, x):
        return super().X(x + self.x_off)

    def Y(self, y):
        return super().Y(y + self.y_off)

    def arrow(self, x, y, dx, dy, size=0.0, color=LINE):
        """Filled triangle at (x, y) pointing along (dx, dy). size in model inches."""
        n = math.hypot(dx, dy) or 1.0
        ux, uy = dx / n, dy / n
        px, py = -uy, ux
        s = size
        self.poly([(x, y), (x - ux * s + px * s * 0.45, y - uy * s + py * s * 0.45),
                   (x - ux * s - px * s * 0.45, y - uy * s - py * s * 0.45)],
                  fill=color, stroke=color, sw=0.6)

    def arc(self, cx, cy, r, a0, a1, color="#8a6d3b", sw=0.9, dash="7,4", n=26):
        """Polyline approximation of an arc; angles in degrees, +x = 0, y as drawn."""
        pts = []
        for i in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            self.line(x1, y1, x2, y2, stroke=color, sw=sw, dash=dash)
        return pts

    def break_line(self, x, y0, y1, amp=0.16, color=LINE):
        """Conventional break zigzag across a vertical cut at model x, y0..y1."""
        n = 4
        pts = []
        for i in range(n + 1):
            t = i / float(n)
            off = 0.0 if i in (0, n) else (amp if i % 2 else -amp)
            pts.append((x + off, y0 + (y1 - y0) * t))
        for (x1, yy1), (x2, yy2) in zip(pts, pts[1:]):
            self.line(x1, yy1, x2, yy2, stroke=color, sw=1.0)

    def break_line_h(self, y, x0, x1, amp=0.16, color=LINE):
        """Break zigzag across a horizontal cut at model y, x0..x1."""
        n = 4
        pts = []
        for i in range(n + 1):
            t = i / float(n)
            off = 0.0 if i in (0, n) else (amp if i % 2 else -amp)
            pts.append((x0 + (x1 - x0) * t, y + off))
        for (x1_, y1_), (x2_, y2_) in zip(pts, pts[1:]):
            self.line(x1_, y1_, x2_, y2_, stroke=color, sw=1.0)


# ---------------------------------------------------------------------------
# 1. front elevation, doors closed (ported from A-1)
# ---------------------------------------------------------------------------
def doors_closed_elevation(path):
    WT, FT = 2.0, 1.0                     # end wall and floor band thickness, drawing only
    WALL_TOP = 96.0
    c = Sheet(260.5, 121.5, scale=5.2, flip_y=True, x_off=14.5, y_off=19.5,
              title="Front elevation, doors closed: tall cabinet at the left wall, "
                    "six TV doors to the right wall")

    # --- room: floor and the two end walls ---------------------------------
    c.rect(-WT, -FT, WALL_W + 2 * WT, FT, fill=MAT["floor"], sw=1.0)
    c.rect(-WT, 0, WT, WALL_TOP, fill=MAT["wall"], sw=1.0)
    c.rect(WALL_W, 0, WT, WALL_TOP, fill=MAT["wall"], sw=1.0)
    c.line(-WT, 0, WALL_W + WT, 0, stroke=LINE, sw=1.6)
    c.text(-WT / 2, 46.0, "left end wall", size=NOTE, rotate=-90, color="#555")
    c.text(WALL_W + WT / 2, 46.0, "right end wall", size=NOTE, rotate=-90, color="#555")

    # --- tall cabinet: carcass, then the door over it ----------------------
    c.rect(0, LINE_A, TALL_W, TALL_H, fill=MAT["spruce58"], sw=1.2)
    c.rect(END_GAP, LINE_A, TALL_DOOR_W, TALL_DOOR_H, fill=MAT["mdf58"], sw=1.4)
    c.text(q(END_GAP + TALL_DOOR_W / 2), 52.0,
           "tall door  %s x %s  (5/8 MDF, 5 hinges at the wall side)"
           % (f(TALL_DOOR_H), f(TALL_DOOR_W)), size=10.5, rotate=-90, weight="bold")
    for h in TALL_CUPS:                  # cups / hinges on the wall (left) edge
        cy = q(LINE_A + h)
        c.line(END_GAP, q(cy - 0.9), END_GAP, q(cy + 0.9), stroke="#8a3b12", sw=3.0)
        c.circle(END_GAP, cy, 2.2, fill="#8a3b12")
    c.line(q(END_GAP + 1.4), 30.0, q(END_GAP + 6.6), 30.0, stroke="#8a3b12", sw=1.2)
    c.arrow(q(END_GAP + 6.6), 30.0, 1, 0, size=1.5, color="#8a3b12")

    # --- TV run: slab strip, then the six doors ----------------------------
    c.rect(TALL_W, SLAB_BOT, TV_W, SLAB_T, fill=MAT["mdf12"], sw=1.2)
    for i, x0 in enumerate(DOOR_LEFT):
        c.rect(x0, DOOR_BOT, DOOR_W, DOOR_H, fill=MAT["mdf58"], sw=1.4)
        c.text(q(x0 + DOOR_W / 2), 13.4, "D%d" % (i + 1), size=13, weight="bold")
        # hinge side: a mark at each cup height on the door's LEFT edge
        for cy in (q(DOOR_BOT + CUP_END), q(DOOR_TOP - CUP_END)):
            c.line(x0, q(cy - 0.55), x0, q(cy + 0.55), stroke="#8a3b12", sw=3.0)
            c.circle(x0, cy, 2.2, fill="#8a3b12")
        # and a short arrow: this door opens to the right
        ay = 9.3
        c.line(q(x0 + 1.4), ay, q(x0 + 6.6), ay, stroke="#8a3b12", sw=1.2)
        c.arrow(q(x0 + 6.6), ay, 1, 0, size=1.5, color="#8a3b12")

    # --- kick band under both units ----------------------------------------
    c.rect(0, 0, TALL_W, KICK_H, fill=MAT["mdf58"], sw=1.4)
    c.rect(TALL_W, 0, TV_W, KICK_H, fill=MAT["mdf58"], sw=1.4, opacity=0.55)
    c.line(TALL_W, 0, TALL_W, KICK_H, stroke=LINE, sw=1.2)
    c.text(q(TALL_W / 2), q(KICK_H / 2), "kick, tall", size=8.0)
    c.text(q(TALL_W + TV_W / 2), q(KICK_H / 2),
           "kick, TV (5/8 MDF) -- set back %s behind the door face, so it is not on "
           "this plane" % f(KICK_RECESS), size=NOTE, color="#555")

    # --- callouts ----------------------------------------------------------
    c.leader(q(TALL_W + TV_W / 2), LINE_F, q(TALL_W + TV_W / 2), 33.4)
    c.label(q(TALL_W + TV_W / 2), 34.6,
            ["TV top slab, 1/2 MDF, %s to %s (two pieces, joint over divider 3)"
             % (f(SLAB_BOT), f(LINE_F))], size=NOTE)
    c.leader(DOOR_LEFT[0], q(DOOR_BOT + CUP_END), q(DOOR_LEFT[0] + 12.0), 40.0)
    c.label(q(DOOR_LEFT[0] + 13.0), 41.2,
            ["every TV door hinges on its LEFT edge and opens right;",
             "cups %s from the door top and bottom (guide 4)" % f(CUP_END)],
            size=NOTE, anchor="start")

    # --- widths: overall, then the two units -------------------------------
    c.dim_h(0, WALL_W, 96.8, text="wall %s between the end walls" % f(WALL_W),
            witness=WALL_TOP, offset_px=-13)
    c.dim_h(0, TALL_W, 92.5, text="tall %s" % f(TALL_W),
            witness=(TALL_TOP, TALL_TOP), offset_px=-13)
    c.dim_h(TALL_W, WALL_W, 92.5, text="TV run %s" % f(TV_W),
            witness=(TALL_TOP, LINE_F), offset_px=-13)
    c.dim_h(0, END_GAP, 89.6, witness=TALL_TOP, offset_px=-13)
    c.dim_h(END_GAP, TALL_W, 89.6, text="tall door %s (flush with the right face)"
            % f(TALL_DOOR_W), witness=TALL_TOP, offset_px=-13)

    # --- small door dims, just above the slab ------------------------------
    y = 21.6
    c.dim_h(TALL_W, DOOR_LEFT[0], y, witness=(LINE_F, DOOR_TOP), offset_px=-11)
    c.dim_h(DOOR_LEFT[0], q(DOOR_LEFT[0] + DOOR_W), y, text="TV door %s" % f(DOOR_W),
            witness=DOOR_TOP, offset_px=-11)
    c.dim_h(q(DOOR_LEFT[0] + DOOR_W), DOOR_LEFT[1], y, text=f(REVEAL) + " reveal",
            witness=DOOR_TOP, offset_px=-11)
    c.dim_h(q(DOOR_LEFT[5] + DOOR_W), WALL_W, y, witness=(DOOR_TOP, LINE_F),
            text="%s at the right wall" % f(END_GAP), fit="left", offset_px=-11)
    c.leader(q(TALL_W + END_GAP / 2), DOOR_TOP, 56.0, 28.4)
    c.label(57.0, 28.4, ["%s at the tall cabinet" % f(END_GAP)], size=NOTE, anchor="start")

    # --- heights, stacked out to the right ---------------------------------
    hx = q(WALL_W + WT + 2.0)   # 203-3/8
    c.dim_v(0, LINE_A, hx, text=f(LINE_A) + " kick", witness=WALL_W, offset_px=12)
    c.dim_v(DOOR_BOT, DOOR_TOP, hx, text=f(DOOR_H) + " door", witness=WALL_W, offset_px=12)
    c.dim_v(DOOR_TOP, SLAB_BOT, hx, text="", witness=WALL_W, offset_px=12)
    c.dim_v(SLAB_BOT, LINE_F, hx, text="", witness=WALL_W, offset_px=12)
    c.leader(hx, q((DOOR_TOP + SLAB_BOT) / 2), q(hx + 3.0), 34.6)
    c.label(q(hx + 3.6), 34.6, ["%s reveal under the slab" % f(REVEAL)],
            size=NOTE, anchor="start")
    c.leader(hx, q((SLAB_BOT + LINE_F) / 2), q(hx + 3.0), 30.6)
    c.label(q(hx + 3.6), 30.6, ["%s slab, %s to %s" % (f(SLAB_T), f(SLAB_BOT), f(LINE_F))],
            size=NOTE, anchor="start")
    c.dim_v(LINE_A, LINE_F, q(hx + 30.0), text=f(TV_H) + " run", witness=WALL_W,
            offset_px=12)
    c.dim_v(0, LINE_F, q(hx + 38.0), text=f(LINE_F) + " slab", witness=WALL_W,
            offset_px=12)

    # --- heights, out to the left ------------------------------------------
    c.dim_v(LINE_A, TALL_TOP, -4.4, text="tall door %s" % f(TALL_DOOR_H), witness=0.0,
            offset_px=-12)
    c.dim_v(0, TALL_TOP, -9.8, text="%s to the top" % f(TALL_TOP), witness=0.0,
            offset_px=-12)

    # --- one row of dims along the bottom: door left edges from the left wall
    sy = -3.2
    stations = [0.0] + DOOR_LEFT
    for x1, x2 in zip(stations, stations[1:]):
        c.dim_h(x1, x2, sy, text="", witness=0.0)
    for x0 in DOOR_LEFT:
        c.text(x0, -4.4, f(x0), size=9.0, color=DIM, rotate=-90, anchor="end")
    c.text(0.0, -4.4, "left wall", size=9.0, color=DIM, rotate=-90, anchor="end")
    c.text(q(DOOR_LEFT[0] + 3.0), -15.8,
           "left edges of doors D1 to D6 from the left wall; pitch %s = door %s + %s reveal"
           % (f(DOOR_W + REVEAL), f(DOOR_W), f(REVEAL)), size=NOTE, anchor="start",
           color=DIM)

    c.text(q(WALL_W / 2), -19.0,
           "front elevation, doors closed -- this is what the room sees",
           size=CAP, color="#555")
    return c.save(path)


# ---------------------------------------------------------------------------
# 2. hinge plan detail (ported from A-5)
# ---------------------------------------------------------------------------
def hinge_plan_detail(path):
    S = 44.0                       # px per inch: this is a detail, drawn large
    FRONT = 5.0                    # model y of the panel front edge (plan, y down)
    DOOR_BACK, DOOR_FACE = FRONT, q(FRONT + T58)
    DIV_TOP = 1.6                  # panels are broken off ~3-1/2 behind the doors
    DX = 16.4                      # x offset of the second (door 1) panel
    NX_A, NX_B = 7.0, 23.6         # note columns, one beside each panel
    plate_hole = q(FRONT - PLATE_BACK)
    plate_y0 = q(plate_hole - PLATE_LEN * 0.45)
    c = Sheet(39.6, 10.3, scale=S, flip_y=False, x_off=7.6, y_off=0.35,
              title="Hinge plan detail: the cover split at a divider, and door 1 on "
                    "its packer at the tall cabinet")

    def cover_dim(x1, x2, y, text):
        """Tiny dimension with its label pulled out to the left on its own lead line,
        so each label is unmistakably attached to its own dimension."""
        c.dim_h(x1, x2, y, text="", witness=DOOR_FACE)
        c.leader(q((x1 + x2) / 2), y, -0.55, y, color=DIM, dot=False)
        c.text(-0.75, y, text, size=10, anchor="end", color=DIM, box=True)

    # ==================================================================
    # panel A: at a divider (doors 2 to 6)
    # ==================================================================
    # divider: left face at x = 0, right face at x = T12; rear broken off
    c.rect(0, DIV_TOP, T12, q(FRONT - DIV_TOP), fill=MAT["spruce12"], sw=1.4)
    c.break_line_h(DIV_TOP, 0, T12)
    hinge_edge = q(T12 - COVER)          # hinged door's left edge: 9 mm onto the divider
    free_edge = q(hinge_edge - REVEAL)   # neighbour's free edge, after the 1/8 reveal

    # the two doors, in front of the divider
    c.rect(-6.0, DOOR_BACK, q(free_edge + 6.0), T58, fill=MAT["mdf58"], sw=1.4)
    c.rect(hinge_edge, DOOR_BACK, q(6.0 - hinge_edge), T58, fill=MAT["mdf58"], sw=1.4)
    c.break_line(-6.0, DOOR_BACK, DOOR_FACE)
    c.break_line(6.0, DOOR_BACK, DOOR_FACE)
    c.text(-3.1, q(DOOR_BACK + T58 / 2), "door D(k-1), free edge", size=NOTE)
    c.text(4.4, q(DOOR_BACK + T58 / 2), "door D(k), opens right", size=NOTE)

    # 35 mm cup in the back face of D(k), centre 22.5 mm from the hinge edge
    cup_c = q(hinge_edge + CUP_OFF)
    c.rect(q(cup_c - CUP_R), DOOR_BACK, CUP_D, CUP_DEPTH, fill="white", sw=1.1)
    c.circle(cup_c, q(DOOR_BACK + CUP_DEPTH / 2), 1.8, fill="#8a3b12")

    # half-overlay plate on the divider's RIGHT face, holes 1-15/32 back from the front
    c.rect(T12, plate_y0, PLATE_T, PLATE_LEN, fill=MAT["2x4"], sw=1.2)
    c.circle(q(T12 + PLATE_T / 2), plate_hole, 2.2, fill=LINE)
    # cranked arm, plate to cup
    for (x1, y1), (x2, y2) in zip(
            [(cup_c, q(DOOR_BACK + CUP_DEPTH / 2)), (0.70, 4.32), (0.78, 3.90)],
            [(0.70, 4.32), (0.78, 3.90), (q(T12 + PLATE_T), 3.90)]):
        c.line(x1, y1, x2, y2, stroke=LINE, sw=1.6)

    # swing of D(k): it opens into the room. Drawn 10 to 80 degrees so neither end of
    # the arc runs into the door or into the cover dimensions below it.
    c.arc(hinge_edge, DOOR_FACE, 1.9, 10, 80)
    a = math.radians(80)
    c.arrow(q(hinge_edge + 1.9 * math.cos(a)), q(DOOR_FACE + 1.9 * math.sin(a)),
            -math.sin(a), math.cos(a), size=0.30, color="#8a6d3b")
    c.text(2.40, 6.80, "swing, 110 deg", size=8.5, color="#8a6d3b", anchor="start")

    c.text(-6.9, 2.1, "REAR (toward the wall)", size=8.5, anchor="start", color="#777")
    c.text(-6.9, 6.25, "FRONT (the room)", size=8.5, anchor="start", color="#777")

    # dims: thicknesses, the 37 mm plate setback, then the three-part cover split
    c.dim_h(0, T12, 1.0, text="%s divider (12.7 mm)" % f(T12), witness=DIV_TOP,
            offset_px=-11)
    c.dim_v(DOOR_BACK, DOOR_FACE, 6.45, text="%s (15.9 mm) door" % f(T58),
            witness=6.0, offset_px=12)
    c.dim_v(plate_hole, FRONT, -2.0, text="%s (37 mm) to the front edge" % f(PLATE_BACK),
            witness=(T12, T12), offset_px=-11)
    cover_dim(hinge_edge, T12, 6.35, 'cover 9 mm nominal')
    cover_dim(free_edge, hinge_edge, 7.05, "%s reveal (3.2 mm)" % f(REVEAL))
    cover_dim(0, free_edge, 7.75, "%.3f mm (about %s)" % (REMAIN_MM, f(REMAIN)))

    # notes for panel A, in the column beside it
    c.leader(q(T12 + PLATE_T), plate_hole, q(NX_A - 0.2), 3.1)
    c.label(NX_A, 3.1,
            ["half-overlay plate (9 mm nominal cover, 0 mm plate) on",
             "divider's RIGHT face -- the face inside D(k)'s own bay.",
             "Holes %s (37 mm) back from the front edge, 32 mm" % f(PLATE_BACK),
             "apart in HEIGHT, so in plan they sit on top of each",
             "other. Plate centres %s and %s above the divider" % (f(DIV_PLATES[0]), f(DIV_PLATES[1])),
             "bottom (line C, %s, which is 2 above the door bottom)." % f(LINE_C),
             "Plate screws 12 mm MAX: the 15 mm screws in the",
             "hinge box break through 1/2 ply."],
            size=NOTE, anchor="start")
    c.leader(cup_c, q(DOOR_BACK + CUP_DEPTH), q(NX_A - 0.2), 7.1)
    c.label(NX_A, 7.1,
            ["35 mm cup, 12.5 mm deep, in the door's BACK face;",
             "centre 7/8 (22.5 mm) in from the hinge edge,",
             "%s from the door top and bottom" % f(CUP_END)],
            size=NOTE, anchor="start")
    c.text(-7.0, 0.25, "A -- at a divider: doors 2 to 6, hinged on dividers 1 to 5",
           size=CAP, weight="bold", anchor="start")

    # ==================================================================
    # panel B: door 1 at the tall cabinet's right side, on its 5/8 packer
    # ==================================================================
    face = DX                      # the tall cabinet's right face
    TALL_CUT = 7.0                 # the tall side is broken off, not drawn to length
    c.rect(q(face - T58), DIV_TOP, T58, q(TALL_CUT - DIV_TOP), fill=MAT["mdf58"], sw=1.4)
    c.break_line_h(DIV_TOP, q(face - T58), face)
    c.break_line_h(TALL_CUT, q(face - T58), face)
    c.rect(face, q(FRONT - PACKER_W), PACKER_T, PACKER_W, fill=MAT["spruce58"], sw=1.4)
    d1_edge = q(face + END_GAP)    # CUTLIST: door 1 left edge 18-5/8, tall face 18-3/8
    c.rect(d1_edge, DOOR_BACK, q(face + 5.4 - d1_edge), T58, fill=MAT["mdf58"], sw=1.4)
    c.break_line(q(face + 5.4), DOOR_BACK, DOOR_FACE)
    cup1 = q(d1_edge + CUP_OFF)
    c.rect(q(cup1 - CUP_R), DOOR_BACK, CUP_D, CUP_DEPTH, fill="white", sw=1.1)
    c.circle(cup1, q(DOOR_BACK + CUP_DEPTH / 2), 1.8, fill="#8a3b12")
    c.text(q(cup1 + CUP_R + 1.5), q(DOOR_BACK + T58 / 2), "door D1, opens right",
           size=NOTE)
    p1x = q(face + PACKER_T)
    c.rect(p1x, plate_y0, PLATE_T, PLATE_LEN, fill=MAT["2x4"], sw=1.2)
    c.circle(q(p1x + PLATE_T / 2), plate_hole, 2.2, fill=LINE)
    for (x1, y1), (x2, y2) in zip(
            [(cup1, q(DOOR_BACK + CUP_DEPTH / 2)), (q(face + 1.32), 4.32),
             (q(face + 1.40), 3.90)],
            [(q(face + 1.32), 4.32), (q(face + 1.40), 3.90),
             (q(p1x + PLATE_T), 3.90)]):
        c.line(x1, y1, x2, y2, stroke=LINE, sw=1.6)
    # the TV door plane: door 1's back face lines up with the rest of the run
    c.line(q(face - 1.4), FRONT, q(face + 5.9), FRONT, stroke="#3b6ea5", sw=0.9,
           dash="8,4")
    c.text(q(face - 1.6), q(FRONT - 0.28), "TV door plane, %s from the wall"
           % f(15 + 3 / 8.0), size=8.5, anchor="end", color="#3b6ea5")

    c.dim_h(q(face - T58), face, 1.0, text="%s tall right side (MDF)" % f(T58),
            witness=DIV_TOP, offset_px=-11)
    c.dim_h(face, d1_edge, 6.35, text="%s gap, cabinet face to door edge" % f(END_GAP),
            witness=DOOR_FACE, fit="right", offset_px=11)
    c.dim_h(d1_edge, q(face + PACKER_T), 7.40,
            text="%s (9.5 mm) cover on the packer" % f(PACKER_T - END_GAP),
            witness=DOOR_FACE, fit="right", offset_px=11)
    c.dim_h(face, q(face + PACKER_T), 8.45, text="%s packer" % f(PACKER_T),
            witness=DOOR_FACE, fit="right", offset_px=11)
    c.dim_v(q(FRONT - PACKER_W), FRONT, q(face + PACKER_T + 1.05),
            text="packer %s wide" % f(PACKER_W), witness=face, offset_px=12)

    c.leader(q(face + PACKER_T / 2), q(FRONT - PACKER_W), q(NX_B - 0.2), 3.1)
    c.label(NX_B, 3.1,
            ["5/8 spruce packer, %s wide x %s tall (line C up to"
             % (f(PACKER_W), f(PACKER_TALL)),
             "the bay 1 end block), glued and screwed to the",
             "tall side's outer face at the plate height; front",
             "face on the TV door plane, so the plate holes land",
             "%s from the wall (guide 4, \"Mounting plates\")."
             % f(15 + 3 / 8.0 - PLATE_BACK)],
            size=NOTE, anchor="start")
    c.leader(q(face - T58 / 2), TALL_CUT, q(NX_B - 0.2), 7.1)
    c.label(NX_B, 7.1,
            ["the tall right side carries on %s past the TV" % f(TALL_PAST_DOOR),
             "door, so no hinge on this face can land door 1:",
             "hence the packer. Half overlay on the packer puts",
             "the edge %s right of %s; the cover screw eats that."
             % (f(1 / 64.0), f(18 + 5 / 8.0))],
            size=NOTE, anchor="start")
    c.text(q(face - T58 - 0.7), 0.25,
           "B -- at the tall cabinet: door 1 on its 5/8 packer",
           size=CAP, weight="bold", anchor="start")

    c.text(-7.0, 8.45,
           "9 mm nominal cover + 1/8 reveal + %.3f mm = the 1/2 divider, so D(k-1)'s free "
           "edge sits essentially flush with the divider's left face" % REMAIN_MM,
           size=NOTE, anchor="start", color="#555")
    c.text(-7.0, 9.05,
           "as built at the shop's 64ths: divider 1 left face %s, right face %s, door 2 "
           "left edge %s -- %s (%.1f mm) of cover. The cover is 9 mm nominal, %s to %s as "
           "built, well inside the hinge's own cover adjustment"
           % (f(DIV_LEFT[0]), f(DIV_LEFT[0] + T12), f(DOOR_LEFT[1]),
              f(DIV_LEFT[0] + T12 - DOOR_LEFT[1]),
              (DIV_LEFT[0] + T12 - DOOR_LEFT[1]) * 25.4, f(11 / 32.0), f(23 / 64.0)),
           size=NOTE, anchor="start", color="#555")
    c.text(q(DX / 2), 9.75,
           "plan, looking down -- rear (wall) at the top, front (room) at the bottom",
           size=CAP, color="#555")
    return c.save(path)


DIAGRAMS = [
    ("04-doors-closed-elevation.svg", doors_closed_elevation,
     "Front elevation with every door closed: tall door at the left wall, TV doors D1 to D6, "
     "kick band under both, and the reveals that set the door sizes"),
    ("04-hinge-plan-detail.svg", hinge_plan_detail,
     "Hinge plan detail: how the 1/2 divider splits into 9 mm cover, 1/8 reveal and a bare "
     "1/64, and how door 1 gets its 5/8 packer on the tall cabinet's right side"),
]


def build(outdir):
    out = []
    for name, fn, caption in DIAGRAMS:
        fn("%s/%s" % (outdir.rstrip("/"), name))
        out.append((name, caption))
    return out


if __name__ == "__main__":
    print(build("."))
