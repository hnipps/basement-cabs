"""Diagrams for guide 6, "Installation".

Every number below is traced to CUTLIST.md or to guide 3's "TV ladder" height table,
which guide 6 delegates to. Labels are produced with ``frac()`` from the same constants
that place the geometry, so a label can never disagree with the drawing.

Five diagrams, one idea each:
  06-wall-elevation.svg      the whole rear wall: lines A/E/F, stud band, rail heights
  06-sleeper-plan.svg        all 18 sleepers in plan, dimensioned from the left wall
  06-tall-fixing-section.svg screw stacks at a rail, plus the leaning-left-wall shim
  06-kick-plan.svg           the three kick planes and the 10-15/16 return
  06-order.svg               the install sequence as a strip
"""
from svgkit import Canvas, MAT, frac, LINE, DIM

# --------------------------------------------------------------------------------------
# Constants.  Fractions are written as exact binary sums so nothing rounds.
# --------------------------------------------------------------------------------------

# CUTLIST.md header: "wall 199-3/8, tall cabinet 18-3/8 W x 82-11/16 H x 24-7/16 D,
#                     TV run 181 W x 15 H x 16 D, 4-15/16 kick under both"
WALL_W = 199 + 3 / 8.0
TALL_W = 18 + 3 / 8.0
TALL_H = 82 + 11 / 16.0
TALL_D = 24 + 7 / 16.0          # includes the 5/8 door
TV_W = 181.0
TV_H = 15.0
TV_D = 16.0                     # includes the 5/8 door

# CUTLIST.md "Carcass depths": tall = 24-7/16 - 1/8 back - 5/8 door = 23-11/16;
#                              TV   = 16 - 5/8 door = 15-3/8
TALL_CARCASS_D = 23 + 11 / 16.0
TV_CARCASS_D = 15 + 3 / 8.0

# guide 3, "TV ladder" height table (lines A..F, above the finished floor at the high spot)
LINE_A = 4 + 15 / 16.0          # underside of everything
LINE_B = 6 + 7 / 16.0           # top of the bottom stringers
LINE_C = 6 + 15 / 16.0          # top of the 1/2 bottoms
LINE_D = 15 + 15 / 16.0         # bottom edge of the 2x4 rails
LINE_E = 19 + 7 / 16.0          # top of rails/dividers/stringers, slab underside
LINE_F = 19 + 15 / 16.0         # slab top = panelling bottom edge

# guide 6 "Reference" step 1: find studs between 4" and 20" off the floor
STUD_BAND_LO, STUD_BAND_HI = 4.0, 20.0
STUD_OC = 16.0                  # typical framing pitch, used only to draw the tape marks
STUD_TAPE_TOP = LINE_F + 4.0    # tape goes above the panelling line so the marks survive

# guide 6 "Reference" step 1: right wall stud check for the bay 6 block, 15" out
BAY6_BLOCK_OUT = 15.0

# Members. CUTLIST.md: 2x2 SPF = 1-1/2 actual, 2x4 rail = 1-1/2 x 3-1/2 actual
T2X2 = 1.5
RAIL_T = 1.5
RAIL_H = 3.5
PLY12 = 0.5                     # 1/2" spruce bottoms and dividers
MDF58 = 5 / 8.0                 # kicks, doors, tall right side
MDF12 = 0.5                     # top slab
HARDBOARD = 1 / 8.0             # tall back
DRYWALL = 0.5
STUD_D = 1.5                    # a 2x4 stud is 1-1/2 deep

# guide 3, tall cabinet: bottom rail sits ON the 5/8 bottom, top rail tight under the top
TALL_TOP = LINE_A + TALL_H
BOT_RAIL_LO = LINE_A + MDF58    # 5/8 spruce bottom under it
BOT_RAIL_HI = BOT_RAIL_LO + RAIL_H
TOP_RAIL_HI = TALL_TOP - MDF58
TOP_RAIL_LO = TOP_RAIL_HI - RAIL_H
BOT_RAIL_C = (BOT_RAIL_LO + BOT_RAIL_HI) / 2
TOP_RAIL_C = (TOP_RAIL_LO + TOP_RAIL_HI) / 2

# CUTLIST.md "TV divider positions", X from the left wall to the divider LEFT face
DIVIDER_X = [48 + 37 / 64.0, 78 + 11 / 16.0, 108 + 51 / 64.0, 138 + 57 / 64.0, 169.0]
# Cross blocks / sleepers sit under the divider CENTRES (guide 3 steps 3, 5)
DIVIDER_C = [x + PLY12 / 2 for x in DIVIDER_X]

# guide 3 step 5: seven cross blocks -- one against the tall cabinet's right side, one
# centred under each divider, one at the right wall. CUTLIST: cross block 12-3/8.
XBLOCK_L = 12 + 3 / 8.0
XB_END_L = TALL_W + T2X2 / 2          # first block hard against the tall cabinet
XB_END_R = WALL_W - T2X2 / 2          # last block hard against the right wall
XBLOCK_C = [XB_END_L] + DIVIDER_C + [XB_END_R]

# guide 6 "Sleepers": 2x2 on end, 4-3/4 long, shimmed to line A
SLEEPER_L = 4 + 3 / 4.0
# TV: rear sleepers tight to the wall; front sleepers with their FRONT face 12-7/8 out
SLEEP_REAR_D0, SLEEP_REAR_D1 = 0.0, T2X2
SLEEP_FRONT_D1 = 12 + 7 / 8.0
SLEEP_FRONT_D0 = SLEEP_FRONT_D1 - T2X2
# Tall: the bottom panel sits 1/8 off the wall, behind the hardboard back, so its
# 23-11/16 depth runs 1/8 to 23-13/16 from the wall. The front pair of sleepers goes
# FLUSH with that front edge: 23-13/16 = 24-7/16 door plane - 5/8 kick, so the flush
# tall kick's rear face lands on the sleeper.
TALL_PANEL_D0 = HARDBOARD
TALL_PANEL_D1 = TALL_PANEL_D0 + TALL_CARCASS_D      # 23-13/16 from the wall
TALL_SLEEP_F1 = TALL_PANEL_D1
TALL_SLEEP_F0 = TALL_SLEEP_F1 - T2X2

# Bottom stringers (guide 3 steps 4 and 6): rear tight to the wall, front face 15-3/8 out
STR_REAR_D0, STR_REAR_D1 = 0.0, T2X2
STR_FRONT_D1 = TV_CARCASS_D
STR_FRONT_D0 = STR_FRONT_D1 - T2X2

# Kicks. CUTLIST 5/8 MDF table: kick tall 18-3/8, kick return 10-15/16,
# kick TV 181 cut as 90-11/16 + 90-5/16, joint behind cross block 3.
KICK_H = 4 + 15 / 16.0
KICK_T = MDF58
KICK_TALL_L = 18 + 3 / 8.0
KICK_RETURN_L = 10 + 15 / 16.0
KICK_TV_L = 181.0
KICK_TV_P1 = 90 + 11 / 16.0
KICK_TV_P2 = 90 + 5 / 16.0
KICK_TV_RECESS = 2.5            # recessed 2-1/2 behind the door plane
DOOR_PLANE_TALL = TALL_D        # 24-7/16 from the wall
DOOR_PLANE_TV = TV_D            # 16 from the wall
KICK_TALL_FACE = DOOR_PLANE_TALL                    # flush with the door face
KICK_TV_FACE = DOOR_PLANE_TV - KICK_TV_RECESS       # 13-1/2 from the wall
KICK_TV_JOINT_X = TALL_W + KICK_TV_P1

# Wall screws. guide 6 step 3 / CUTLIST "Wall screws" note.
SCREW_L = 4.0
TALL_STACK = RAIL_T + HARDBOARD + DRYWALL     # 2-1/8
TV_STACK = RAIL_T + DRYWALL                   # 2
TALL_BITE = SCREW_L - TALL_STACK              # 1-7/8 claimed
TV_BITE = SCREW_L - TV_STACK                  # 2 claimed
LEAN_SHIM = 1 / 8.0                           # 1/8 gap at the left wall
DOOR_END_GAP = 1 / 4.0                        # 1/4 at the wall and at the tall cabinet

BAY6_CLEAR = 29 + 7 / 8.0       # CUTLIST "Clear bay widths": bay 6 29-7/8

CAP = 10                        # caption font size
GREY = "#777"


# --------------------------------------------------------------------------------------
# small local helpers
# --------------------------------------------------------------------------------------
def arrow(c, x1, y1, x2, y2, color=DIM, sw=1.0, head=5.0):
    """Straight leader with a filled head at (x2, y2). head is in px."""
    c.line(x1, y1, x2, y2, stroke=color, sw=sw)
    px1, py1, px2, py2 = c.X(x1), c.Y(y1), c.X(x2), c.Y(y2)
    dx, dy = px2 - px1, py2 - py1
    n = (dx * dx + dy * dy) ** 0.5 or 1.0
    ux, uy = dx / n, dy / n
    bx, by = px2 - ux * head, py2 - uy * head
    c.parts.append(
        f"<polygon points='{px2:.1f},{py2:.1f} {bx - uy * head * 0.45:.1f},{by + ux * head * 0.45:.1f} "
        f"{bx + uy * head * 0.45:.1f},{by - ux * head * 0.45:.1f}' fill='{color}'/>"
    )


def caption(c, x, y, s):
    c.text(x, y, s, size=CAP, anchor="start", color=GREY)


def box(c, x, y, w, h, lines, fill="none", size=10, weight="normal", dash=None):
    c.rect(x, y, w, h, fill=fill, dash=dash)
    c.label(x + w / 2, y + h / 2, lines, size=size)


# --------------------------------------------------------------------------------------
# 1. wall elevation
# --------------------------------------------------------------------------------------
def wall_elevation(path):
    S, M = 6.2, 11.0
    HI = 98.0
    c = Canvas(WALL_W, HI, scale=S, margin=M, flip_y=True,
               title="Guide 6 - rear wall front elevation: setting-out lines, stud band, fixings")

    # floor and the two end walls
    c.rect(-9, -3, WALL_W + 18, 3, fill=MAT["floor"], sw=0.8)
    c.rect(-5, 0, 5, 92, fill=MAT["wall"], sw=0.8)
    c.rect(WALL_W, 0, 5, 92, fill=MAT["wall"], sw=0.8)
    c.text(-2.2, 60, "LEFT wall", size=10, rotate=-90)
    c.text(WALL_W + 2.5, 60, "RIGHT wall", size=10, rotate=-90)
    # wall panelling starts at line F
    for x0 in (-5.0, WALL_W):
        c.rect(x0, LINE_F, 5, 9, fill="#e6e6e6", sw=0.8)
    c.text(-2.2, LINE_F + 4.5, "panelling", size=9, rotate=-90, color=GREY)
    c.text(WALL_W + 2.5, LINE_F + 4.5, "panelling", size=9, rotate=-90, color=GREY)

    # stud-finding band, drawn first so everything sits on top of it
    c.rect(0, STUD_BAND_LO, WALL_W, STUD_BAND_HI - STUD_BAND_LO,
           fill="#f5eec9", stroke="none", sw=0, opacity=0.85)

    # setting-out lines. The three letters get their own column at x = -8 with kinked
    # leaders, because E and F are only 1/2 apart and would collide on the lines.
    c.line(-5, LINE_A, WALL_W + 5, LINE_A, stroke=DIM, sw=0.8, dash="7 4")
    c.text(-8.0, LINE_A, "A", size=12, color=DIM, weight="bold")
    c.line(-5, LINE_E, WALL_W + 5, LINE_E, stroke=DIM, sw=0.8, dash="7 4")
    c.line(-7.1, 13.0, -5.6, LINE_E, stroke=DIM, sw=0.7)
    c.text(-8.0, 13.0, "E", size=12, color=DIM, weight="bold")
    c.line(-5, LINE_F, WALL_W + 5, LINE_F, stroke=DIM, sw=0.8, dash="7 4")
    c.line(-7.1, 27.0, -5.6, LINE_F, stroke=DIM, sw=0.7)
    c.text(-8.0, 27.0, "F", size=12, color=DIM, weight="bold")

    # ---- tall cabinet ----
    c.rect(0, LINE_A, TALL_W, TALL_H, fill=MAT["spruce58"])
    c.rect(0, BOT_RAIL_LO, TALL_W, RAIL_H, fill=MAT["2x4"])
    c.rect(0, TOP_RAIL_LO, TALL_W, RAIL_H, fill=MAT["2x4"])
    c.label(TALL_W / 2, 50, ["tall", "cabinet"], size=11)
    c.text(TALL_W / 2, BOT_RAIL_C, "bottom rail", size=8)
    c.text(TALL_W / 2, TOP_RAIL_C, "top rail", size=8)
    for y in (BOT_RAIL_C, TOP_RAIL_C):
        for k in (0.14, 0.86):      # clear of the "bottom rail" / "top rail" captions
            c.circle(TALL_W * k, y, 2.4, fill=DIM)

    # ---- TV run ----
    c.rect(TALL_W, LINE_A, TV_W, T2X2, fill=MAT["2x2"])                 # bottom stringers
    c.rect(TALL_W, LINE_B, TV_W, PLY12, fill=MAT["spruce12"])           # the three bottoms
    c.rect(TALL_W, LINE_D, TV_W, RAIL_H, fill=MAT["2x4"])               # three TV rails
    c.rect(TALL_W, LINE_E, TV_W, MDF12, fill=MAT["mdf12"])              # top slab
    for i, x in enumerate(DIVIDER_X, start=1):
        c.rect(x, LINE_C, PLY12, LINE_E - LINE_C, fill=MAT["spruce12"], sw=0.9)
        c.text(x + PLY12 / 2, LINE_C + 1.2, str(i), size=9)
    bay2 = (DIVIDER_X[0] + PLY12 + DIVIDER_X[1]) / 2
    bay3 = (DIVIDER_X[1] + PLY12 + DIVIDER_X[2]) / 2
    c.text(bay2, LINE_D + RAIL_H / 2, "three TV rails end to end", size=9)
    c.text(bay3, LINE_A + T2X2 / 2, "bottom stringers", size=8)
    c.text(TALL_W + 4, LINE_C + 1.2, "divider", size=9, anchor="start")

    # tape marks above the panelling line at typical stud centres
    n = int((WALL_W - STUD_OC) // STUD_OC)
    for k in range(1, n + 1):
        x = k * STUD_OC
        c.line(x, LINE_F + 0.6, x, STUD_TAPE_TOP, stroke=DIM, sw=1.4)
    c.text(STUD_OC * 2, STUD_TAPE_TOP + 2.4,
           "tape marks on stud centres, above the panelling line", size=10, color=DIM, anchor="start")

    # floor high spot
    arrow(c, 150, -6.6, 150, -0.3, color=LINE)
    c.label(153, -5.6, ["floor high spot: sleepers full height",
                        "here, shims everywhere else"], size=10, anchor="start")

    # right wall stud check for the bay 6 block
    arrow(c, WALL_W - 26, LINE_E + 7, WALL_W - 1.5, LINE_E + 1.5, color=LINE)
    c.label(WALL_W - 27, LINE_E + 9,
            ["right wall: find a stud " + frac(BAY6_BLOCK_OUT) + " out from the",
             "rear wall for the bay 6 top-front block;",
             "bay 6 must finish " + frac(BAY6_CLEAR) + " clear"], size=10, anchor="end")

    # ---- annotation block in the empty middle ----
    ax, ay = 26.0, 78.0
    rows = [
        ("line F  " + frac(LINE_F) + "   slab top = panelling bottom edge", DIM),
        ("line E  " + frac(LINE_E) + "   slab underside = top of the ladder", DIM),
        ("line A  " + frac(LINE_A) + "    underside of both units", DIM),
        ("", LINE),
        ("stud-finding band " + frac(STUD_BAND_LO) + " to " + frac(STUD_BAND_HI)
         + " off the floor", LINE),
        ("tall cabinet rail centres " + frac(BOT_RAIL_C) + " and " + frac(TOP_RAIL_C)
         + " above the floor", LINE),
        ("bottom rail " + frac(BOT_RAIL_LO) + " to " + frac(BOT_RAIL_HI)
         + ", top rail " + frac(TOP_RAIL_LO) + " to " + frac(TOP_RAIL_HI), LINE),
        ("two #10 x " + frac(SCREW_L) + " into two studs per rail (red dots)", LINE),
    ]
    for i, (s_, col) in enumerate(rows):
        if s_:
            c.text(ax, ay - i * 3.3, s_, size=11, anchor="start", color=col)

    # ---- dimensions ----
    # One dim per column so no two rotated labels share a strip of canvas, and every
    # rotated label is short enough not to straddle the line it belongs to.
    # The A/E/F heights and the two rail centre heights are in the annotation block.
    # Witnesses: the cabinet height and the TV-run height run off the carcass itself; the
    # three widths run off the tops of the two end walls (WALL_TOP) and the cabinet top.
    WALL_TOP = 92.0
    c.dim_v(LINE_A, TALL_TOP, -4.0, text=frac(TALL_H) + " tall cabinet", witness=0.0)
    c.dim_v(LINE_A, LINE_F, WALL_W + 3.0, text=frac(TV_H) + " TV run", witness=WALL_W)
    # 3-1/2 is wider than the 3-1/2 span, so push it to the RIGHT of its line, clear of
    # the rail band and of the "top rail" caption inside it.
    c.dim_v(TOP_RAIL_LO, TOP_RAIL_HI, TALL_W + 3.0, offset_px=12, fit="beside",
            witness=TALL_W)
    c.dim_h(0, TALL_W, 90.5, witness=TALL_TOP)
    c.dim_h(TALL_W, WALL_W, 90.5, witness=(TALL_TOP, WALL_TOP))
    c.dim_h(0, WALL_W, 94.5, witness=WALL_TOP)

    caption(c, -5, -9.0,
            "06-wall-elevation: rear wall, front elevation. All heights above the finished "
            "floor at the high spot.")
    return c.save(path)

# --------------------------------------------------------------------------------------
# 2. sleeper plan
# --------------------------------------------------------------------------------------
def sleeper_plan(path):
    # The margin has to hold two depth dimensions on the left and three on the right,
    # all outside the end walls, so it is much wider than the drawing needs.
    S, M = 6.2, 17.0
    c = Canvas(WALL_W, 62, scale=S, margin=M, flip_y=False,
               title="Guide 6 - plan of all 18 sleepers")

    # rear wall at the top, end walls
    c.rect(-9, -2.5, WALL_W + 18, 2.5, fill=MAT["wall"], sw=0.8)
    c.rect(-5, 0, 5, 26, fill=MAT["wall"], sw=0.8)
    c.rect(WALL_W, 0, 5, 26, fill=MAT["wall"], sw=0.8)
    c.text(WALL_W / 2, -1.25, "REAR WALL", size=10)

    # tall cabinet bottom panel
    c.rect(0, TALL_PANEL_D0, TALL_W, TALL_CARCASS_D, fill=MAT["spruce58"], sw=1.0,
           opacity=0.55)
    c.label(TALL_W / 2, 16.5, ["tall bottom", frac(TALL_W) + " x " + frac(TALL_CARCASS_D)], size=9)
    # its four sleepers
    for x0 in (0.0, TALL_W - T2X2):
        c.rect(x0, 0, T2X2, T2X2, fill=MAT["2x2"])
        c.rect(x0, TALL_SLEEP_F0, T2X2, T2X2, fill=MAT["2x2"])

    # TV run footprint and stringers
    c.rect(TALL_W, 0, TV_W, TV_CARCASS_D, fill="none", stroke=GREY, sw=0.8, dash="4 3")
    c.rect(TALL_W, STR_REAR_D0, TV_W, T2X2, fill=MAT["2x2"], sw=0.8, opacity=0.45)
    c.rect(TALL_W, STR_FRONT_D0, TV_W, T2X2, fill=MAT["2x2"], sw=0.8, opacity=0.45)
    c.text(TALL_W + 4, STR_REAR_D1 + 1.0, "bottom rear stringer", size=8, anchor="start")
    c.text(TALL_W + 4, STR_FRONT_D0 - 1.0, "bottom front stringer", size=8, anchor="start")

    # cross blocks and the fourteen TV sleepers
    for i, xc in enumerate(XBLOCK_C, start=1):
        c.rect(xc - T2X2 / 2, STR_REAR_D1, T2X2, XBLOCK_L, fill=MAT["2x2"], sw=0.8, opacity=0.5)
        c.rect(xc - T2X2 / 2, SLEEP_REAR_D0, T2X2, T2X2, fill=MAT["2x2"])
        c.rect(xc - T2X2 / 2, SLEEP_FRONT_D0, T2X2, T2X2, fill=MAT["2x2"])
        c.text(xc, 7.0, str(i), size=9, color=GREY)

    c.text(XBLOCK_C[0] + 3, 7.0, "cross block", size=8, anchor="start", color=GREY)
    c.text(XBLOCK_C[3], 3.0, "rear sleeper", size=8)
    c.text(XBLOCK_C[4], 10.4, "front sleeper", size=8)
    c.text(XBLOCK_C[5] + 2, 0.75, frac(T2X2) + " sq", size=9, color=DIM, anchor="start")

    # ---- dimensions: X from the left wall ----
    # Rows are 4-1/2 apart (28 px at this scale) so no text can land on the line above.
    y1, y2, y3, y4 = 28.0, 32.5, 37.0, 41.5
    # Witness lines from the features down to the rows that use them.
    for x_ in (0.0, TALL_W):
        c.line(x_, TALL_PANEL_D1 + 0.4, x_, y4, stroke=DIM, sw=0.5, dash="2 3")
    c.line(WALL_W, TV_CARCASS_D + 0.4, WALL_W, y4, stroke=DIM, sw=0.5, dash="2 3")
    for xc in XBLOCK_C:
        c.line(xc, TV_CARCASS_D + 0.4, xc, y2, stroke=DIM, sw=0.5, dash="2 3")
    c.dim_h(0, TALL_W, y1)
    c.dim_h(0, XBLOCK_C[0], y2)
    for a, b in zip(XBLOCK_C, XBLOCK_C[1:]):
        c.dim_h(a, b, y2)
    c.dim_h(TALL_W, WALL_W, y3)
    c.dim_h(0, WALL_W, y4)

    # ---- depth dimensions, outside the end walls -------------------------------------
    # Bare numbers only: a rotated label long enough to name the feature would be several
    # times its own span and would run into its neighbours. The key below names them.
    c.dim_v(TALL_PANEL_D0, TALL_PANEL_D1, -7.0, witness=0.0)
    c.dim_v(0, TALL_SLEEP_F1, -11.0, witness=0.0)
    c.dim_v(0, TV_CARCASS_D, WALL_W + 7.5, witness=WALL_W)
    c.dim_v(0, SLEEP_FRONT_D1, WALL_W + 11.5, witness=WALL_W)
    c.dim_v(STR_REAR_D1, STR_REAR_D1 + XBLOCK_L, WALL_W + 15.5, witness=WALL_W)

    # notes, including the key to the five depth dimensions
    notes = [
        ("18 sleepers: 2x2 on end, " + frac(SLEEPER_L) + " long, shimmed to line A.", LINE),
        ("Tall: 4, one per corner; front pair flush with the panel's front edge, "
         + frac(TALL_SLEEP_F1) + " from the wall.", LINE),
        ("TV: 14, rear + front at each of the seven cross block positions.", LINE),
        ("Depths from the rear wall, LEFT of the drawing:  " + frac(TALL_CARCASS_D)
         + " tall bottom panel (its rear edge " + frac(TALL_PANEL_D0) + " off the wall,"
         " behind the back),  " + frac(TALL_SLEEP_F1) + " tall front sleeper face.", DIM),
        ("Depths from the rear wall, RIGHT of the drawing:  " + frac(TV_CARCASS_D)
         + " bottom front stringer face,  " + frac(SLEEP_FRONT_D1) + " TV front sleeper face,",
         DIM),
        ("and " + frac(XBLOCK_L) + " cross block, measured from the back of the bottom rear "
         "stringer at " + frac(STR_REAR_D1) + ".", DIM),
        ("Divider centres from the tall cabinet side: "
         + ", ".join(frac(x - TALL_W) for x in DIVIDER_C) + ".", DIM),
    ]
    for i, (s_, col) in enumerate(notes):
        c.text(TALL_W + 4, 45.5 + i * 2.2, s_, size=10, anchor="start", color=col)

    caption(c, -5, 61.4,
            "06-sleeper-plan: plan, wall at the top, doors at the bottom. X measured from "
            "the LEFT wall.")
    return c.save(path)

# --------------------------------------------------------------------------------------
# 3. fixing sections
# --------------------------------------------------------------------------------------
def tall_fixing_section(path):
    S, M = 30.0, 0.7
    PANEL = 9.6                      # model-inch pitch between the three details
    TOP, SH = 5.0, 3.5               # section band: 3-1/2 of rail seen across the wall
    c = Canvas(3 * PANEL, 14.4, scale=S, margin=M, flip_y=False,
               title="Guide 6 - section at a hanging rail: screw stacks and the leaning-wall shim")

    def notes(panel_left, lines):
        for i, s_ in enumerate(lines):
            c.text(panel_left + PANEL / 2, 11.0 + i * 0.48, s_, size=9)

    def stack(panel_left, title, layers, bite, extra):
        """One horizontal section. Depth runs to the RIGHT, away from the wall."""
        stack_t = sum(w for w, _, _ in layers)
        x0 = panel_left + 6.4 - stack_t - STUD_D      # so the screw head lands mid-panel
        c.rect(x0, TOP, STUD_D, SH, fill=MAT["2x4"])
        c.text(x0 + STUD_D / 2, TOP + SH * 0.27, "stud", size=9, rotate=-90)
        x = x0 + STUD_D
        for w, fill, name in layers:
            c.rect(x, TOP - 0.9, w, SH + 1.8, fill=fill)
            if w >= 0.45:
                c.text(x + w / 2, TOP + SH * 0.27, name, size=9, rotate=-90)
            x += w
        face = x
        yc, tip = TOP + SH / 2, face - SCREW_L
        c.line(tip, yc, face, yc, stroke=LINE, sw=3.0)
        c.circle(face, yc, 3.2)
        # Witnesses: the layer ends run off the top edge of the layer rectangles, the screw
        # tip off the top of its own dashed tip line (drawn below).
        band, tipy = TOP - 0.9, TOP - 0.4
        c.dim_h(tip, face, 1.9, text="#10 x " + frac(SCREW_L), witness=(tipy, band))
        c.dim_h(tip, x0 + STUD_D, 2.9, text=frac(bite) + " past the drywall",
                witness=(tipy, band))
        c.dim_h(x0 + STUD_D, face, 3.9, text=frac(stack_t) + " stack", witness=band)
        if bite > STUD_D:
            c.line(tip, TOP - 0.4, tip, TOP + SH + 0.4, stroke=DIM, sw=0.8, dash="3 2")
            c.text(tip + 0.15, TOP + SH + 1.5,
                   "tip " + frac(bite - STUD_D) + " into the cavity", size=8,
                   color=DIM, anchor="start")
        c.text(panel_left + PANEL / 2, 0.6, title, size=11, weight="bold")
        notes(panel_left, extra)
        return face

    stack(0.0, "tall cabinet rail",
          [(DRYWALL, MAT["wall"], "drywall"), (HARDBOARD, MAT["hardboard"], "hardboard"),
           (RAIL_T, MAT["2x4"], "rail")],
          TALL_BITE,
          ["rail " + frac(RAIL_T) + " + hardboard " + frac(HARDBOARD) + " + drywall "
           + frac(DRYWALL) + " = " + frac(TALL_STACK),
           "guide 6 step 3 calls the remaining " + frac(TALL_BITE) + " stud bite,",
           "but a 2x4 stud is only " + frac(STUD_D) + " deep, so the tip",
           "comes out the back by " + frac(TALL_BITE - STUD_D) + "."])

    stack(PANEL, "TV hanging rail",
          [(DRYWALL, MAT["wall"], "drywall"), (RAIL_T, MAT["2x4"], "rail")],
          TV_BITE,
          ["no back behind the TV rails: rail " + frac(RAIL_T) + " +",
           "drywall " + frac(DRYWALL) + " = " + frac(TV_STACK) + ". CUTLIST calls the rest",
           frac(TV_BITE) + " of stud bite; on the same " + frac(STUD_D) + " stud",
           frac(TV_BITE - STUD_D) + " comes out the back."])

    # third detail: shim between the cabinet side and a leaning left wall
    panel_left = 2 * PANEL
    x0 = panel_left + 4.0
    c.rect(x0, TOP - 0.9, DRYWALL, SH + 1.8, fill=MAT["wall"])
    c.text(x0 + DRYWALL / 2, TOP + SH * 0.27, "left wall", size=9, rotate=-90)
    gx = x0 + DRYWALL
    c.rect(gx, TOP - 0.9, LEAN_SHIM, SH + 1.8, fill=MAT["spruce12"])
    c.rect(gx + LEAN_SHIM, TOP - 0.9, MDF58, SH + 1.8, fill=MAT["spruce58"])
    c.text(gx + LEAN_SHIM + MDF58 / 2, TOP + SH * 0.27, "tall left side", size=9, rotate=-90)
    c.dim_h(gx, gx + LEAN_SHIM, 3.9, text=frac(LEAN_SHIM) + " shim", witness=TOP - 0.9)
    c.dim_h(gx + LEAN_SHIM, gx + LEAN_SHIM + MDF58, 2.9, text=frac(MDF58) + " side",
            witness=TOP - 0.9)
    c.text(panel_left + PANEL / 2, 0.6, "leaning left wall", size=11, weight="bold")
    notes(panel_left,
          ["shim at BOTH rail heights (" + frac(BOT_RAIL_C) + " and " + frac(TOP_RAIL_C) + ")",
           "so the cabinet stays plumb; a " + frac(LEAN_SHIM) + " gap at the wall",
           "vanishes inside the door's " + frac(DOOR_END_GAP) + " end gap.",
           "Same trick behind a rail if the REAR wall leans."])

    caption(c, 0.0, 14.2, "06-tall-fixing-section: horizontal sections through a rail, drawn large.")
    return c.save(path)

# --------------------------------------------------------------------------------------
# 4. kick plan
# --------------------------------------------------------------------------------------
def kick_plan(path):
    # Wide margin: two depth dimensions live left of the left wall, two right of the right
    # wall, all outside the wall rectangles.
    S, M = 6.2, 15.0
    c = Canvas(WALL_W, 60, scale=S, margin=M, flip_y=False,
               title="Guide 6 - kick plan: three planes, one return")

    c.rect(-9, -2.5, WALL_W + 18, 2.5, fill=MAT["wall"], sw=0.8)
    c.rect(-5, 0, 5, 27, fill=MAT["wall"], sw=0.8)
    c.rect(WALL_W, 0, 5, 27, fill=MAT["wall"], sw=0.8)
    c.text(WALL_W / 2, -1.25, "REAR WALL", size=10)

    # carcass outlines for context
    c.rect(0, TALL_PANEL_D0, TALL_W, TALL_CARCASS_D, fill="none", stroke=GREY, sw=0.7,
           dash="3 3")
    c.rect(TALL_W, 0, TV_W, TV_CARCASS_D, fill="none", stroke=GREY, sw=0.7, dash="3 3")

    # door planes, dashed
    c.line(0, DOOR_PLANE_TALL, TALL_W, DOOR_PLANE_TALL, stroke=LINE, sw=1.0, dash="8 4")
    c.line(TALL_W, DOOR_PLANE_TV, WALL_W, DOOR_PLANE_TV, stroke=LINE, sw=1.0, dash="8 4")
    c.line(TALL_W, DOOR_PLANE_TV, TALL_W, DOOR_PLANE_TALL, stroke=LINE, sw=1.0, dash="8 4")

    # sleepers the kicks screw to
    for x0 in (0.0, TALL_W - T2X2):
        c.rect(x0, TALL_SLEEP_F0, T2X2, T2X2, fill=MAT["2x2"], sw=0.8)
    for xc in XBLOCK_C:
        c.rect(xc - T2X2 / 2, SLEEP_FRONT_D0, T2X2, T2X2, fill=MAT["2x2"], sw=0.8)

    # tall kick, flush with the door face
    c.rect(0, KICK_TALL_FACE - KICK_T, KICK_TALL_L, KICK_T, fill=MAT["mdf58"])
    c.label(1.0, 5.4, ["kick, tall " + frac(KICK_TALL_L),
                       "flush with the",
                       "door face"], size=9, anchor="start")
    c.label(TALL_W / 2, 12.0, ["door plane", frac(DOOR_PLANE_TALL)], size=9, color=GREY)
    arrow(c, TALL_W / 2, 14.2, TALL_W / 2, KICK_TALL_FACE - 0.3, color=GREY)

    # TV kick in two pieces
    c.rect(TALL_W, KICK_TV_FACE - KICK_T, KICK_TV_P1, KICK_T, fill=MAT["mdf58"])
    c.rect(KICK_TV_JOINT_X, KICK_TV_FACE - KICK_T, KICK_TV_P2, KICK_T, fill=MAT["mdf58"])
    c.line(KICK_TV_JOINT_X, KICK_TV_FACE - KICK_T - 1.2, KICK_TV_JOINT_X, KICK_TV_FACE + 1.2,
           stroke=DIM, sw=1.4)
    c.text(TALL_W + KICK_TV_P1 / 2, 10.2, "kick, TV " + frac(KICK_TV_P1), size=10)
    c.text(KICK_TV_JOINT_X + KICK_TV_P2 / 2, 10.2, "kick, TV " + frac(KICK_TV_P2), size=10)
    c.text(TALL_W + 100, DOOR_PLANE_TV + 1.4, "TV door plane " + frac(DOOR_PLANE_TV),
           size=9, color=GREY)

    arrow(c, KICK_TV_JOINT_X + 16, 7.0, KICK_TV_JOINT_X + 0.4, KICK_TV_FACE - KICK_T - 1.5)
    c.text(KICK_TV_JOINT_X + 17, 7.0,
           "joint behind cross block 3's sleeper (" + frac(DIVIDER_C[2]) + " from the left wall)",
           size=10, anchor="start", color=DIM)

    # the return and its 2x2 block. The note sits in the empty band in front of the TV
    # kick with a short horizontal leader, instead of a long diagonal across the run.
    c.rect(TALL_W, KICK_TV_FACE, KICK_T, KICK_RETURN_L, fill=MAT["mdf58"])
    c.rect(TALL_W + KICK_T, KICK_TV_FACE + 3.0, T2X2, T2X2, fill=MAT["2x2"], sw=0.8)
    ret_y = KICK_TV_FACE + KICK_RETURN_L / 2
    arrow(c, TALL_W + 9.5, ret_y, TALL_W + KICK_T + 0.4, ret_y)
    c.label(TALL_W + 10.5, ret_y,
            ["kick return " + frac(KICK_RETURN_L) + " joins the two planes at the tall",
             "cabinet's right side, on a 2x2 block behind it",
             "(" + frac(DOOR_PLANE_TALL) + " - " + frac(KICK_TV_FACE) + " = "
             + frac(KICK_RETURN_L) + ")"], size=10, anchor="start")

    # ---- dimensions ------------------------------------------------------------------
    # Rows 5 apart (31 px) so no text lands on the line above; each row witnessed back to
    # the kick face it measures.
    c.dim_h(0, KICK_TALL_L, 29.0, witness=KICK_TALL_FACE)
    c.dim_h(TALL_W, KICK_TV_JOINT_X, 29.0, witness=KICK_TV_FACE)
    c.dim_h(KICK_TV_JOINT_X, WALL_W, 29.0, witness=KICK_TV_FACE)
    c.dim_h(TALL_W, WALL_W, 34.0, text=frac(KICK_TV_L), witness=KICK_TV_FACE)
    c.dim_h(0, WALL_W, 39.0, witness=(KICK_TALL_FACE, KICK_TV_FACE))
    # Depths: bare numbers, named in the key below, so no rotated label overruns its span.
    c.dim_v(0, KICK_TALL_FACE, -7.0, witness=0.0)
    c.dim_v(0, TALL_SLEEP_F1, -11.0, witness=0.0)
    c.dim_v(0, KICK_TV_FACE, WALL_W + 7.5, witness=WALL_W)
    c.dim_v(0, DOOR_PLANE_TV, WALL_W + 11.5, witness=WALL_W)
    # The recess is only 2-1/2 deep, so it is dimensioned in open drawing space with the
    # label written horizontally to the right of its own line.
    c.dim_v(KICK_TV_FACE, DOOR_PLANE_TV, TALL_W + 128.0,
            text=frac(KICK_TV_RECESS) + " recess", offset_px=6, fit="beside")

    notes = [
        ("All kicks " + frac(KICK_T) + " MDF, " + frac(KICK_H)
         + " tall, #8 x 1-1/4 into the sleepers,", LINE),
        ("two per sleeper, heads filled. Kicks come off for cleaning.", LINE),
        ("Depths from the rear wall, LEFT of the drawing:  " + frac(KICK_TALL_FACE)
         + " tall kick face (= the tall door plane); the tall front sleepers are flush",
         DIM),
        ("with the bottom panel's front edge at " + frac(TALL_SLEEP_F1)
         + ", so the flush kick's rear face lands on them.", DIM),
        ("Depths from the rear wall, RIGHT of the drawing:  " + frac(KICK_TV_FACE)
         + " TV kick face,  " + frac(DOOR_PLANE_TV) + " TV door plane.", DIM),
    ]
    for i, (s_, col) in enumerate(notes):
        c.text(TALL_W + 4, 43.5 + i * 2.0, s_, size=10, anchor="start", color=col)

    caption(c, -5, 59.4,
            "06-kick-plan: plan, wall at the top. Door planes dashed; the TV kick sits "
            + frac(KICK_TV_RECESS) + " behind its door plane.")
    return c.save(path)

# --------------------------------------------------------------------------------------
# 5. order strip
# --------------------------------------------------------------------------------------
def order_strip(path):
    S, M = 6.5, 3.0
    W, H = 190.0, 66.0
    c = Canvas(W, H, scale=S, margin=M, flip_y=False,
               title="Guide 6 - order of work")

    bw, gap, by, bh = 34.0, 5.0, 4.0, 15.0
    stages = [
        ["1. TALL CABINET", "sleepers, plumb,", "screw to studs"],
        ["2. TV LADDER", "guide 3 'TV ladder'", "steps 1 to 10"],
        ["3. KICKS", "tall, TV in 2 pieces,", "return"],
        ["4. DOORS", "guide 4 'Hang'", "tall, then TV 1 to 6"],
        ["5. TOP SLAB", "guide 7", "two pieces, jointed"],
    ]
    xs = [i * (bw + gap) for i in range(5)]
    for x, lines in zip(xs, stages):
        box(c, x, by, bw, bh, lines, fill="#f4f4f4", size=11)
    for x in xs[:-1]:
        arrow(c, x + bw + 0.6, by + bh / 2, x + bw + gap - 0.6, by + bh / 2, color=LINE, sw=1.4)

    # bracket from stage 2 down to its ten sub-steps
    x2 = xs[1] + bw / 2
    c.line(x2, by + bh, x2, by + bh + 4.0, stroke=LINE, sw=1.0)
    c.line(4.0, by + bh + 4.0, W - 4.0, by + bh + 4.0, stroke=LINE, sw=1.0)

    subs = [
        "1 level line E on the wall",
        "2 three 2x4 rails to the studs",
        "3 seven rear sleepers to line A",
        "4 bottom rear stringer, 3 pieces",
        "5 seven cross blocks",
        "6 front sleepers + front stringer",
        "7 three bottoms, rear edge scribed",
        "8 five dividers, notched over the rail",
        "9 six top-front stringers",
        "10 check plumb, line E, front plane",
    ]
    cw, cgap, cy, ch = 36.0, 2.0, by + bh + 7.0, 8.0
    for i, s in enumerate(subs):
        col, row = i % 5, i // 5
        x = col * (cw + cgap)
        y = cy + row * (ch + 2.0)
        # 9.5 keeps the longest sub-step ("8 five dividers...") inside its box
        box(c, x, y, cw, ch, s, fill="white", size=9.5, dash="3 2")
        if row == 0:
            c.line(x + cw / 2, by + bh + 4.0, x + cw / 2, y, stroke=LINE, sw=0.6, dash="2 2")

    c.text(0, cy + 2 * (ch + 2.0) + 4.5,
           "Rails first: everything hangs off them, and nothing else squares the run.",
           size=11, anchor="start")
    c.text(0, cy + 2 * (ch + 2.0) + 8.5,
           "Between 2 and 3: check bay 6 is " + frac(BAY6_CLEAR)
           + " clear. If it is short, move divider 5 left and recut door 6",
           size=11, anchor="start", color=DIM)
    c.text(0, cy + 2 * (ch + 2.0) + 12.0,
           "and the bay 6 top front stringer; the " + frac(DOOR_END_GAP)
           + " end gap absorbs up to " + frac(1 / 8.0) + " either way.",
           size=11, anchor="start", color=DIM)

    caption(c, 0, H - 1.0, "06-order: sequence only, not to scale.")
    return c.save(path)


# --------------------------------------------------------------------------------------
def build(outdir):
    jobs = [
        ("06-wall-elevation.svg", wall_elevation,
         "Rear wall elevation: lines A, E and F, the stud-finding band, the tall cabinet's "
         "two rail heights and the right-wall stud check"),
        ("06-sleeper-plan.svg", sleeper_plan,
         "Plan of all 18 sleepers: four under the tall cabinet, fourteen under the seven "
         "TV cross block positions, dimensioned from the left wall"),
        ("06-tall-fixing-section.svg", tall_fixing_section,
         "Sections at a hanging rail: the tall cabinet screw stack, the TV rail stack, and "
         "shimming a leaning left wall"),
        ("06-kick-plan.svg", kick_plan,
         "Kick plan: tall kick flush with the door face, TV kick in two pieces recessed "
         "2-1/2, and the 10-15/16 return between the planes"),
        ("06-order.svg", order_strip,
         "Order of work: tall cabinet, TV ladder (guide 3 steps 1 to 10), kicks, doors, slab"),
    ]
    out = []
    for name, fn, cap in jobs:
        fn(f"{outdir.rstrip('/')}/{name}")
        out.append((name, cap))
    return out


if __name__ == "__main__":
    print(build("."))
