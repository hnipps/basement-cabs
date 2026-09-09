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
DRYWALL = 0.5          # 1/2 drywall (CUTLIST notes "Wall screws")
STUD_D = LUM           # a 2x4 stud is 1-1/2 deep behind the drywall
SCREW_LEN = 4.0        # #10 x 4" wall screws (guide 3 step 2, CUTLIST notes)

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
PIN_PITCH = 32 / 25.4         # 32 mm shelf-pin pitch (guide 4)
POCKET_REAR = q(1.5)          # "first one 1-1/2 from an edge" (guide 3 "Joinery")
POCKET_FRONT = 3.0            # front pocket setback, chosen to clear the 2 zone
KEEP_CLEAR = 2.0              # "2" clear of the front-left corner" (guide 3)
RAIL_POCKET_INSET = 1.0       # 2 pockets per rail end, 1 from each long edge (drawing choice)
KICK_H = q(4 + 15 / 16.)      # kick height, both runs (CUTLIST 5/8 MDF table)

# Tall door hinge / plate heights from the bottom edge (guide 4 "Mounting plates").
TALL_HINGES = [q(3.5), q(22 + 7 / 16.), q(41 + 3 / 8.), q(60 + 1 / 4.), q(79 + 3 / 16.)]
# Shelf pin rows: 32 mm pitch up from PIN_LOW, skipping any row within 1 of a hinge
# plate height (guide 4 "Shelf pins"). Three shelves, roughly quartering the opening.
_ROWS = [q(PIN_LOW + k * PIN_PITCH) for k in range(200)
         if PIN_LOW + k * PIN_PITCH <= PIN_HIGH]
_ROWS = [r for r in _ROWS if all(abs(r - h) >= 1.0 for h in TALL_HINGES)]
_OPEN = [T58 + (TALL_H - 2 * T58) * k / 4.0 for k in (1, 2, 3)]
SHELF_PINS = [min(_ROWS, key=lambda r, t=t: abs(r - t)) for t in _OPEN]

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
DIV_H = q(12.5)                  # TV divider 12-1/2 (CUTLIST 1/2 spruce table)
NOTCH_UP = RAIL_H                # rail notch 3-1/2 up x 1-1/2 in (CUTLIST notes)
NOTCH_IN = LUM
DOOR_H = q(14 + 3 / 8.)          # TV door 29-63/64 x 14-3/8 (CUTLIST 5/8 MDF table)
DOOR_REVEAL = q(0.125)           # 1/8 under the slab (CUTLIST notes "Doors")
# TV door plates: 1-1/2 and 8-7/8 above the divider's bottom edge (guide 4).
PLATE_UP = [q(1.5), q(8 + 7 / 8.)]
PACKER_T = T58                   # 5/8 MDF packer on the tall cabinet's right face
PACKER_W = 3.0                   # packer 3 wide in the depth direction (guide 4)

# --- TV run length and positions -------------------------------------------
TV_LEN = 181.0                   # TV run width (CUTLIST header)
WALL_LEN = q(199 + 3 / 8.)       # wall length (CUTLIST header) = TALL_W + TV_LEN
# Divider LEFT faces from the tall cabinet's right side. CUTLIST "TV divider
# positions" gives 30.209 / 60.313 / 90.417 / 120.521 / 150.625; snapped to 64ths
# these are exactly the guide's 30-13/64, 60-5/16, 90-27/64, 120-33/64, 150-5/8.
DIV_LEFT = [q(30.209), q(60.313), q(90.417), q(120.521), q(150.625)]
DIV_CTR = [q(x + T12 / 2) for x in DIV_LEFT]   # cross block / joint centres
# Rail joints (CUTLIST "Solid lumber": joints at 78-45/64 and 139-3/64 from the
# left wall, i.e. 60-21/64 and 120-43/64 from the tall cabinet side).
RAIL_LEN = q(60 + 21 / 64.)
RAIL_JOINTS = [RAIL_LEN, q(120 + 43 / 64.)]
# The three rails as cut: 60-21/64 + 60-11/32 + 60-21/64 = 181 exactly, the middle
# one out of the 6-1/2' board (CUTLIST "Solid lumber - 2x4 on hand").
RAIL_MID = q(60 + 11 / 32.)
RAIL_LENS = [RAIL_LEN, RAIL_MID, RAIL_LEN]
# Bottom stringer / bottom pieces (CUTLIST 1/2 spruce + 2x2 tables).
BOT_PIECES = [q(60 + 9 / 16.), q(60 + 13 / 64.), q(60 + 15 / 64.)]
BOT_JOINTS = [BOT_PIECES[0], q(BOT_PIECES[0] + BOT_PIECES[1])]   # 60-9/16, 120-49/64
# Slab: two pieces 90-43/64 + 90-21/64, jointed over divider 3's centre (CUTLIST 1/2 MDF).
SLAB_PIECES = [q(90 + 43 / 64.), q(90 + 21 / 64.)]
SLAB_JOINT = SLAB_PIECES[0]
# Cross blocks: left end, the five divider centres, right end (guide 3 step 5).
CROSS_CTR = [q(LUM / 2)] + DIV_CTR + [q(TV_LEN - LUM / 2)]
# Top front stringers, bays 1 to 6 (CUTLIST 2x2 table).
TOP_FRONT = [q(30 + 13 / 64.)] + [q(29 + 39 / 64.)] * 4 + [q(29 + 7 / 8.)]
END_BLOCK = 3.0                  # 2x2 offcut end block, length to suit (guide 3 step 9)
# Door 1's packer runs from line C up to the underside of the bay 1 end block, i.e.
# LINE_E - 1-1/2 = 17-15/16, so the block sits directly on top of it: 11 tall (guide 4).
PACKER_TALL = q(LINE_E - LUM - LINE_C)

CAP = 9.5                        # caption / label font size
NOTE = 9.0
HINGE = "#3b6ea5"                # hinge plate marks and the A-F reference lines


def _caption(c, x, y, text, anchor="middle"):
    c.text(x, y, text, size=CAP, anchor=anchor, color="#555")


def _shade(col, k):
    """Lighten (k > 1) or darken (k < 1) a #rrggbb fill, for the oblique faces."""
    v = [int(col[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(round(x * k)))) for x in v)


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

    def pocket(self, x, y, into=1.0):
        """Pocket screw: circle on the joint line, stub pointing into the side."""
        c = self.circle(x, y, 2.4, fill="white", stroke=LINE)
        self.line(x, y, x + into, y, stroke=LINE, sw=0.8)
        return c

    def plate(self, x, y, w=0.45, h=1.0):
        """Hinge mounting-plate mark on a face; (x, y) is the face at the plate centre."""
        self.rect(x, q(y - h / 2), w, h, fill=HINGE, stroke=HINGE, sw=0.6)

    def arrow(self, x1, y1, x2, y2, head=0.5, color=LINE):
        """Straight arrow with a solid head at (x2, y2), for the axis key."""
        self.line(x1, y1, x2, y2, stroke=color, sw=1.1)
        dx, dy = x2 - x1, y2 - y1
        n = (dx * dx + dy * dy) ** 0.5 or 1.0
        ux, uy = dx / n, dy / n
        bx, by = x2 - ux * head, y2 - uy * head
        self.poly([(x2, y2), (bx - uy * head * 0.35, by + ux * head * 0.35),
                   (bx + uy * head * 0.35, by - ux * head * 0.35)], fill=color, stroke=color, sw=0.6)


# ---------------------------------------------------------------------------
# 1. tall box, side section
# ---------------------------------------------------------------------------
def tall_box_section(path):
    c = Sheet(73, 107, scale=7.5, flip_y=True, x_off=8.2, y_off=12.0,
              title="Tall cabinet, side section (rear at left, front at right)")
    # cut plane between the sides: the left side's inner face is the background
    c.rect(0, 0, TALL_D, TALL_H, fill=MAT["spruce58"], sw=1.0)
    c.rect(-T18, 0, T18, TALL_H, fill=MAT["hardboard"])                 # back
    c.rect(0, 0, TALL_D, T58, fill=MAT["spruce58"], sw=1.6)             # bottom
    c.rect(0, TALL_H - T58, TALL_D, T58, fill=MAT["spruce58"], sw=1.6)  # top
    c.rect(0, T58, LUM, RAIL_H, fill=MAT["2x4"], sw=1.4)                # bottom rail
    c.rect(0, TALL_H - T58 - RAIL_H, LUM, RAIL_H, fill=MAT["2x4"], sw=1.4)  # top rail
    # the door's rear face sits on the carcass front edge, not on the back's plane
    c.rect(TALL_D, 0, T58, TALL_H, fill=MAT["mdf58"], sw=1.4)           # door
    for x in (PIN_INSET, TALL_D - PIN_INSET):
        c.line(x, PIN_LOW, x, PIN_HIGH, stroke="#666", sw=0.9, dash="5,4")
        c.circle(x, PIN_LOW, 1.6, fill="#666")
        c.circle(x, PIN_HIGH, 1.6, fill="#666")

    lx = q(TALL_D + T58 + 1.8)
    for (ax, ay), ly, lines in [
        ((TALL_D / 2, TALL_H - T58 / 2), 92.5,
         ["tall top 23-11/16 x 17-1/8 (5/8 spruce),", "on its end, flush front and rear"]),
        ((LUM / 2, TALL_H - T58 - RAIL_H / 2), 81.0,
         ["tall hanging rail 17-1/8 x 3-1/2 (2x4),", "tight under the top, flush rear"]),
        ((q(TALL_D + T58 / 2), 64.0), 64.0, ["tall door, 5/8 MDF, rear face on", "the carcass front edge"]),
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

    c.dim_v(0, TALL_H, -0.9, offset_px=-13, witness=0)
    c.dim_h(0, TALL_D, -1.6, offset_px=13, witness=0)
    c.dim_h(-T18, TALL_D, -4.4, text=f(TALL_D_BACK) + " with the back", offset_px=13, witness=0)
    c.dim_h(-T18, q(TALL_D + T58), -7.2, text=f(TALL_D_DOOR) + " with the door",
            offset_px=13, witness=0)
    c.dim_v(T58, T58 + RAIL_H, -2.8, offset_px=-12, witness=0, fit="along")
    c.dim_h(0, LUM, q(T58 + RAIL_H + 1.4), offset_px=-12, witness=q(T58 + RAIL_H))
    _caption(c, -7.0, -11.2, "side section - the cut plane runs between the two sides",
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
    c.leader(T58, TALL_H / 2, -4.8, TALL_H / 2)
    c.text(q(TALL_W + 2.6), 62.0, "tall right side (5/8 MDF) removed to draw",
           size=NOTE, rotate=-90, color="#777")
    c.leader(TALL_W, 62.0, q(TALL_W + 2.2), 62.0)
    c.dim_h(0, TALL_W, -1.6, offset_px=13, witness=0)
    c.dim_h(T58, q(TALL_W - T58), -4.2, offset_px=13, witness=0)
    c.dim_v(0, TALL_H, -0.9, offset_px=-13, witness=0)
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
    c.dim_h(px0, q(px0 + TALL_INNER), q(py0 - 2.4), offset_px=13, witness=py0)
    c.dim_v(py0, q(py0 + TALL_D), q(px0 - 1.4), offset_px=-12, witness=px0)
    c.dim_v(q(py0 + TALL_D - POCKET_REAR), q(py0 + TALL_D), q(px0 + TALL_INNER + 1.3),
            offset_px=11, rotate=90, witness=q(px0 + TALL_INNER))
    c.dim_v(py0, q(py0 + TALL_D - depths[2]), q(px0 + TALL_INNER + 1.3),
            offset_px=11, rotate=90, witness=q(px0 + TALL_INNER))
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
    c = Sheet(39, 35, scale=23.0, flip_y=True, x_off=10.5, y_off=8.4,
              title="TV ladder, cross-section through one bay (wall at left, floor at bottom)")
    FL = 1.1                                   # floor slab, drawing depth only
    stud0 = q(-DRYWALL - STUD_D)               # rear face of the stud
    stud_lo, stud_hi = 12.5, q(LINE_F + 0.9)   # the stud is drawn at the rail only
    c.rect(stud0, stud_lo, STUD_D, q(stud_hi - stud_lo), fill=MAT["waste"], sw=1.0,
           dash="7,4")   # drawn at the rail only
    c.rect(-DRYWALL, 0, DRYWALL, q(LINE_F + 2.6), fill=MAT["wall"], sw=1.0)   # 1/2 drywall
    c.rect(stud0, -FL, q(TV_DEPTH + 1.4 - stud0), FL, fill=MAT["floor"], sw=1.0)
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

    # #10 x 4 through the rail into the stud: 1-1/2 rail + 1/2 drywall = 2, then the
    # stud is only 1-1/2 deep, so the last 1/2 of the screw comes out behind it.
    sc_y = q(LINE_D + RAIL_H / 2)
    sc_tip = q(LUM - SCREW_LEN)
    c.line(sc_tip, sc_y, LUM, sc_y, stroke="#8b3a00", sw=2.0)
    c.line(LUM, q(sc_y - 0.35), LUM, q(sc_y + 0.35), stroke="#8b3a00", sw=2.0)

    # lines A to F, labelled at the far left
    nudge = {"A": -0.30, "B": -0.38, "C": 0.38, "D": 0.0, "E": -0.42, "F": 0.42}
    for name, h, _what in LINES:
        c.line(-2.9, h, TV_DEPTH + 0.9, h, stroke=HINGE, sw=0.8, dash="9,4")
        ly = h + nudge[name]
        c.leader(-2.9, h, -3.2, ly, dot=False)
        c.text(-3.4, ly, "%s  %s" % (name, f(h)), size=CAP, anchor="end", color=HINGE)

    # front-side parts: labels down the right, leaders short and level
    lx = q(TV_DEPTH + 1.6)
    for (ax, ay), ly, lines in [
        ((13.0, q(LINE_F - T12 / 2)), 23.6,
         ["TV top slab (1/2 MDF),", "16 deep, line E to line F"]),
        ((q(TV_CARCASS - LUM / 2), q(LINE_E - LUM / 2)), 21.0,
         ["top front stringer, bay 2 (2x2),", "29-39/64, top on line E"]),
        ((q(TV_DEPTH - T58 / 2), 12.6), 13.0,
         ["TV door (5/8 MDF) 29-63/64 x 14-3/8,", "1/8 under the slab"]),
        ((10.4, 10.4), 10.2, ["divider 2 (1/2 spruce)", "15-3/8 x 12-1/2, on the bottom"]),
        ((7.0, q(LINE_B + T12 / 2)), 7.8, ["TV bottom 1 (1/2 spruce), 15-3/8 deep,", "rear edge scribed to the wall"]),
        ((q(TV_CARCASS - LUM / 2), q(LINE_A + LUM / 2)), 5.9,
         ["bottom front stringer (2x2),", "front face 15-3/8 from the wall"]),
        ((10.4, q(LINE_A + LUM / 2)), 4.0, ["cross block 12-3/8 between the", "stringers (behind the front one)"]),
        ((q(kick_face - T58 / 2), 2.4), 2.2, ["kick, TV (5/8 MDF), face 2-1/2", "behind the door face"]),
        ((q(fs0 + LUM / 2), 1.4), 0.4, ["front sleeper (2x2), cut 4-3/4,", "shimmed up to line A"]),
    ]:
        c.leader(ax, ay, lx - 0.3, ly)
        c.label(lx, ly, lines, size=NOTE, anchor="start")

    # rear-side parts: the rail mid-left, the two rear pieces bottom-left
    c.leader(q(LUM / 2), 16.8, -3.2, 12.2)
    c.label(-3.4, 12.4, ["TV hanging rail (2x4),", "60-21/64 x 3-1/2,", "top on line E"],
            size=NOTE, anchor="end")
    c.leader(q(LUM / 2), q(LINE_A + LUM / 2), -1.1, 2.6)
    c.label(-1.4, 2.7, ["bottom rear stringer (2x2),", "tight to the wall, top on line B"],
            size=NOTE, anchor="end")
    c.leader(q(LUM / 2), 1.4, -1.1, 0.4)
    c.label(-1.4, 0.5, ["rear sleeper (2x2), cut 4-3/4"], size=NOTE, anchor="end")
    c.text(q(-DRYWALL / 2), 5.6, "1/2 drywall", size=8.0, rotate=-90, color="#555")
    c.text(q(stud0 + STUD_D / 2), 14.4, "2x4 stud", size=8.0, rotate=-90, color="#555")

    # the screw note sits above the slab, its leader straight up the screw line
    c.leader(-1.2, sc_y, -1.2, 24.4, dot=True)
    c.label(q(sc_tip + 0.3), 25.4,
            ["#10 x 4 through the rail into the stud: rail 1-1/2 + drywall 1/2 = 2 before",
             "the stud, then only 1-1/2 of stud - the last 1/2 of the screw stands out behind it"],
            size=NOTE, anchor="start")
    c.leader(NOTCH_IN, 18.4, 2.6, 21.4)
    c.label(2.8, 21.5, ["rail notch: 3-1/2 up x 1-1/2 in,", "rear top corner of every divider"],
            size=NOTE, anchor="start")

    # dimensions
    c.dim_h(0, NOTCH_IN, q(LINE_F + 3.4), offset_px=-11, witness=LINE_E, fit="right")
    c.dim_h(-DRYWALL, LUM, 11.3, text=f(LUM + DRYWALL) + " to the stud face",
            witness=stud_lo, fit="right")
    c.dim_h(stud0, -DRYWALL, 11.3, text=f(STUD_D) + " stud", witness=stud_lo, fit="left")
    c.dim_h(0, SLEEPER_FRONT_FACE, -2.4, witness=0)
    c.dim_h(q(kick_face - T58), TV_DEPTH, -2.4, text=f(KICK_RECESS) + " recess", witness=0)
    c.dim_h(0, TV_CARCASS, -3.9, text=f(TV_CARCASS) + " carcass", witness=0)
    c.dim_h(TV_CARCASS, TV_DEPTH, -3.9, text=f(T58) + " door", witness=0)
    c.dim_h(0, TV_DEPTH, -5.4, text=f(TV_DEPTH) + " overall depth", witness=0)
    c.dim_v(LINE_C, LINE_E, 12.2, offset_px=-11, witness=TV_CARCASS)
    c.dim_v(LINE_D, LINE_E, q(stud0 - 0.6), offset_px=-11, witness=stud0)
    _caption(c, 5.0, -7.4,
             "cross-section, bay 2 - lines A to F are heights above the finished floor at the high spot")
    return c.save(path)


# ---------------------------------------------------------------------------
# 4. whole-wall front elevation, doors off
# ---------------------------------------------------------------------------
def ladder_elevation(path):
    c = Sheet(209, 141, scale=6.0, flip_y=True, x_off=24.0, y_off=46.0,
              title="Whole wall, front elevation with the doors off "
                    "(tall cabinet at the left, 181 TV ladder to the right wall)")
    TX0 = q(-TALL_W)              # tall cabinet's left face; x = 0 is its right face
    TZ0, TZ1 = LINE_A, q(LINE_A + TALL_H)
    c.rect(q(TX0 - 1.6), 0, 1.6, q(TZ1 + 2.0), fill=MAT["wall"], sw=1.0)   # left wall
    c.rect(TV_LEN, 0, 1.6, q(LINE_F + 2.0), fill=MAT["wall"], sw=1.0)      # right wall
    c.line(q(TX0 - 1.6), 0, q(TV_LEN + 1.6), 0, stroke=LINE, sw=1.4)       # floor
    c.text(q(TX0 - 0.8), 30.0, "left wall", size=NOTE, rotate=-90, color="#555")
    c.text(q(TV_LEN + 0.8), 11.0, "right wall", size=NOTE, rotate=-90, color="#555")

    # kicks: tall flush, TV recessed 2-1/2 (dashed - it sits behind the door plane)
    c.rect(TX0, 0, TALL_W, KICK_H, fill=MAT["mdf58"], sw=1.2)
    c.rect(0, 0, TV_LEN, KICK_H, fill=MAT["mdf58"], sw=1.0, dash="7,4")
    c.text(q(TV_LEN / 2), 1.5, "kick, TV (5/8 MDF), 181 in two pieces, recessed 2-1/2",
           size=NOTE, box=True)
    c.text(q(TX0 + TALL_W / 2), 1.5, "kick, tall", size=8.0, box=True)

    # --- tall cabinet interior, door and right side drawn, shelves on pins ----
    c.rect(TX0, TZ0, TALL_W, TALL_H, fill=MAT["hardboard"], sw=1.0, opacity=0.35)  # back
    c.rect(TX0, TZ0, T58, TALL_H, fill=MAT["spruce58"], sw=1.4)            # left side
    c.rect(q(-T58), TZ0, T58, TALL_H, fill=MAT["mdf58"], sw=1.4)           # right side (MDF)
    IX0, IW = q(TX0 + T58), TALL_INNER
    c.rect(IX0, TZ0, IW, T58, fill=MAT["spruce58"], sw=1.4)                # bottom
    c.rect(IX0, q(TZ1 - T58), IW, T58, fill=MAT["spruce58"], sw=1.4)       # top
    for y0 in (q(TZ0 + T58), q(TZ1 - T58 - RAIL_H)):                       # two 2x4 rails
        c.rect(IX0, y0, IW, RAIL_H, fill=MAT["2x4"], sw=1.2)
        c.text(q(IX0 + IW / 2), q(y0 + RAIL_H / 2), "2x4 rail 17-1/8", size=8.0, box=True)
    for h in SHELF_PINS:                                                   # three shelves
        y0 = q(TZ0 + h)
        c.rect(IX0, y0, IW, T58, fill=MAT["spruce58"], sw=1.2)
        for x in (q(IX0 + 0.6), q(IX0 + IW - 0.6)):
            c.circle(x, q(y0 - 0.35), 1.5, fill="#555")
    for h in TALL_HINGES:                                                  # 5 plates
        c.plate(IX0, q(TZ0 + h))
    c.leader(q(IX0 + IW / 2), q(TZ0 + SHELF_PINS[2]), 6.0, 72.0)
    c.label(6.4, 72.0,
            ["tall cabinet, door off: 5/8 spruce carcass, 5/8 MDF right side,",
             "1/8 hardboard back, two 2x4 rails 17-1/8, three shelves on pins",
             "(rows shown are 32 mm pin positions clear of the hinge plates)"],
            size=NOTE, anchor="start")
    c.leader(IX0, q(TZ0 + TALL_HINGES[3]), 6.0, 62.0)
    c.label(6.4, 62.0, ["five hinge plates on the left side's inner face, wall side:",
                        "3-1/2, 22-7/16, 41-3/8, 60-1/4, 79-3/16 up from the bottom"],
            size=NOTE, anchor="start")

    # --- TV ladder ------------------------------------------------------------
    edges = [0.0] + RAIL_JOINTS + [TV_LEN]                # three 2x4 rails end to end
    for i in range(3):
        c.rect(edges[i], LINE_D, q(edges[i + 1] - edges[i]), RAIL_H, fill=MAT["2x4"], sw=1.2)
        c.text(q(edges[i] + 15.0), q(LINE_D + 0.8),
               "TV hanging rail %d, %s" % (i + 1, f(RAIL_LENS[i])), size=NOTE, box=True)
    bedges = [0.0] + BOT_JOINTS + [TV_LEN]                # stringers and bottoms
    for i in range(3):
        w = q(bedges[i + 1] - bedges[i])
        c.rect(bedges[i], LINE_A, w, LUM, fill=MAT["2x2"], sw=1.2)
        c.rect(bedges[i], LINE_B, w, T12, fill=MAT["spruce12"], sw=1.2)
        c.text(q(bedges[i] + 15.0), q(LINE_A + LUM / 2),
               "stringers %s" % f(w), size=8.0, box=True)
        c.text(q(bedges[i] + 15.0), 11.5, "TV bottom %d, %s x 15-3/8" % (i + 1, f(w)),
               size=8.0, color="#5b4a2e", box=True)
    for i, cx in enumerate(CROSS_CTR):                    # seven cross blocks, hidden
        c.rect(q(cx - LUM / 2), LINE_A, LUM, LUM, fill="none", sw=0.9, dash="3,2")
        tx = cx + (2.6 if i == 0 else (-2.6 if i == len(CROSS_CTR) - 1 else 0.0))
        c.text(tx, 3.5, "cb %d" % (i + 1), size=8.0, color="#777", box=True)
        c.leader(cx, LINE_A, tx, 4.1, dot=False)
    for i, x in enumerate(DIV_LEFT):                      # five dividers, then plates
        c.rect(x, LINE_C, T12, DIV_H, fill=MAT["spruce12"], sw=1.3)
        for up in PLATE_UP:
            c.plate(q(x + T12), q(LINE_C + up))
        c.text(q(x + T12 / 2), q(LINE_F + 1.4), "div %d" % (i + 1), size=8.0, box=True)
        c.leader(q(x + T12 / 2), LINE_E, q(x + T12 / 2), q(LINE_F + 0.8), dot=False)
    # door 1's plates land on a 5/8 packer screwed to the tall cabinet's right face
    c.rect(0, LINE_C, PACKER_T, PACKER_TALL, fill="none", sw=1.0, dash="4,3")
    for up in PLATE_UP:
        c.plate(PACKER_T, q(LINE_C + up))
    bays = [(0.0, DIV_LEFT[0])]
    bays += [(q(DIV_LEFT[k - 1] + T12), DIV_LEFT[k]) for k in range(1, 5)]
    bays += [(q(DIV_LEFT[4] + T12), TV_LEN)]
    for i, (x0, x1) in enumerate(bays):                   # six top front stringers
        c.rect(x0, q(LINE_E - LUM), q(x1 - x0), LUM, fill=MAT["2x2"], sw=1.2)
        c.text(q((x0 + x1) / 2), q(LINE_E - LUM / 2),
               "bay %d stringer %s" % (i + 1, f(TOP_FRONT[i])), size=7.5, box=True)
    for x0 in (0.0, q(TV_LEN - END_BLOCK)):               # end blocks behind the stringers
        c.rect(x0, q(LINE_E - LUM), END_BLOCK, LUM, fill="none", sw=1.0, dash="2,2")
    # slab, two pieces jointed over divider 3
    for x0, w in ((0.0, SLAB_PIECES[0]), (SLAB_JOINT, SLAB_PIECES[1])):
        c.rect(x0, LINE_E, w, T12, fill=MAT["mdf12"], sw=1.3)
    c.line(SLAB_JOINT, LINE_E, SLAB_JOINT, LINE_F, stroke=DIM, sw=1.6)

    # notes above the ladder, each leader short and vertical-ish
    c.leader(q(END_BLOCK / 2), q(LINE_E - LUM), 8.0, 25.0)
    c.label(8.4, 25.2, ["2x2 offcut end block screwed to the tall cabinet's right side,",
                        "behind the stringer; %s packer %s tall under the 2x2 end block,"
                        % (f(PACKER_T), f(PACKER_TALL)),
                        "both on the tall cabinet's right face - it carries door 1's plates"],
            size=NOTE, anchor="start")
    c.leader(q(TV_LEN - END_BLOCK / 2), q(LINE_E - LUM), q(TV_LEN - 8.0), 25.0)
    c.label(q(TV_LEN - 8.4), 25.2, ["end block to the right wall"], size=NOTE, anchor="end")
    c.leader(SLAB_JOINT, LINE_F, q(SLAB_JOINT + 6.0), 33.0)
    c.label(q(SLAB_JOINT + 6.4), 33.2,
            ["TV top slab (1/2 MDF), 16 deep: %s + %s, joint over divider 3"
             % (f(SLAB_PIECES[0]), f(SLAB_PIECES[1]))], size=NOTE, anchor="start")
    c.leader(q(DIV_LEFT[1] + T12), q(LINE_C + PLATE_UP[1]), q(DIV_LEFT[1] + 9.0), 29.0)
    c.label(q(DIV_LEFT[1] + 9.4), 29.2,
            ["hinge plates on every divider's right face and on the packer,",
             "1-1/2 and 8-7/8 above the divider bottom (guide 4)"], size=NOTE, anchor="start")

    # --- dimensions: joints above the ladder, positions below the drawing -----
    c.dim_h(0, RAIL_JOINTS[0], 41.0, text=f(RAIL_JOINTS[0]) + " rail joint 1 (in divider 2)",
            witness=LINE_E)
    c.dim_h(0, RAIL_JOINTS[1], 47.0, text=f(RAIL_JOINTS[1]) + " rail joint 2 (in divider 4)",
            witness=LINE_E)
    c.dim_h(0, SLAB_JOINT, 53.0, text=f(SLAB_JOINT) + " slab joint over divider 3",
            witness=LINE_F)
    c.dim_v(TZ0, TZ1, q(TX0 - 2.6), text=f(TALL_H) + " tall cabinet", offset_px=-12, witness=TX0)
    c.dim_h(TX0, 0.0, q(TZ1 + 1.4), text=f(TALL_W) + " tall cabinet", offset_px=11, witness=TZ1)
    c.label(8.0, 34.0,
            ["bottom stringers: the same three lengths front and rear (see the plan).",
             "TV rails: %s + %s + %s = %s, joints at %s and %s"
             % (f(RAIL_LENS[0]), f(RAIL_LENS[1]), f(RAIL_LENS[2]), f(TV_LEN),
                f(RAIL_JOINTS[0]), f(RAIL_JOINTS[1]))], size=NOTE, anchor="start")

    c.dim_h(0, BOT_JOINTS[0], -4.0,
            text=f(BOT_JOINTS[0]) + " stringer / bottom joint 1", witness=LINE_A)
    c.dim_h(0, BOT_JOINTS[1], -8.5,
            text=f(BOT_JOINTS[1]) + " stringer / bottom joint 2", witness=LINE_A)
    for i, x in enumerate(DIV_LEFT):
        c.dim_h(0, x, q(-13.0 - 4.5 * i), text=f(x) + " to divider %d left face" % (i + 1),
                witness=LINE_C)
    c.dim_h(0, TV_LEN, -35.5, text=f(TV_LEN) + " TV run, tall cabinet side to right wall",
            witness=LINE_A)
    c.dim_h(TX0, TV_LEN, -40.0, text=f(WALL_LEN) + " wall", witness=(TZ0, LINE_A))
    _caption(c, q(TV_LEN / 2), -44.0,
             "whole wall, doors off - rail joints hide inside dividers 2 and 4, "
             "the slab joint lands over divider 3")
    return c.save(path)


# ---------------------------------------------------------------------------
# 5. TV ladder, exploded oblique of one bay segment
# ---------------------------------------------------------------------------
# Cabinet oblique: x runs along the run, z up, d back to the wall at 45 degrees with
# the depth foreshortened 1:2, so a model point (x, d, z) lands at (x + d/2, z + d/2).
def _o(x, d, z):
    return (x + d / 2.0, z + d / 2.0)


def _obox(c, x0, dx, d0, dd, z0, dz, fill, sw=1.1):
    """Three visible faces of a box: front (d = d0), top (z = z0 + dz), right (x = x0 + dx)."""
    x1, d1, z1 = x0 + dx, d0 + dd, z0 + dz
    c.poly([_o(x1, d0, z0), _o(x1, d1, z0), _o(x1, d1, z1), _o(x1, d0, z1)],
           fill=_shade(fill, 0.86), sw=sw)
    c.poly([_o(x0, d0, z1), _o(x1, d0, z1), _o(x1, d1, z1), _o(x0, d1, z1)],
           fill=_shade(fill, 1.06), sw=sw)
    c.poly([_o(x0, d0, z0), _o(x1, d0, z0), _o(x1, d0, z1), _o(x0, d0, z1)],
           fill=fill, sw=sw)


def ladder_exploded(path):
    # heights relative to line A, so the drawing keeps guide 3's spacings
    RB, RC, RD, RE, RF = (q(v - LINE_A) for v in (LINE_B, LINE_C, LINE_D, LINE_E, LINE_F))
    DW = TV_CARCASS                       # wall at d = 15-3/8, front faces at d = 0
    SEG = q(TOP_FRONT[1] + T12)           # one bay 2 pitch: 29-39/64 stringer + a divider
    SEGR = q(SEG + LUM / 2)               # continuous parts run on past the divider
    DX0 = q(SEG - T12)                    # divider left face
    CB0 = q(DX0 + T12 / 2 - LUM / 2)      # cross block, centred under the divider
    LIFT = {"bot": 0.0, "pan": 5.0, "div": 11.0, "rail": 19.0, "slab": 31.0}

    c = Sheet(88, 62, scale=11.0, flip_y=True, x_off=24.0, y_off=5.6,
              title="TV ladder, exploded oblique of one bay segment")

    # 1. bottom ladder: rear and front 2x2 stringers with a cross block between them
    z = LIFT["bot"]
    _obox(c, 0, SEGR, q(DW - LUM), LUM, z, LUM, MAT["2x2"])          # rear stringer
    _obox(c, CB0, LUM, LUM, CROSS_LEN, z, LUM, MAT["2x2"])           # cross block
    _obox(c, 0, SEGR, 0, LUM, z, LUM, MAT["2x2"])                    # front stringer
    # 2. 1/2 spruce bottom
    z = q(LIFT["pan"] + RB)
    _obox(c, 0, SEGR, 0, DW, z, T12, MAT["spruce12"])
    # 3. notched 1/2 spruce divider, and the short top-front 2x2 stringer beside it
    z = q(LIFT["div"] + RC)
    dv_top = q(z + DIV_H)
    ntch_z = q(z + (RD - RC))
    x1 = q(DX0 + T12)
    face = [_o(x1, 0, z), _o(x1, DW, z), _o(x1, DW, ntch_z),
            _o(x1, q(DW - NOTCH_IN), ntch_z), _o(x1, q(DW - NOTCH_IN), dv_top),
            _o(x1, 0, dv_top)]
    c.poly(face, fill=_shade(MAT["spruce12"], 0.86), sw=1.1)          # right face, notched
    c.poly([_o(DX0, 0, dv_top), _o(x1, 0, dv_top), _o(x1, q(DW - NOTCH_IN), dv_top),
            _o(DX0, q(DW - NOTCH_IN), dv_top)],
           fill=_shade(MAT["spruce12"], 1.06), sw=1.0)                # top edge
    c.poly([_o(DX0, q(DW - NOTCH_IN), ntch_z), _o(x1, q(DW - NOTCH_IN), ntch_z),
            _o(x1, DW, ntch_z), _o(DX0, DW, ntch_z)],
           fill=_shade(MAT["spruce12"], 1.06), sw=1.0)                # notch floor
    c.poly([_o(DX0, 0, z), _o(x1, 0, z), _o(x1, 0, dv_top), _o(DX0, 0, dv_top)],
           fill=MAT["spruce12"], sw=1.1)                              # front edge
    _obox(c, 0, DX0, 0, LUM, q(LIFT["div"] + RE - LUM), LUM, MAT["2x2"])
    # 4. 2x4 rail, the top-rear member, dropped through the notches
    z = q(LIFT["rail"] + RD)
    _obox(c, 0, SEGR, q(DW - LUM), LUM, z, RAIL_H, MAT["2x4"])
    # 5. 1/2 MDF slab, 16 deep: 5/8 of it overhangs the carcass front
    z = q(LIFT["slab"] + RE)
    _obox(c, 0, SEGR, q(-T58), TV_DEPTH, z, T12, MAT["mdf12"])

    # assembly path
    for gx in (q(SEG * 0.62), ):
        for z0, z1 in ((q(LUM + 0.6), q(LIFT["pan"] + RB - 0.6)),
                       (q(LIFT["pan"] + RB + T12 + 0.6), q(LIFT["div"] + RC - 0.6)),
                       (q(LIFT["div"] + RE + 0.6), q(LIFT["rail"] + RD - 0.6)),
                       (q(LIFT["rail"] + RD + RAIL_H + 0.6), q(LIFT["slab"] + RE - 0.6))):
            a, b = _o(gx, DW / 2, z0), _o(gx, DW / 2, z1)
            c.line(a[0], a[1], b[0], b[1], stroke="#888", sw=0.8, dash="5,4")

    # labels: front-side parts to the left, wall-side parts to the right
    lft, rgt = -1.6, q(SEGR + DW / 2 + 1.6)
    for (px, pd, pz), ly, lines in [
        ((q(SEGR * 0.45), 0, q(LUM / 2)), 3.0,
         ["bottom front stringer (2x2), 181 in three", "pieces 60-9/16 / 60-13/64 / 60-15/64"]),
        ((q(SEGR * 0.30), 0, q(LIFT["pan"] + RB + T12 / 2)), q(LIFT["pan"] + RB + 2.2),
         ["TV bottom (1/2 spruce), 15-3/8 deep,", "same three lengths, same joints"]),
        ((q(SEGR * 0.30), 0, q(LIFT["div"] + RE - LUM / 2)), q(LIFT["div"] + RE + 1.0),
         ["top front stringer (2x2) 29-39/64:", "SIX separate pieces, one per bay"]),
        ((q(SEGR * 0.30), q(-T58), q(LIFT["slab"] + RE + T12 / 2)), q(LIFT["slab"] + RE + 3.4),
         ["TV top slab (1/2 MDF) 16 deep,", "90-43/64 + 90-21/64 over divider 3"]),
    ]:
        a = _o(px, pd, pz)
        c.leader(a[0], a[1], lft + 0.3, ly)
        c.label(lft, ly, lines, size=NOTE, anchor="end")
    for (px, pd, pz), ly, lines in [
        ((q(SEGR * 0.75), q(DW - LUM / 2), q(LUM / 2)), 8.0,
         ["bottom rear stringer (2x2),", "tight to the wall, top on line B"]),
        ((q(CB0 + LUM / 2), q(DW / 2), LUM), 3.0,
         ["cross block 12-3/8 (2x2): one at each", "end and one under every divider"]),
        ((q(DX0 + T12), q(DW * 0.55), q(LIFT["div"] + RC + DIV_H / 2)), q(LIFT["div"] + RC + 6.0),
         ["divider (1/2 spruce) 15-3/8 x 12-1/2,", "notch 3-1/2 up x 1-1/2 in, rear top"]),
        ((q(SEGR * 0.8), q(DW - LUM), q(LIFT["rail"] + RD + RAIL_H / 2)), q(LIFT["rail"] + RD + 2.6),
         ["2x4 hanging rail 60-21/64 x 3-1/2:", "the top-rear member, to the studs"]),
    ]:
        a = _o(px, pd, pz)
        c.leader(a[0], a[1], rgt - 0.3, ly)
        c.label(rgt, ly, lines, size=NOTE, anchor="start")

    # axis key
    kx, ky = -19.0, 34.0
    c.arrow(kx, ky, q(kx + 4.0), ky)
    c.text(q(kx + 4.4), ky, "along run", size=8.0, anchor="start")
    c.arrow(kx, ky, kx, q(ky + 4.0))
    c.text(kx, q(ky + 4.6), "up", size=8.0)
    c.arrow(kx, ky, q(kx + 2.8), q(ky + 2.8))
    c.text(q(kx + 3.0), q(ky + 3.4), "to wall", size=8.0, anchor="start")
    c.label(q(kx + 1.0), q(ky - 2.6), ["cabinet oblique,", "depth foreshortened 1:2"],
            size=8.0, color="#777", anchor="start")

    c.dim_h(0, SEG, -2.6, text=f(SEG) + " one bay pitch", witness=0)
    _caption(c, q(SEGR / 2), -4.8,
             "exploded oblique, one bay segment - dashed lines are the assembly path, not gaps")
    return c.save(path)


# ---------------------------------------------------------------------------
# 6. TV ladder, plan of the bottom ladder
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

    c.dim_v(0, TV_CARCASS, -2.6, offset_px=-11, witness=0)
    c.dim_v(LUM, q(LUM + CROSS_LEN), -6.2, offset_px=-11, witness=0)
    c.dim_v(0, SLEEPER_FRONT_FACE, -9.8, offset_px=-11, witness=0)
    c.dim_h(0, TV_LEN, -11.8, text=f(TV_LEN), witness=0)
    c.dim_h(0, BOT_JOINTS[0], -7.2, text=f(BOT_JOINTS[0]) + " bottom joint over cross block 2",
            witness=0)
    c.dim_h(0, BOT_JOINTS[1], -2.6, text=f(BOT_JOINTS[1]) + " bottom joint over cross block 4",
            witness=0)
    for i, cx in enumerate(CROSS_CTR[1:6]):
        c.dim_h(0, cx, q(TV_CARCASS + 4.4 + 4.6 * i),
                text=f(cx) + " cross block %d centre = divider %d centre" % (i + 2, i + 1),
                witness=TV_CARCASS)
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
     "TV ladder cross-section through one bay, with lines A to F, the drywall and stud behind, and the #10 x 4 screw through the rail"),
    ("03-ladder-exploded.svg", ladder_exploded,
     "Exploded oblique of one ladder bay: stringers and cross block, bottom, notched divider, 2x4 rail, top-front stringer, slab"),
    ("03-ladder-elevation.svg", ladder_elevation,
     "Whole-wall front elevation with the doors off: tall cabinet interior and the 181 TV ladder, joints, dividers, hinge plates and the slab"),
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
