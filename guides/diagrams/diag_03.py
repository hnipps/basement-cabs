"""Diagrams for guide 03 (tall box and TV ladder).

Every number below is a constant taken from CUTLIST.md or
guides/03-tall-box-and-ladder.md, cited on the line that defines it. Geometry and
labels come from the same constants, so the drawing cannot disagree with its text.

All lengths are snapped to 64ths by ``q()``: ``svgkit.frac`` uses
``limit_denominator(64)``, which happily returns thirds and 43rds for a raw decimal
(30.209 -> "30-9/43"), so values must already be exact 64ths before they are labelled.
"""
from svgkit import Canvas, MAT, frac, LINE, DIM


def q(x):
    """Snap to the nearest 1/64 (shop resolution, and what frac() can print)."""
    return round(x * 64) / 64.0


def f(x):
    return frac(q(x))


# --- material thicknesses (CUTLIST material headings) -----------------------
T58 = 0.625            # 5/8" spruce ply and 5/8" MDF
T12 = 0.5              # 1/2" spruce ply and 1/2" MDF
T18 = 0.125            # 1/8" hardboard
LUM = 1.5              # 2x2 SPF and 2x4 thickness, actual (CUTLIST 2x2 / 2x4 headings)
RAIL_H = 3.5           # 2x4 actual width (CUTLIST "Solid lumber - 2x4 on hand")

# --- tall cabinet (CUTLIST 5/8 spruce + 5/8 MDF + hardboard tables) ---------
TALL_H = q(82 + 11 / 16.)   # tall left/right side length 82-11/16
TALL_D = q(23 + 11 / 16.)   # tall side width = carcass depth 23-11/16
TALL_W = q(18 + 3 / 8.)     # tall back width 18-3/8 = box outside width
TALL_INNER = q(TALL_W - 2 * T58)   # 17-1/8 = tall top/bottom width, rail length
TALL_D_BACK = q(TALL_D + T18)      # 23-13/16 with the back on (guide 3 "Box outside")
TALL_D_DOOR = q(TALL_D_BACK + T58)  # 24-7/16 overall (CUTLIST header)
PIN_INSET = q(1 + 15 / 32.)   # 37 mm pin/plate setback (guide 4 "Shelf pins")
PIN_LOW = q(T58 + 6)          # pin rows start 6 above the cabinet bottom (guide 4)
PIN_HIGH = q(TALL_H - T58 - 6)  # and stop 6 below the top
POCKET_REAR = q(1.5)          # "first one 1-1/2 from an edge" (guide 3 "Joinery")
POCKET_FRONT = 3.0            # front pocket setback, chosen to clear the 2 zone
KEEP_CLEAR = 2.0              # "2" clear of the front-left corner" (guide 3)
RAIL_POCKET_INSET = 1.0       # 2 pockets per rail end, 1 from each long edge (drawing choice)

# --- TV run reference lines (guide 3 "TV ladder" table) ---------------------
LINE_A = q(4 + 15 / 16.)
LINE_B = q(6 + 7 / 16.)
LINE_C = q(6 + 15 / 16.)
LINE_D = q(15 + 15 / 16.)
LINE_E = q(19 + 7 / 16.)
LINE_F = q(19 + 15 / 16.)
LINES = [
    ("A", LINE_A, "underside of both bottom stringers"),
    ("B", LINE_B, "top of the bottom stringers"),
    ("C", LINE_C, "top of the 1/2 bottoms"),
    ("D", LINE_D, "bottom edge of the 2x4 rails"),
    ("E", LINE_E, "top of rails, dividers, stringers"),
    ("F", LINE_F, "slab top = panelling bottom"),
]

# --- TV run depths (CUTLIST notes "Carcass depths"; guide 3 steps 3, 6, 7) --
TV_DEPTH = 16.0                  # TV top slab width 16 = overall depth
TV_CARCASS = q(TV_DEPTH - T58)   # 15-3/8 bottom depth / front stringer front face
CROSS_LEN = q(12 + 3 / 8.)       # cross block 12-3/8 (CUTLIST 2x2 table)
SLEEPER_CUT = q(4 + 3 / 4.)      # "Cut them 4-3/4 and shim to line A" (guide 3 step 3)
SLEEPER_FRONT_FACE = q(12 + 7 / 8.)   # front sleeper front face from wall (step 6)
KICK_RECESS = q(2.5)             # TV kick recessed 2-1/2 behind the door face
KICK_H = q(4 + 15 / 16.)         # kick, TV height (CUTLIST 5/8 MDF table)
DIV_H = q(12.5)                  # TV divider 12-1/2 (CUTLIST 1/2 spruce table)
NOTCH_UP = RAIL_H                # rail notch 3-1/2 up x 1-1/2 in (CUTLIST notes)
NOTCH_IN = LUM
DOOR_H = q(14 + 3 / 8.)          # TV door 29-63/64 x 14-3/8 (CUTLIST 5/8 MDF table)
DOOR_REVEAL = q(0.125)           # 1/8 under the slab (CUTLIST notes "Doors")

# --- TV run length and positions -------------------------------------------
TV_LEN = 181.0                   # TV run width (CUTLIST header)
# Divider LEFT faces from the tall cabinet's right side. CUTLIST "TV divider
# positions" gives 30.209 / 60.313 / 90.417 / 120.521 / 150.625; snapped to 64ths
# these are exactly the guide's 30-13/64, 60-5/16, 90-27/64, 120-33/64, 150-5/8.
DIV_LEFT = [q(30.209), q(60.313), q(90.417), q(120.521), q(150.625)]
DIV_CTR = [q(x + T12 / 2) for x in DIV_LEFT]   # cross block / joint centres
# Rail joints (CUTLIST "Solid lumber": joints at 78-45/64 and 139-3/64 from the
# left wall, i.e. 60-21/64 and 120-43/64 from the tall cabinet side).
RAIL_LEN = q(60 + 21 / 64.)
RAIL_JOINTS = [RAIL_LEN, q(120 + 43 / 64.)]
# Bottom stringer / bottom pieces (CUTLIST 1/2 spruce + 2x2 tables).
BOT_PIECES = [q(60 + 9 / 16.), q(60 + 13 / 64.), q(60 + 15 / 64.)]
BOT_JOINTS = [BOT_PIECES[0], q(BOT_PIECES[0] + BOT_PIECES[1])]   # 60-9/16, 120-49/64
# Cross blocks: left end, the five divider centres, right end (guide 3 step 5).
CROSS_CTR = [q(LUM / 2)] + DIV_CTR + [q(TV_LEN - LUM / 2)]
# Top front stringers, bays 1 to 6 (CUTLIST 2x2 table).
TOP_FRONT = [q(30 + 13 / 64.)] + [q(29 + 39 / 64.)] * 4 + [q(29 + 7 / 8.)]
END_BLOCK = 3.0                  # 2x2 offcut end block, length to suit (guide 3 step 9)

CAP = 9.5                        # caption / label font size
NOTE = 9.0


def _caption(c, x, y, text, anchor="middle"):
    c.text(x, y, text, size=CAP, anchor=anchor, color="#555")


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

    def leader(self, x1, y1, x2, y2):
        self.line(x1, y1, x2, y2, stroke="#777", sw=0.7)

    def pocket(self, x, y, into=1.0):
        """Pocket screw: circle on the joint line, stub pointing into the side."""
        self.circle(x, y, 2.4, fill="white", stroke=LINE)
        self.line(x, y, x + into, y, stroke=LINE, sw=0.8)


# ---------------------------------------------------------------------------
# 1. tall box, side section
# ---------------------------------------------------------------------------
def tall_box_section(path):
    c = Sheet(70, 106, scale=7.5, flip_y=True, x_off=5.6, y_off=11.4,
              title="Tall cabinet, side section (rear at left, front at right)")
    # cut plane between the sides: the left side's inner face is the background
    c.rect(0, 0, TALL_D, TALL_H, fill=MAT["spruce58"], sw=1.0)
    c.rect(-T18, 0, T18, TALL_H, fill=MAT["hardboard"])                 # back
    c.rect(0, 0, TALL_D, T58, fill=MAT["spruce58"], sw=1.6)             # bottom
    c.rect(0, TALL_H - T58, TALL_D, T58, fill=MAT["spruce58"], sw=1.6)  # top
    c.rect(0, T58, LUM, RAIL_H, fill=MAT["2x4"], sw=1.4)                # bottom rail
    c.rect(0, TALL_H - T58 - RAIL_H, LUM, RAIL_H, fill=MAT["2x4"], sw=1.4)  # top rail
    c.rect(TALL_D_BACK, 0, T58, TALL_H, fill=MAT["mdf58"], sw=1.4)      # door
    for x in (PIN_INSET, TALL_D - PIN_INSET):
        c.line(x, PIN_LOW, x, PIN_HIGH, stroke="#666", sw=0.9, dash="5,4")
        c.circle(x, PIN_LOW, 1.6, fill="#666")
        c.circle(x, PIN_HIGH, 1.6, fill="#666")

    lx = TALL_D_DOOR - T18 + 2.0
    for (ax, ay), ly, lines in [
        ((TALL_D / 2, TALL_H - T58 / 2), 92.5,
         ["tall top 23-11/16 x 17-1/8 (5/8 spruce),", "on its end, flush front and rear"]),
        ((LUM / 2, TALL_H - T58 - RAIL_H / 2), 81.0,
         ["tall hanging rail 17-1/8 x 3-1/2 (2x4),", "tight under the top, flush rear"]),
        ((TALL_D_BACK + T58 / 2, 64.0), 64.0, ["tall door, 5/8 MDF"]),
        ((TALL_D - PIN_INSET, 48.0), 48.0,
         ["shelf pin rows, 1-15/32 from the front", "and rear edges (guide 4)"]),
        ((-T18 / 2, 32.0), 32.0, ["tall back, 1/8 hardboard,", "over the rear edges"]),
        ((LUM / 2, T58 + RAIL_H / 2), 13.0,
         ["tall hanging rail on the bottom", "at the rear, planed face to the rear"]),
        ((TALL_D / 2, T58 / 2), 3.0,
         ["tall bottom, on its end,", "flush with the front and rear edges"]),
    ]:
        c.leader(ax, ay, lx - 0.4, ly)
        c.label(lx, ly, lines, size=NOTE, anchor="start")
    c.text(TALL_D / 2, TALL_H / 2, "tall left side, inner face (5/8 spruce)",
           size=NOTE, color="#5b4a2e", rotate=-90)

    c.dim_v(0, TALL_H, -0.9, offset_px=-13)
    c.dim_h(0, TALL_D, -1.6, offset_px=13)
    c.dim_h(-T18, TALL_D, -4.4, text=f(TALL_D_BACK) + " with the back", offset_px=13)
    c.dim_h(-T18, TALL_D_DOOR - T18, -7.2, text=f(TALL_D_DOOR) + " with the door", offset_px=13)
    c.dim_v(T58, T58 + RAIL_H, -2.8, offset_px=-12)
    c.dim_h(0, LUM, T58 + RAIL_H + 1.4, offset_px=-12)
    _caption(c, -4.4, -10.6, "side section - the cut plane runs between the two sides",
             anchor="start")
    return c.save(path)


# ---------------------------------------------------------------------------
# 2. tall box, front elevation: where the pockets go
# ---------------------------------------------------------------------------
def tall_box_front(path):
    c = Sheet(76, 96, scale=7.0, flip_y=True, x_off=7.2, y_off=8.0,
              title="Tall cabinet, front elevation with the MDF right side removed")
    RS = q(TALL_W - T58)   # left face of the (removed) right side
    c.rect(0, 0, T58, TALL_H, fill=MAT["spruce58"], sw=1.6)          # left side
    c.rect(RS, 0, T58, TALL_H, fill="none", sw=1.1, dash="6,4")      # right side removed
    c.rect(T58, 0, TALL_INNER, T58, fill=MAT["spruce58"], sw=1.6)    # bottom
    c.rect(T58, TALL_H - T58, TALL_INNER, T58, fill=MAT["spruce58"], sw=1.6)  # top
    rails = [T58, q(TALL_H - T58 - RAIL_H)]
    for y0 in rails:
        c.rect(T58, y0, TALL_INNER, RAIL_H, fill=MAT["2x4"], sw=1.4)
        for y in (q(y0 + RAIL_POCKET_INSET), q(y0 + RAIL_H - RAIL_POCKET_INSET)):
            c.pocket(T58, y, into=-T58)
            c.pocket(RS, y, into=T58)
    for y in (q(T58 / 2), q(TALL_H - T58 / 2)):
        c.pocket(T58, y, into=-T58)
        c.pocket(RS, y, into=T58)
    c.text(-5.2, TALL_H / 2, "tall left side (5/8 spruce)", size=NOTE, rotate=-90)
    c.leader(-4.8, TALL_H / 2, T58, TALL_H / 2)
    c.text(q(TALL_W + 2.6), 62.0, "tall right side (5/8 MDF) removed to draw",
           size=NOTE, rotate=-90, color="#777")
    c.leader(q(TALL_W + 2.2), 62.0, TALL_W, 62.0)
    c.dim_h(0, TALL_W, -1.6, offset_px=13)
    c.dim_h(T58, q(TALL_W - T58), -4.2, offset_px=13)
    c.dim_v(0, TALL_H, -0.9, offset_px=-13)
    c.dim_v(rails[1], q(rails[1] + RAIL_POCKET_INSET), q(TALL_W / 2), offset_px=-11)

    # notes column, clear of the 18-3/8 wide elevation
    nx = q(TALL_W + 6.0)
    for (ax, ay), ly, lines in [
        ((T58, q(TALL_H - T58 / 2)), 81.0,
         ["tall top: 3 pockets in each end,", "spread in the depth - see the plan"]),
        ((T58, q(rails[1] + RAIL_H - RAIL_POCKET_INSET)), 74.0,
         ["tall hanging rail: 2 pockets per end,", "1 from each long edge, jig at 1-1/2,", "2-1/2 coarse screws"]),
        ((T58, q(rails[0] + RAIL_POCKET_INSET)), 9.0,
         ["bottom rail: the same 2 pockets per end"]),
        ((T58, q(T58 / 2)), 5.0, ["tall bottom: 3 pockets in each end"]),
    ]:
        c.leader(ax, ay, nx - 0.5, ly)
        c.label(nx, ly, lines, size=NOTE, anchor="start")
    c.label(nx, 65.0,
            ["Pockets go in the ends of the top, bottom",
             "and rails, screwing into the sides.",
             "NEVER drill pockets in the sides.",
             "Jig at the 5/8 setting, 1 coarse screws,",
             "glue on every joint.",
             "",
             "circle = pocket, stub = screw direction"], size=NOTE, anchor="start")

    # plan of the top / bottom panel: where the three pockets sit in the depth
    px0, py0 = nx, 16.0
    c.rect(px0, py0, TALL_INNER, TALL_D, fill=MAT["spruce58"], sw=1.4)
    c.rect(px0, py0, KEEP_CLEAR, KEEP_CLEAR, fill=MAT["waste"], sw=0.9)
    depths = [POCKET_REAR, q(TALL_D / 2), q(TALL_D - POCKET_FRONT)]
    for d in depths:
        y = q(py0 + TALL_D - d)   # plan: front edge at the bottom, rear edge at the top
        c.pocket(px0, y, into=1.1)
        c.pocket(q(px0 + TALL_INNER), y, into=-1.1)
    c.text(px0, q(py0 + TALL_D + 2.6), "tall top / bottom, plan (both the same)",
           size=CAP, anchor="start")
    c.text(q(px0 + TALL_INNER / 2), q(py0 + TALL_D - 0.9), "rear edge", size=NOTE)
    c.text(q(px0 + TALL_INNER / 2), q(py0 + 1.1), "front edge", size=NOTE)
    c.text(q(px0 + TALL_INNER / 2), q(py0 + 17.0), "3 pockets per end", size=NOTE)
    c.dim_h(px0, q(px0 + TALL_INNER), q(py0 - 2.4), offset_px=13)
    c.dim_v(py0, q(py0 + TALL_D), q(px0 - 1.4), offset_px=-12)
    c.dim_v(q(py0 + TALL_D - POCKET_REAR), q(py0 + TALL_D), q(px0 + TALL_INNER + 1.3),
            offset_px=11, rotate=90)
    c.dim_v(py0, q(py0 + TALL_D - depths[2]), q(px0 + TALL_INNER + 1.3),
            offset_px=11, rotate=90)
    kx = q(px0 + TALL_INNER + 4.0)
    c.leader(px0 + KEEP_CLEAR, q(py0 + KEEP_CLEAR), kx - 0.4, q(py0 + 7.0))
    c.label(kx, q(py0 + 7.0),
            ["keep pockets 2 clear of the", "front-left corner: the hinge", "plates land there (guide 4)"],
            size=NOTE, anchor="start")
    _caption(c, -6.4, -7.4, "front elevation - pocket screw layout", anchor="start")
    return c.save(path)


# ---------------------------------------------------------------------------
# 3. TV ladder, cross-section through one bay
# ---------------------------------------------------------------------------
def ladder_section(path):
    c = Sheet(41, 29, scale=23.0, flip_y=True, x_off=9.0, y_off=4.2,
              title="TV ladder, cross-section through one bay (wall at left, floor at bottom)")
    WALL_T, FL = 1.6, 1.1
    c.rect(-WALL_T, 0, WALL_T, LINE_F + 2.6, fill=MAT["wall"], sw=1.0)
    c.rect(-WALL_T, -FL, TV_DEPTH + 1.4 + WALL_T, FL, fill=MAT["floor"], sw=1.0)
    fs0 = q(SLEEPER_FRONT_FACE - LUM)         # front sleeper rear face
    for x0 in (0.0, fs0):                     # sleepers, cut 4-3/4, shimmed to line A
        c.rect(x0, 0, LUM, SLEEPER_CUT, fill=MAT["2x2"], sw=1.2)
        c.rect(x0, SLEEPER_CUT, LUM, q(LINE_A - SLEEPER_CUT), fill=MAT["waste"], sw=0.8)
    fst0 = q(TV_CARCASS - LUM)                # front stringer rear face
    c.rect(0, LINE_A, LUM, LUM, fill=MAT["2x2"], sw=1.3)                 # rear stringer
    c.rect(fst0, LINE_A, LUM, LUM, fill=MAT["2x2"], sw=1.3)              # front stringer
    c.rect(LUM, LINE_A, CROSS_LEN, LUM, fill=MAT["2x2"], sw=1.0, dash="6,3")  # cross block
    c.rect(0, LINE_B, TV_CARCASS, T12, fill=MAT["spruce12"], sw=1.3)     # TV bottom
    c.poly([(0, LINE_C), (TV_CARCASS, LINE_C), (TV_CARCASS, LINE_E),
            (NOTCH_IN, LINE_E), (NOTCH_IN, LINE_D), (0, LINE_D)],
           fill=MAT["spruce12"], sw=1.4)                                  # divider
    c.rect(0, LINE_D, LUM, RAIL_H, fill=MAT["2x4"], sw=1.4)              # 2x4 rail
    c.rect(fst0, q(LINE_E - LUM), LUM, LUM, fill=MAT["2x2"], sw=1.3)     # top front stringer
    c.rect(0, LINE_E, TV_DEPTH, T12, fill=MAT["mdf12"], sw=1.4)          # slab
    door_top = q(LINE_E - DOOR_REVEAL)
    c.rect(TV_CARCASS, q(door_top - DOOR_H), T58, DOOR_H, fill=MAT["mdf58"], sw=1.4)
    kick_face = q(TV_DEPTH - KICK_RECESS)
    c.rect(q(kick_face - T58), 0, T58, KICK_H, fill=MAT["mdf58"], sw=1.4)

    # lines A to F, labelled at the far left
    nudge = {"A": -0.30, "B": -0.38, "C": 0.38, "D": 0.0, "E": -0.42, "F": 0.42}
    for name, h, _what in LINES:
        c.line(-4.4, h, TV_DEPTH + 0.9, h, stroke="#3b6ea5", sw=0.8, dash="9,4")
        ly = h + nudge[name]
        c.leader(-4.4, h, -4.7, ly)
        c.text(-4.9, ly, "%s  %s" % (name, f(h)), size=CAP, anchor="end", color="#3b6ea5")

    lx = TV_DEPTH + 1.4
    for (ax, ay), ly, lines in [
        ((q(TV_CARCASS - LUM / 2), q(LINE_E - LUM / 2)), 19.6,
         ["top front stringer bay 2 (2x2),", "top on line E, front face flush"]),
        ((q(LUM / 2), q(LINE_D + RAIL_H / 2)), 17.6,
         ["TV hanging rail 60-21/64 x 3-1/2 (2x4),", "screwed to the studs, top on line E"]),
        ((8.6, 13.2), 14.5, ["divider 2 (1/2 spruce), 12-1/2 tall,", "standing on the bottom"]),
        ((q(TV_DEPTH - T58 / 2), 11.4), 11.4, ["TV door (5/8 MDF), 14-3/8 high,", "bottom on line A"]),
        ((7.0, q(LINE_B + T12 / 2)), 9.0, ["TV bottom 1 (1/2 spruce), 15-3/8 deep,", "rear edge scribed to the wall"]),
        ((q(LUM / 2), q(LINE_A + LUM / 2)), 7.2, ["bottom rear stringer (2x2),", "tight to the wall, top on line B"]),
        ((q(TV_CARCASS - LUM / 2), q(LINE_A + LUM / 2)), 5.4, ["bottom front stringer (2x2),", "front face 15-3/8 from the wall"]),
        ((7.0, q(LINE_A + LUM / 2)), 3.6, ["cross block 12-3/8, between the", "stringers (hidden behind the front one)"]),
        ((q(kick_face - T58 / 2), 2.4), 2.4, ["kick, TV (5/8 MDF), face 2-1/2", "behind the door face"]),
        ((q(fs0 + LUM / 2), 1.9), 0.7, ["sleepers (2x2) cut 4-3/4,", "shimmed up to line A"]),
    ]:
        c.leader(ax, ay, lx - 0.3, ly)
        c.label(lx, ly, lines, size=NOTE, anchor="start")
    c.leader(q(LUM / 2), 1.9, lx - 0.3, 0.7)
    c.text(7.0, q(LINE_F + 1.0), "TV top slab (1/2 MDF), 16 deep, E to F", size=CAP)
    c.label(5.6, 11.5, ["rail notch in the divider:", "3-1/2 up x 1-1/2 in, rear top corner"],
            size=NOTE)
    c.leader(3.0, 12.1, NOTCH_IN + 0.1, q(LINE_D - 0.4))

    c.dim_h(0, NOTCH_IN, q(LINE_F + 2.1), offset_px=-11)
    c.dim_h(0, SLEEPER_FRONT_FACE, -1.9)
    c.dim_h(q(kick_face - T58), TV_DEPTH, -1.9, text=f(KICK_RECESS) + " recess")
    c.dim_h(0, TV_CARCASS, -2.9)
    c.dim_h(0, TV_DEPTH, -3.9)
    c.dim_v(LINE_C, LINE_E, 10.4, offset_px=-11)
    _caption(c, 6.0, q(LINE_F + 3.4), "cross-section, bay 2 - all six lines are heights above the finished floor at the high spot")
    return c.save(path)


# ---------------------------------------------------------------------------
# 4. TV ladder, front elevation of the whole run
# ---------------------------------------------------------------------------
def ladder_elevation(path):
    c = Sheet(190, 74, scale=6.0, flip_y=True, x_off=3.4, y_off=26.2,
              title="TV ladder, front elevation of the 181 run (doors off, slab off)")
    c.rect(-1.7, 0, 1.7, q(LINE_F + 1.0), fill=MAT["mdf58"], sw=1.0)
    c.rect(TV_LEN, 0, 1.7, q(LINE_F + 1.0), fill=MAT["wall"], sw=1.0)
    c.line(-1.7, 0, TV_LEN + 1.7, 0, stroke=LINE, sw=1.4)
    c.text(-0.85, 12.5, "tall cabinet side", size=NOTE, rotate=-90, color="#5b4a2e")
    c.text(TV_LEN + 0.85, 10.0, "right wall", size=NOTE, rotate=-90, color="#555")

    # three 2x4 rails end to end, top edge on line E
    edges = [0.0] + RAIL_JOINTS + [TV_LEN]
    for i in range(3):
        c.rect(edges[i], LINE_D, q(edges[i + 1] - edges[i]), RAIL_H, fill=MAT["2x4"], sw=1.2)
        c.text(q(edges[i] + 0.3 * (edges[i + 1] - edges[i])), q(LINE_D + 0.75),
               "TV hanging rail %d, %s" % (i + 1, f(edges[i + 1] - edges[i])), size=NOTE)
    # bottom stringers (front and rear in line in elevation) and the three bottoms
    bedges = [0.0] + BOT_JOINTS + [TV_LEN]
    for i in range(3):
        w = q(bedges[i + 1] - bedges[i])
        c.rect(bedges[i], LINE_A, w, LUM, fill=MAT["2x2"], sw=1.2)
        c.rect(bedges[i], LINE_B, w, T12, fill=MAT["spruce12"], sw=1.2)
        tx = q(bedges[i] + 0.3 * w)
        c.text(tx, q(LINE_A + LUM / 2), "bottom stringers %s" % f(w), size=NOTE)
        c.text(tx, 3.7, "TV bottom %d" % (i + 1), size=NOTE, color="#5b4a2e")
    # seven cross blocks, hidden behind the front stringer
    for i, cx in enumerate(CROSS_CTR):
        c.rect(q(cx - LUM / 2), LINE_A, LUM, LUM, fill="none", sw=0.9, dash="3,2")
        tx = cx + (1.8 if i == 0 else (-1.8 if i == len(CROSS_CTR) - 1 else 0.0))
        c.text(tx, 2.2, "cb %d" % (i + 1), size=8.0, color="#777")
        c.leader(cx, 2.9, cx, q(LINE_A - 0.1))
    # five dividers, standing on the bottoms, in front of the rails
    for i, x in enumerate(DIV_LEFT):
        c.rect(x, LINE_C, T12, DIV_H, fill=MAT["spruce12"], sw=1.3)
        c.text(q(x + T12 / 2), q(LINE_E + 0.9), "divider %d" % (i + 1), size=NOTE)
    # six top front stringers, one per bay, in front of the rails
    bays = [(0.0, DIV_LEFT[0])]
    bays += [(q(DIV_LEFT[k - 1] + T12), DIV_LEFT[k]) for k in range(1, 5)]
    bays += [(q(DIV_LEFT[4] + T12), TV_LEN)]
    for i, (x0, x1) in enumerate(bays):
        c.rect(x0, q(LINE_E - LUM), q(x1 - x0), LUM, fill=MAT["2x2"], sw=1.2)
        c.text(q((x0 + x1) / 2), q(LINE_E - LUM / 2),
               "top front stringer bay %d, %s" % (i + 1, f(TOP_FRONT[i])), size=8.0)
    # end blocks, bay 1 left and bay 6 right
    for x0 in (0.0, q(TV_LEN - END_BLOCK)):
        c.rect(x0, q(LINE_E - LUM), END_BLOCK, LUM, fill="none", sw=1.0, dash="2,2")
    c.leader(q(END_BLOCK / 2), LINE_E, 14.0, 22.2)
    c.label(15.0, 22.4, ["2x2 offcut end block screwed to the tall cabinet side (behind the stringer)"],
            size=NOTE, anchor="start")
    c.leader(q(TV_LEN - END_BLOCK / 2), LINE_E, q(TV_LEN - 14.0), 22.2)
    c.label(q(TV_LEN - 15.0), 22.4, ["end block to the right wall"], size=NOTE, anchor="end")

    # dimensions: joints along the top, divider left faces along the bottom
    c.dim_h(0, RAIL_JOINTS[0], 25.6, text=f(RAIL_JOINTS[0]) + " rail joint 1")
    c.dim_h(0, RAIL_JOINTS[1], 30.2, text=f(RAIL_JOINTS[1]) + " rail joint 2")
    c.dim_h(0, BOT_JOINTS[0], 34.8, text=f(BOT_JOINTS[0]) + " bottom stringer / bottom joint 1")
    c.dim_h(0, BOT_JOINTS[1], 39.4, text=f(BOT_JOINTS[1]) + " bottom stringer / bottom joint 2")
    c.dim_h(0, TV_LEN, 44.0, text=f(TV_LEN) + " tall cabinet side to right wall")
    for i, x in enumerate(DIV_LEFT):
        c.dim_h(0, x, q(-3.4 - 4.6 * i), text=f(x) + " to divider %d left face" % (i + 1))
    _caption(c, TV_LEN / 2, -25.4,
             "front elevation, doors and slab off - rail joints hide inside dividers 2 and 4")
    return c.save(path)


# ---------------------------------------------------------------------------
# 5. TV ladder, plan of the bottom ladder
# ---------------------------------------------------------------------------
def ladder_plan(path):
    c = Sheet(200, 63, scale=6.0, flip_y=False, x_off=13.0, y_off=15.4,
              title="Bottom ladder, plan from above (wall at the top)")
    c.rect(-1.7, -1.7, TV_LEN + 3.4, 1.7, fill=MAT["wall"], sw=1.0)
    c.text(TV_LEN / 2, -0.85, "rear wall", size=NOTE, color="#555")
    c.rect(-1.7, 0, 1.7, TV_CARCASS, fill=MAT["mdf58"], sw=1.0)
    c.rect(TV_LEN, 0, 1.7, TV_CARCASS, fill=MAT["wall"], sw=1.0)
    c.text(-0.85, TV_CARCASS / 2, "tall cabinet", size=NOTE, rotate=-90, color="#5b4a2e")
    c.text(TV_LEN + 0.85, TV_CARCASS / 2, "right wall", size=NOTE, rotate=-90, color="#555")

    bedges = [0.0] + BOT_JOINTS + [TV_LEN]
    fst0 = q(TV_CARCASS - LUM)
    for i in range(3):
        w = q(bedges[i + 1] - bedges[i])
        c.rect(bedges[i], 0, w, LUM, fill=MAT["2x2"], sw=1.2)        # rear stringer
        c.rect(bedges[i], fst0, w, LUM, fill=MAT["2x2"], sw=1.2)     # front stringer
        mid = q(bedges[i] + 0.3 * w)
        c.text(mid, q(LUM / 2), "bottom rear stringer %s" % f(w), size=NOTE)
        c.text(mid, q(fst0 + LUM / 2), "bottom front stringer %s" % f(w), size=NOTE)
        c.text(mid, q(TV_CARCASS / 2 + 1.7), "TV bottom %d" % (i + 1),
               size=NOTE, color="#5b4a2e")
    fs0 = q(SLEEPER_FRONT_FACE - LUM)
    for i, cx in enumerate(CROSS_CTR):
        x0 = q(cx - LUM / 2)
        c.rect(x0, LUM, LUM, CROSS_LEN, fill=MAT["2x2"], sw=1.2)     # cross block 12-3/8
        c.text(cx, q(LUM + CROSS_LEN / 2), "cross block %d" % (i + 1),
               size=8.0, rotate=-90)
        for sy in (0.0, fs0):                                        # sleepers below
            c.rect(x0, sy, LUM, LUM, fill="none", stroke="#8b3a00", sw=1.4, dash="4,2")
    for x in BOT_JOINTS:
        c.line(x, -0.3, x, q(TV_CARCASS + 0.3), stroke=DIM, sw=1.3, dash="10,3,2,3")

    c.dim_v(0, TV_CARCASS, -2.6, offset_px=-11)
    c.dim_v(LUM, q(LUM + CROSS_LEN), -6.2, offset_px=-11)
    c.dim_v(0, SLEEPER_FRONT_FACE, -9.8, offset_px=-11)
    c.dim_h(0, TV_LEN, -11.8, text=f(TV_LEN))
    c.dim_h(0, BOT_JOINTS[0], -7.2, text=f(BOT_JOINTS[0]) + " bottom joint over cross block 2")
    c.dim_h(0, BOT_JOINTS[1], -2.6, text=f(BOT_JOINTS[1]) + " bottom joint over cross block 4")
    for i, cx in enumerate(CROSS_CTR[1:6]):
        c.dim_h(0, cx, q(TV_CARCASS + 4.4 + 4.6 * i),
                text=f(cx) + " cross block %d centre = divider %d centre" % (i + 2, i + 1))
    c.label(2.0, q(TV_CARCASS + 27.0),
            ["the three TV bottoms are 1/2 spruce, 15-3/8 deep, jointed over cross blocks 2 and 4",
             "dashed squares = 2x2 sleepers under the ladder, one under each end of every cross block:",
             "rear sleepers tight to the wall, front sleepers with their front face 12-7/8 from the wall"],
            size=NOTE, anchor="start")
    _caption(c, TV_LEN / 2, q(TV_CARCASS + 30.6),
             "plan of the bottom ladder - rails, dividers, slab and doors omitted")
    return c.save(path)


DIAGRAMS = [
    ("03-tall-box-section.svg", tall_box_section,
     "Tall cabinet side section: top and bottom on their ends, rails at the rear, back over the rear edges, door in front"),
    ("03-tall-box-front.svg", tall_box_front,
     "Tall cabinet front elevation with the MDF side removed: pocket screws go in the ends of the top, bottom and rails, never in the sides"),
    ("03-ladder-section.svg", ladder_section,
     "TV ladder cross-section through one bay, with lines A to F set out from the finished floor"),
    ("03-ladder-elevation.svg", ladder_elevation,
     "TV ladder front elevation of the whole 181 run: rail and stringer joints, five dividers, seven cross blocks, six top front stringers"),
    ("03-ladder-plan.svg", ladder_plan,
     "Bottom ladder in plan: two stringers, seven cross blocks 12-3/8, fourteen sleepers, and the bottom joints over cross blocks 2 and 4"),
]


def build(outdir):
    out = []
    for name, fn, caption in DIAGRAMS:
        fn("%s/%s" % (outdir.rstrip("/"), name))
        out.append((name, caption))
    return out


if __name__ == "__main__":
    print(build("."))
