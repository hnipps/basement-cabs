"""Diagrams for guide 02 (cutting): sheet nests, stick crosscut plan, saw guide.

Every number below is taken from ../../CUTLIST.md (source of truth) or from
guides/02-cutting.md where the guide adds shop detail the cut list does not carry
(rip order, oversize allowances, the saw guide). Labels are rendered with frac()
from the same constants that place the geometry, so text and drawing agree.
"""
import os

from svgkit import Canvas, MAT, frac, LINE, DIM

# ---------------------------------------------------------------------------
# constants
# ---------------------------------------------------------------------------
KERF = 0.125                     # guide 02 "Kerf is 1/8"
OVERSIZE = 0.5                   # guide 02: doors/slab roughed 1/2 oversize

# sheet sizes
SPRUCE_SHEET = (96.0, 48.0)      # CUTLIST 5/8 + 1/2 spruce: "a true 48 x 96"
MDF_SHEET = (97.0, 49.0)         # CUTLIST 5/8 MDF: "Nest A (fits 2 x 49x97)"
HARDBOARD_SHEET = (96.0, 48.0)   # CUTLIST 1/8 hardboard, buy 1

# --- 5/8" spruce plywood (tall carcass) ------------------------------------
TALL_H = 82 + 11 / 16.0          # CUTLIST: tall left side length 82-11/16
TALL_DEPTH = 23 + 11 / 16.0      # CUTLIST: tall left side width 23-11/16
TOP_LEN = 23 + 11 / 16.0         # CUTLIST: tall top, bottom  23-11/16 long
TOP_W = 17 + 1 / 8.0             # CUTLIST: tall top, bottom  17-1/8 wide
SHELF_LEN = 23 + 1 / 16.0        # CUTLIST: tall shelves 23-1/16 long
SHELF_W = 17 + 1 / 16.0          # CUTLIST: tall shelves 17-1/16 wide
BLANK_W = 17 + 1 / 4.0           # guide 02 step 2: five blanks at 17-1/4
STRIP58 = SPRUCE_SHEET[1] - TALL_DEPTH - KERF   # 24-3/16 remaining rip

# --- 1/2" spruce plywood (TV bottoms and dividers) -------------------------
BOTTOM_W = 15 + 3 / 8.0          # CUTLIST: TV bottoms 15-3/8 wide
BOTTOMS = [                      # CUTLIST: TV bottom 1/2/3 lengths
    (60 + 9 / 16.0, "TV bottom 1"),
    (60 + 13 / 64.0, "TV bottom 2"),
    (60 + 15 / 64.0, "TV bottom 3"),
]
DIV_LEN = 15 + 3 / 8.0           # CUTLIST: TV dividers 15-3/8 x 12-1/2
DIV_H = 12 + 1 / 2.0
NOTCH_UP = 3 + 1 / 2.0           # CUTLIST notes: notch 3-1/2 up x 1-1/2 in
NOTCH_IN = 1 + 1 / 2.0

# --- 5/8" MDF (2 sheets, Nest A) -------------------------------------------
TALL_RIGHT_W = 23 + 11 / 16.0    # CUTLIST: tall right side (exposed face)
TALL_DOOR_W = 18 + 1 / 8.0       # CUTLIST: tall door 82-11/16 x 18-1/8
KICK_W = 4 + 15 / 16.0           # CUTLIST: all kicks 4-15/16 wide
TV_KICK_L = 90 + 11 / 16.0       # guide 02 + CUTLIST: TV kick left piece
TV_KICK_R = 90 + 5 / 16.0        # guide 02 + CUTLIST: TV kick right piece
TALL_KICK = 18 + 3 / 8.0         # CUTLIST: kick, tall (flush)
KICK_RETURN = 10 + 15 / 16.0     # CUTLIST: kick return
DOOR_W = 14 + 3 / 8.0            # CUTLIST: TV doors 29-63/64 x 14-3/8
DOOR_LEN = 29 + 63 / 64.0
DOOR_BLANK = DOOR_LEN + OVERSIZE  # guide 02: 30-31/64 blanks
TALL_DOOR_BLANK = TALL_H + OVERSIZE

# --- 1/2" MDF (TV top slab) ------------------------------------------------
FENCE_W = 3.0                    # guide 02 "Build the saw guide" step 1
SLAB_W = 16.0                    # CUTLIST: TV top slab 16 wide
SLAB_L = 90 + 43 / 64.0          # CUTLIST: slab left piece
SLAB_R = 90 + 21 / 64.0          # CUTLIST: slab right piece

# --- 1/8" hardboard --------------------------------------------------------
BACK_L = 82 + 11 / 16.0          # CUTLIST: tall back 82-11/16 x 18-3/8
BACK_W = 18 + 3 / 8.0
GUIDE_BASE_W = 8.0               # guide 02: 8" saw-guide base strip
HARDBOARD_T = 1 / 8.0
MDF12_T = 1 / 2.0

# --- 2x2 crosscut plan (CUTLIST "Crosscut plan, 1/8 kerf, 96 boards") ------
# The third element of each row is the leftover printed in the CUTLIST/guide table;
# the drawing labels the leftover it actually computes (see report: #3/#4 differ by 1/64).
BOARD_2X2 = 96.0
T2 = 1.5                         # 2x2 actual 1-1/2
STRINGER_A = 60 + 9 / 16.0
STRINGER_B = 60 + 13 / 64.0
STRINGER_C = 60 + 15 / 64.0
TOPF_BAY1 = 30 + 13 / 64.0
TOPF_MID = 29 + 39 / 64.0
TOPF_BAY6 = 29 + 7 / 8.0
CROSS_BLOCK = 12 + 3 / 8.0
STICKS_2X2 = [
    ("#1", [(STRINGER_A, "bottom stringer"), (TOPF_BAY1, "top front stringer bay 1")], 4 + 63 / 64.0),
    ("#2", [(STRINGER_A, "bottom stringer"), (TOPF_BAY6, "top front stringer bay 6")], 5 + 5 / 16.0),
    ("#3", [(STRINGER_C, "bottom stringer"), (TOPF_MID, "top front stringer bay 2")], 5 + 59 / 64.0),
    ("#4", [(STRINGER_C, "bottom stringer"), (TOPF_MID, "top front stringer bay 3")], 5 + 59 / 64.0),
    ("#5", [(STRINGER_B, "bottom stringer"), (TOPF_MID, "top front stringer bay 4")], 5 + 15 / 16.0),
    ("#6", [(STRINGER_B, "bottom stringer"), (TOPF_MID, "top front stringer bay 5")], 5 + 15 / 16.0),
    ("#7", [(CROSS_BLOCK, "cross block")] * 7, 8 + 1 / 2.0),
    ("#8", [], BOARD_2X2),       # kick sleepers, cut to suit (guide 6)
]

# --- 2x4 crosscut plan (CUTLIST "Crosscut plan from the boards on hand") ---
# Table leftovers below do not deduct the kerf; the drawing computes and labels its own.
T4 = 3.5                         # 2x4 actual 3-1/2
TV_RAIL = 60 + 21 / 64.0         # CUTLIST: TV hanging rails
TALL_RAIL = 17 + 1 / 8.0         # CUTLIST: tall hanging rails
STICKS_2X4 = [
    ("8' #1", 96.0, [(TV_RAIL, "TV hanging rail")], 35 + 43 / 64.0),
    ("8' #2", 96.0, [(TV_RAIL, "TV hanging rail")], 35 + 43 / 64.0),
    ("6-1/2' #1", 78.0, [(TV_RAIL, "TV hanging rail")], 17 + 43 / 64.0),
    ("47\"", 47.0, [(TALL_RAIL, "tall hanging rail"), (TALL_RAIL, "tall hanging rail")], 12 + 5 / 8.0),
    ("6-1/2' #2", 78.0, [], 78.0),
]


# ---------------------------------------------------------------------------
# small drawing helpers
# ---------------------------------------------------------------------------
def _sheet(c, ox, oy, L, W, name):
    """Sheet outline with its size called out above the top-left corner."""
    c.rect(ox, oy, L, W, fill="white", stroke=LINE, sw=1.8)
    c.text(ox, oy - 1.6, f"{name}  {frac(L)} x {frac(W)}", size=13,
           anchor="start", weight="bold")


def _waste(c, ox, oy, w, h, label=None, size=9):
    if w <= 0.02 or h <= 0.02:
        return
    c.rect(ox, oy, w, h, fill=MAT["waste"], stroke=LINE, sw=0.6)
    if label:
        c.label(ox + w / 2, oy + h / 2, label, size=size)


def _kerf_h(c, ox, oy, L):
    """Kerf line running along the sheet length at across-width position oy."""
    c.line(ox, oy, ox + L, oy, stroke=LINE, sw=0.8, dash="3 3")


def _kerf_v(c, ox, oy, h):
    c.line(ox, oy, ox, oy + h, stroke=LINE, sw=0.8, dash="3 3")


def _dim_h_boxed(c, x1, x2, y, text=None, offset_px=-12, size=10):
    """dim_h with a white box behind the text, for dimensions over a dark fill."""
    t = frac(abs(x2 - x1)) if text is None else text
    w = len(t) * size * 0.62 / c.s
    h = size * 1.5 / c.s
    c.rect((x1 + x2) / 2 - w / 2, y + offset_px / c.s - h / 2, w, h,
           fill="white", stroke="none", sw=0)
    c.dim_h(x1, x2, y, text=t, offset_px=offset_px, size=size)


def _caption(c, ox, oy, text):
    c.text(ox, oy, text, size=11, anchor="start", color="#555")


# ---------------------------------------------------------------------------
# 1. 5/8" spruce nest
# ---------------------------------------------------------------------------
def nest_spruce_58(outdir):
    L, W = SPRUCE_SHEET
    ox, oy = 6.0, 3.0
    c = Canvas(ox + L + 3.0, oy + W + 4.5, scale=12.0, margin=0.5,
               title="Guide 02 - 5/8 spruce nest, one 48 x 96 sheet")
    _sheet(c, ox, oy, L, W, "5/8 spruce plywood")

    # --- rip 1: 23-11/16 full length -> tall left side
    y = oy
    c.rect(ox, y, TALL_H, TALL_DEPTH, fill=MAT["spruce58"])
    c.label(ox + TALL_H / 2, y + TALL_DEPTH / 2 - 1.2,
            ["tall left side", f"{frac(TALL_H)} x {frac(TALL_DEPTH)}"], size=13)
    c.dim_h(ox, ox + TALL_H, y + TALL_DEPTH - 1.6, offset_px=-13)
    _waste(c, ox + TALL_H + KERF, y, L - TALL_H - KERF, TALL_DEPTH,
           ["waste", frac(L - TALL_H - KERF)])
    c.dim_v(y, y + TALL_DEPTH, ox - 1.0)
    _kerf_v(c, ox + TALL_H + KERF / 2, y, TALL_DEPTH)

    # --- rip 2: remaining 24-3/16 strip, cross-cut into five 17-1/4 blanks
    y2 = oy + TALL_DEPTH + KERF
    _kerf_h(c, ox, oy + TALL_DEPTH + KERF / 2, L)
    c.dim_v(y2, y2 + STRIP58, ox - 1.0)

    blanks = [
        ("tall top", TOP_LEN, TOP_W),
        ("tall bottom", TOP_LEN, TOP_W),
        ("tall shelf 1", SHELF_LEN, SHELF_W),
        ("tall shelf 2", SHELF_LEN, SHELF_W),
        ("tall shelf 3", SHELF_LEN, SHELF_W),
    ]
    x = ox
    for i, (name, fin_len, fin_w) in enumerate(blanks):
        c.rect(x, y2, BLANK_W, STRIP58, fill=MAT["spruce58"])
        # final trim lines: STRIP58 -> fin_len across the sheet, BLANK_W -> fin_w
        c.line(x, y2 + fin_len, x + BLANK_W, y2 + fin_len, stroke=DIM, sw=0.8, dash="4 3")
        c.line(x + fin_w, y2, x + fin_w, y2 + fin_len, stroke=DIM, sw=0.8, dash="4 3")
        c.label(x + BLANK_W / 2, y2 + STRIP58 / 2 - 2.0,
                [f"blank {i + 1}", name, "trim to", f"{frac(fin_len)} x {frac(fin_w)}"], size=11)
        if i:
            _kerf_v(c, x - KERF / 2, y2, STRIP58)
        x += BLANK_W + KERF
    used = 5 * BLANK_W + 4 * KERF
    c.dim_h(ox, ox + used, y2 + STRIP58 - 0.9, offset_px=-12)
    _waste(c, ox + used + KERF, y2, L - used - KERF, STRIP58,
           ["waste", frac(L - used - KERF)])
    _kerf_v(c, ox + used + KERF / 2, y2, STRIP58)

    c.text(ox + used / 2, y2 + STRIP58 + 1.4,
           f"five blanks {frac(BLANK_W)} wide  (5 x {frac(BLANK_W)} = {frac(5 * BLANK_W)} along the length)",
           size=11, anchor="middle")
    c.text(ox + L, oy - 1.6,
           f"kerf {frac(KERF)} (dashed);  {frac(TALL_DEPTH)} + kerf + {frac(TALL_DEPTH)} = "
           f"{frac(2 * TALL_DEPTH + KERF)}, so a true 48 sheet only",
           size=11, anchor="end", color=DIM)
    _caption(c, ox, oy + W + 3.2,
             "Sheet plan, 5/8 spruce: one full-length rip for the tall left side, five blanks from the rest.")
    name = "02-nest-spruce-58.svg"
    c.save(os.path.join(outdir, name))
    return name, "5/8 spruce nest: tall left side plus five 17-1/4 blanks for top, bottom and shelves"


# ---------------------------------------------------------------------------
# 2. 1/2" spruce nest + divider notch inset
# ---------------------------------------------------------------------------
def nest_spruce_12(outdir):
    L, W = SPRUCE_SHEET
    ox, oy = 6.0, 3.0
    inset_y = oy + W + 6.0
    c = Canvas(ox + L + 3.0, inset_y + DIV_H + 8.0, scale=11.5, margin=0.5,
               title="Guide 02 - 1/2 spruce nest, TV bottoms and dividers")
    _sheet(c, ox, oy, L, W, "1/2 spruce plywood")

    div_no = 1
    for si, (blen, bname) in enumerate(BOTTOMS):
        y = oy + si * (BOTTOM_W + KERF)
        if si:
            _kerf_h(c, ox, y - KERF / 2, L)
        c.dim_v(y, y + BOTTOM_W, ox - 1.0)
        # bottom
        c.rect(ox, y, blen, BOTTOM_W, fill=MAT["spruce12"])
        c.label(ox + blen / 2, y + BOTTOM_W / 2 - 0.9,
                [bname, f"{frac(blen)} x {frac(BOTTOM_W)}"], size=12)
        c.dim_h(ox, ox + blen, y + BOTTOM_W - 1.1, offset_px=-12)
        x = ox + blen + KERF
        _kerf_v(c, x - KERF / 2, y, BOTTOM_W)
        # two dividers
        for _ in range(2):
            spare = div_no == 6
            c.rect(x, y, DIV_H, BOTTOM_W, fill=MAT["spruce12"])
            lines = [f"divider {div_no}", f"{frac(DIV_LEN)} x {frac(DIV_H)}"]
            if spare:
                lines = ["divider 6", "SPARE", f"{frac(DIV_LEN)} x {frac(DIV_H)}"]
            c.label(x + DIV_H / 2, y + BOTTOM_W / 2 - 0.6, lines, size=10)
            c.dim_h(x, x + DIV_H, y + BOTTOM_W - 1.1, offset_px=-12)
            div_no += 1
            x += DIV_H + KERF
            _kerf_v(c, x - KERF / 2, y, BOTTOM_W)
        _waste(c, x, y, ox + L - x, BOTTOM_W,
               ["waste", frac(ox + L - x)])

    strips = 3 * BOTTOM_W + 2 * KERF
    _kerf_h(c, ox, oy + strips + KERF / 2, L)
    _waste(c, ox, oy + strips + KERF, L, W - strips - KERF,
           f"leftover {frac(W - strips - KERF)} x {frac(L)}")
    c.dim_v(oy, oy + strips, ox - 3.2, text=f"3 strips = {frac(strips)}")

    # --- inset: divider notch, viewed on the right face
    ix = ox + 4.0
    c.text(ix, inset_y - 2.4, "Inset: divider, right face  (notch at the rear top corner)",
           size=12, anchor="start", weight="bold")
    pts = [(ix, inset_y + DIV_H), (ix, inset_y + NOTCH_UP), (ix + NOTCH_IN, inset_y + NOTCH_UP),
           (ix + NOTCH_IN, inset_y), (ix + DIV_LEN, inset_y), (ix + DIV_LEN, inset_y + DIV_H)]
    c.poly(pts, fill=MAT["spruce12"], sw=1.6)
    c.rect(ix, inset_y, NOTCH_IN, NOTCH_UP, fill=MAT["waste"], stroke=DIM, sw=0.8, dash="4 3")
    c.dim_h(ix, ix + NOTCH_IN, inset_y - 0.5, offset_px=-11)
    c.dim_v(inset_y, inset_y + NOTCH_UP, ix + NOTCH_IN + 1.5, offset_px=12, rotate=90)
    c.text(ix + NOTCH_IN + 3.2, inset_y + NOTCH_UP / 2, "notch for the 2x4 rail",
           size=8.5, anchor="start")
    c.dim_h(ix, ix + DIV_LEN, inset_y + DIV_H + 1.6, offset_px=12)
    c.dim_v(inset_y, inset_y + DIV_H, ix - 1.0)
    c.text(ix, inset_y + DIV_H + 3.4, "rear (wall)", size=10, anchor="start")
    c.text(ix + DIV_LEN, inset_y + DIV_H + 3.4, "front", size=10, anchor="end")
    c.text(ix + DIV_LEN / 2 + 1.2, inset_y + DIV_H / 2,
           '"H" on this (RIGHT) face:', size=8.5, anchor="middle")
    c.text(ix + DIV_LEN / 2 + 1.2, inset_y + DIV_H / 2 + 1.1,
           "the hinge plates go here", size=8.5, anchor="middle")
    _caption(c, ox, inset_y + DIV_H + 6.0,
             "Sheet plan, 1/2 spruce: three strips, each one TV bottom plus two dividers. Inset not to the sheet scale.")
    name = "02-nest-spruce-12.svg"
    c.save(os.path.join(outdir, name))
    return name, "1/2 spruce nest: three 15-3/8 strips of one bottom plus two dividers, and the divider notch"


# ---------------------------------------------------------------------------
# 3. 5/8" MDF, Nest A, both sheets
# ---------------------------------------------------------------------------
def nest_mdf_58(outdir):
    L, W = MDF_SHEET
    ox = 6.0
    oy1, oy2 = 3.0, 3.0 + W + 8.0
    c = Canvas(ox + L + 3.0, oy2 + W + 4.5, scale=11.0, margin=0.5,
               title="Guide 02 - 5/8 MDF Nest A, two 49 x 97 sheets")

    # ---------------- sheet 1
    _sheet(c, ox, oy1, L, W, "5/8 MDF sheet 1")
    y = oy1
    c.rect(ox, y, TALL_H, TALL_RIGHT_W, fill=MAT["mdf58"])
    c.label(ox + TALL_H / 2, y + TALL_RIGHT_W / 2 - 1.4,
            ["tall right side  (EXPOSED FACE - mark it, keep it scratch-free)",
             f"{frac(TALL_H)} x {frac(TALL_RIGHT_W)}"], size=12)
    c.dim_h(ox, ox + TALL_H, y + TALL_RIGHT_W - 1.4, offset_px=-12)
    c.dim_v(y, y + TALL_RIGHT_W, ox - 1.0)
    _waste(c, ox + TALL_H + KERF, y, L - TALL_H - KERF, TALL_RIGHT_W,
           ["waste", frac(L - TALL_H - KERF)])
    _kerf_v(c, ox + TALL_H + KERF / 2, y, TALL_RIGHT_W)

    y = oy1 + TALL_RIGHT_W + KERF
    _kerf_h(c, ox, y - KERF / 2, L)
    c.rect(ox, y, TALL_DOOR_BLANK, TALL_DOOR_W, fill=MAT["mdf58"])
    c.label(ox + TALL_DOOR_BLANK / 2, y + TALL_DOOR_W / 2 - 1.4,
            ["tall door blank", f"{frac(TALL_DOOR_BLANK)} x {frac(TALL_DOOR_W)}",
             f"(finish {frac(TALL_H)} in guide 4)"], size=12)
    c.dim_h(ox, ox + TALL_DOOR_BLANK, y + TALL_DOOR_W - 1.2, offset_px=-12)
    c.dim_v(y, y + TALL_DOOR_W, ox - 1.0)
    _waste(c, ox + TALL_DOOR_BLANK + KERF, y, L - TALL_DOOR_BLANK - KERF, TALL_DOOR_W,
           ["waste", frac(L - TALL_DOOR_BLANK - KERF)])
    _kerf_v(c, ox + TALL_DOOR_BLANK + KERF / 2, y, TALL_DOOR_W)

    y = y + TALL_DOOR_W + KERF
    _kerf_h(c, ox, y - KERF / 2, L)
    c.rect(ox, y, TV_KICK_L, KICK_W, fill=MAT["mdf58"])
    c.dim_h(ox, ox + TV_KICK_L, y + KICK_W / 2, offset_px=-8)
    c.text(ox + TV_KICK_L / 2, y + KICK_W / 2 + 1.1, "kick, TV (left piece)", size=11)
    c.dim_v(y, y + KICK_W, ox - 1.0)
    _waste(c, ox + TV_KICK_L + KERF, y, L - TV_KICK_L - KERF, KICK_W,
           frac(L - TV_KICK_L - KERF))
    _kerf_v(c, ox + TV_KICK_L + KERF / 2, y, KICK_W)

    used1 = TALL_RIGHT_W + TALL_DOOR_W + KICK_W + 3 * KERF
    y = oy1 + used1
    _kerf_h(c, ox, y - KERF / 2, L)
    _waste(c, ox, y, L, W - used1, f"waste {frac(W - used1)}")
    c.dim_v(oy1, oy1 + used1, ox - 3.4, text=f"3 rips = {frac(used1)}")

    # ---------------- sheet 2
    _sheet(c, ox, oy2, L, W, "5/8 MDF sheet 2")
    door_no = 1
    for si in range(2):
        y = oy2 + si * (DOOR_W + KERF)
        if si:
            _kerf_h(c, ox, y - KERF / 2, L)
        c.dim_v(y, y + DOOR_W, ox - 1.0)
        x = ox
        for _ in range(3):
            c.rect(x, y, DOOR_BLANK, DOOR_W, fill=MAT["mdf58"])
            c.label(x + DOOR_BLANK / 2, y + DOOR_W / 2 - 1.2,
                    [f"TV door {door_no} blank", f"{frac(DOOR_BLANK)} x {frac(DOOR_W)}",
                     f"(finish {frac(DOOR_LEN)} in guide 4)"], size=10)
            door_no += 1
            x += DOOR_BLANK + KERF
            _kerf_v(c, x - KERF / 2, y, DOOR_W)
        c.dim_h(ox, x - KERF, y + DOOR_W - 1.0, offset_px=-11,
                text=f"3 x {frac(DOOR_BLANK)} = {frac(3 * DOOR_BLANK)}")
        _waste(c, x, y, ox + L - x, DOOR_W, frac(ox + L - x))

    y = oy2 + 2 * (DOOR_W + KERF)
    _kerf_h(c, ox, y - KERF / 2, L)
    c.rect(ox, y, TV_KICK_R, KICK_W, fill=MAT["mdf58"])
    c.dim_h(ox, ox + TV_KICK_R, y + KICK_W / 2, offset_px=-8)
    c.text(ox + TV_KICK_R / 2, y + KICK_W / 2 + 1.1, "kick, TV (right piece)", size=11)
    c.dim_v(y, y + KICK_W, ox - 1.0)
    _waste(c, ox + TV_KICK_R + KERF, y, L - TV_KICK_R - KERF, KICK_W,
           frac(L - TV_KICK_R - KERF))
    _kerf_v(c, ox + TV_KICK_R + KERF / 2, y, KICK_W)

    y = y + KICK_W + KERF
    _kerf_h(c, ox, y - KERF / 2, L)
    c.dim_v(y, y + KICK_W, ox - 1.0)
    x = ox
    for plen, pname in ((TALL_KICK, "kick, tall"), (KICK_RETURN, "kick return")):
        c.rect(x, y, plen, KICK_W, fill=MAT["mdf58"])
        c.dim_h(x, x + plen, y + KICK_W / 2, offset_px=-8)
        c.text(x + plen / 2, y + KICK_W / 2 + 1.1, pname, size=10)
        x += plen + KERF
        _kerf_v(c, x - KERF / 2, y, KICK_W)
    _waste(c, x, y, ox + L - x, KICK_W, frac(ox + L - x))

    used2 = 2 * DOOR_W + 2 * KICK_W + 4 * KERF
    y = oy2 + used2
    _kerf_h(c, ox, y - KERF / 2, L)
    _waste(c, ox, y, L, W - used2, f"waste {frac(W - used2)}")
    c.dim_v(oy2 + 2 * (DOOR_W + KERF), oy2 + used2, ox - 3.4,
            text=f"remaining {frac(W - 2 * DOOR_W - 3 * KERF)}: two {frac(KICK_W)} strips")

    c.text(ox + L, oy1 - 1.6, f"kerf {frac(KERF)} (dashed);  doors and the tall door "
                              f"roughed {frac(OVERSIZE)} long", size=11, anchor="end", color=DIM)
    _caption(c, ox, oy2 + W + 3.2,
             "Sheet plans, 5/8 MDF Nest A. Rips run the full 97 length; cross-cut after ripping.")
    name = "02-nest-mdf-58.svg"
    c.save(os.path.join(outdir, name))
    return name, "5/8 MDF Nest A: sheet 1 tall side, tall door and one kick strip; sheet 2 the six TV doors and the rest of the kicks"


# ---------------------------------------------------------------------------
# 4. 1/2" MDF slab sheet + hardboard sheet
# ---------------------------------------------------------------------------
def nest_mdf_12_hardboard(outdir):
    L1, W1 = MDF_SHEET
    L2, W2 = HARDBOARD_SHEET
    ox = 6.0
    oy1, oy2 = 3.0, 3.0 + W1 + 8.0
    c = Canvas(ox + L1 + 3.0, oy2 + W2 + 4.5, scale=11.0, margin=0.5,
               title="Guide 02 - 1/2 MDF slab sheet and the 1/8 hardboard sheet")

    # ---------------- 1/2 MDF
    _sheet(c, ox, oy1, L1, W1, "1/2 MDF")
    y = oy1
    c.rect(ox, y, L1, FENCE_W, fill=MAT["mdf12"])
    c.text(ox + L1 / 2, y + FENCE_W / 2,
           f"saw-guide FENCE  {frac(FENCE_W)} x {frac(L1)}  - rip off a long factory edge first", size=11)
    c.dim_v(y, y + FENCE_W, ox - 1.0)

    y = oy1 + FENCE_W + KERF
    _kerf_h(c, ox, y - KERF / 2, L1)
    c.rect(ox, y, SLAB_L, SLAB_W, fill=MAT["mdf12"])
    c.label(ox + SLAB_L / 2, y + SLAB_W / 2 - 1.4,
            ["TV top slab, left piece", f"{frac(SLAB_L)} x {frac(SLAB_W)}",
             "cut to length now"], size=12)
    c.dim_h(ox, ox + SLAB_L, y + SLAB_W - 1.2, offset_px=-12)
    c.dim_v(y, y + SLAB_W, ox - 1.0)
    _waste(c, ox + SLAB_L + KERF, y, L1 - SLAB_L - KERF, SLAB_W,
           ["waste", frac(L1 - SLAB_L - KERF)])
    _kerf_v(c, ox + SLAB_L + KERF / 2, y, SLAB_W)

    y = y + SLAB_W + KERF
    _kerf_h(c, ox, y - KERF / 2, L1)
    blank_r = SLAB_R + OVERSIZE
    c.rect(ox, y, blank_r, SLAB_W, fill=MAT["mdf12"])
    c.label(ox + blank_r / 2, y + SLAB_W / 2 - 1.4,
            ["TV top slab, right piece", f"{frac(blank_r)} x {frac(SLAB_W)}",
             f"leave {frac(OVERSIZE)} long: finish {frac(SLAB_R)} in guide 7"], size=12)
    c.dim_h(ox, ox + blank_r, y + SLAB_W - 1.2, offset_px=-12)
    c.dim_v(y, y + SLAB_W, ox - 1.0)
    _waste(c, ox + blank_r + KERF, y, L1 - blank_r - KERF, SLAB_W,
           ["waste", frac(L1 - blank_r - KERF)])
    _kerf_v(c, ox + blank_r + KERF / 2, y, SLAB_W)

    used = FENCE_W + 2 * SLAB_W + 3 * KERF
    y = oy1 + used
    _kerf_h(c, ox, y - KERF / 2, L1)
    _waste(c, ox, y, L1, W1 - used,
           f"leftover {frac(W1 - used)} x {frac(L1)}: paint test panels, hinge-plate template")
    c.dim_v(y, oy1 + W1, ox - 1.0)

    # ---------------- hardboard
    _sheet(c, ox, oy2, L2, W2, "1/8 hardboard")
    y = oy2
    c.rect(ox, y, BACK_L, BACK_W, fill=MAT["hardboard"])
    c.label(ox + BACK_L / 2, y + BACK_W / 2 - 1.0,
            ["tall back", f"{frac(BACK_L)} x {frac(BACK_W)}"], size=13, color="white")
    _dim_h_boxed(c, ox, ox + BACK_L, y + BACK_W - 1.4, offset_px=-12)
    c.dim_v(y, y + BACK_W, ox - 1.0)
    _waste(c, ox + BACK_L + KERF, y, L2 - BACK_L - KERF, BACK_W,
           ["waste", frac(L2 - BACK_L - KERF)])
    _kerf_v(c, ox + BACK_L + KERF / 2, y, BACK_W)

    y = oy2 + BACK_W + KERF
    _kerf_h(c, ox, y - KERF / 2, L2)
    c.rect(ox, y, L2, GUIDE_BASE_W, fill=MAT["hardboard"])
    c.text(ox + L2 / 2, y + GUIDE_BASE_W / 2,
           f"saw-guide BASE  {frac(GUIDE_BASE_W)} x {frac(L2)}", size=12, color="white")
    c.dim_v(y, y + GUIDE_BASE_W, ox - 1.0)

    y = y + GUIDE_BASE_W + KERF
    _kerf_h(c, ox, y - KERF / 2, L2)
    _waste(c, ox, y, L2, oy2 + W2 - y,
           f"leftover {frac(oy2 + W2 - y)} x {frac(L2)}: shelf-pin template")
    c.dim_v(y, oy2 + W2, ox - 1.0)

    c.text(ox + L1, oy1 - 1.6, f"kerf {frac(KERF)} (dashed)", size=11, anchor="end", color=DIM)
    _caption(c, ox, oy2 + W2 + 3.2,
             "Sheet plans: the 1/2 MDF gives the fence and both slab pieces; the hardboard gives the tall back and the guide base.")
    name = "02-nest-mdf-12-hardboard.svg"
    c.save(os.path.join(outdir, name))
    return name, "1/2 MDF slab sheet (fence strip, two 16 slab strips) and the 1/8 hardboard sheet (tall back, saw-guide base)"


# ---------------------------------------------------------------------------
# 5. 2x2 and 2x4 crosscut plan
# ---------------------------------------------------------------------------
def sticks(outdir):
    ox = 11.0
    oy = 3.0
    pitch2 = 4.6
    pitch4 = 6.4
    rows2 = len(STICKS_2X2)
    rows4 = len(STICKS_2X4)
    height = oy + rows2 * pitch2 + 3.5 + rows4 * pitch4 + 4.0
    c = Canvas(ox + BOARD_2X2 + 6.0, height, scale=11.0, margin=0.5,
               title="Guide 02 - crosscut plan for the 2x2 and 2x4 sticks")

    c.text(ox, oy - 1.7, "2x2 SPF, eight 8' boards (square one end first, measure every length from it)",
           size=13, anchor="start", weight="bold")
    c.text(ox + BOARD_2X2 + 0.4, oy - 0.7, "leftover", size=10, anchor="start", color=DIM)
    y = oy
    for label, cuts, left in STICKS_2X2:
        c.text(ox - 1.0, y + T2 / 2, label, size=12, anchor="end", weight="bold")
        c.line(ox, y - 0.5, ox, y + T2 + 0.5, stroke=LINE, sw=1.6)  # squared end
        x = ox
        for clen, cname in cuts:
            c.rect(x, y, clen, T2, fill=MAT["2x2"])
            c.dim_h(x, x + clen, y, offset_px=-6)
            c.text(x + clen / 2, y + T2 / 2 + 0.05, cname, size=9)
            x += clen + KERF
            _kerf_v(c, x - KERF / 2, y - 0.3, T2 + 0.6)
        if cuts:
            _waste(c, x, y, ox + BOARD_2X2 - x, T2, None)
            c.text(ox + BOARD_2X2 + 0.4, y + T2 / 2, frac(ox + BOARD_2X2 - x),
                   size=9, anchor="start", color=DIM)
        else:
            _waste(c, ox, y, BOARD_2X2, T2, None)
            c.text(ox + 1.0, y + T2 / 2,
                   "board #8 (on hand): kick sleepers, cut to suit in guide 6", size=10, anchor="start")
        c.rect(ox, y, BOARD_2X2, T2, fill="none", stroke=LINE, sw=1.2)
        y += pitch2

    y += 2.0
    c.text(ox, y - 1.7, "2x4 on hand (miter-saw crosscuts, no rips)",
           size=13, anchor="start", weight="bold")
    for label, blen, cuts, left in STICKS_2X4:
        c.text(ox - 1.0, y + T4 / 2, label, size=12, anchor="end", weight="bold")
        c.line(ox, y - 0.5, ox, y + T4 + 0.5, stroke=LINE, sw=1.6)
        x = ox
        for clen, cname in cuts:
            c.rect(x, y, clen, T4, fill=MAT["2x4"])
            c.dim_h(x, x + clen, y, offset_px=-6)
            c.text(x + clen / 2, y + T4 / 2, cname, size=10)
            x += clen + KERF
            _kerf_v(c, x - KERF / 2, y - 0.3, T4 + 0.6)
        if cuts:
            _waste(c, x, y, ox + blen - x, T4, None)
            c.text(ox + blen + 0.4, y + T4 / 2, frac(ox + blen - x),
                   size=9, anchor="start", color=DIM)
        else:
            _waste(c, ox, y, blen, T4, None)
            c.text(ox + 1.0, y + T4 / 2, f"untouched, {frac(blen)} - keep for shims, bearers and cauls",
                   size=10, anchor="start")
        c.rect(ox, y, blen, T4, fill="none", stroke=LINE, sw=1.2)
        y += pitch4

    c.text(ox + BOARD_2X2, oy - 1.7,
           f"kerf {frac(KERF)} after every cut (dashed)", size=11, anchor="end", color=DIM)
    _caption(c, ox - 10.0, y + 1.6,
             "Crosscut plan, bars to a common length scale. Hatched tails are the leftovers with the kerfs taken out - keep them, they are sleeper length.")
    name = "02-sticks.svg"
    c.save(os.path.join(outdir, name))
    return name, "Crosscut plan for the eight 2x2 boards and the 2x4 stock on hand, with leftovers hatched"


# ---------------------------------------------------------------------------
# 6. saw guide cross-section
# ---------------------------------------------------------------------------
def saw_guide(outdir):
    show = 3.0                      # guide 02: about 3" of base showing on the cut side
    behind = GUIDE_BASE_W - show - MDF12_T
    work_t = 5 / 8.0                # a 5/8 sheet under the guide
    work_over = 2.0                 # drawn overhang either side
    shoe_t = 1 / 4.0                # saw base plate, drawn
    ox = 5.0                        # left edge of the base = the cut line
    base_y = 5.0                    # top face of the workpiece
    by = base_y - HARDBOARD_T       # top face of the hardboard base
    fx = ox + show                  # fence, outward (factory) face
    fy = by - FENCE_W               # top of the fence
    sy = by - shoe_t                # top of the saw base plate
    c = Canvas(ox + GUIDE_BASE_W + work_over + 4.5, 10.0, scale=34.0, margin=0.5,
               title="Guide 02 - shop-made saw guide, cross-section")

    # --- top: how much base shows on the cut side, and the factory edge
    c.dim_h(ox, fx, 0.5, offset_px=12,
            text=f"{frac(show)} of base showing (the saw's own offset)")
    c.text(fx - 0.6, 1.40, "factory edge outward", size=11, anchor="end", color=DIM)
    c.line(fx - 0.5, 1.62, fx - 0.08, 1.95, stroke=DIM, sw=0.8)

    # --- workpiece
    c.rect(ox - work_over, base_y, GUIDE_BASE_W + 2 * work_over, work_t,
           fill=MAT["spruce58"])
    c.text(ox + GUIDE_BASE_W + work_over, base_y + work_t + 0.55,
           "workpiece (good face down)", size=11, anchor="end")

    # --- 1/8 hardboard base, 8" wide, lying on the workpiece
    c.rect(ox, by, GUIDE_BASE_W, HARDBOARD_T, fill=MAT["hardboard"])
    c.text(ox + GUIDE_BASE_W + 0.55, base_y - 0.75,
           f"{frac(HARDBOARD_T)} hardboard base", size=11, anchor="start")
    c.line(ox + GUIDE_BASE_W + 0.45, base_y - 0.62, ox + GUIDE_BASE_W - 0.4, by + 0.02,
           stroke=LINE, sw=0.8)
    c.dim_h(ox, ox + GUIDE_BASE_W, base_y + work_t + 2.6, offset_px=12,
            text=f"{frac(GUIDE_BASE_W)} base")

    # --- 1/2 MDF fence on top of the base, factory edge outward
    c.rect(fx, fy, MDF12_T, FENCE_W, fill=MAT["mdf12"])
    c.line(fx, fy, fx, fy + FENCE_W, stroke=DIM, sw=2.0)
    c.dim_v(fy, fy + FENCE_W, fx - 0.35, offset_px=-11)
    c.text(fx + MDF12_T + 1.2, 2.45,
           f"{frac(FENCE_W)} x {frac(MDF12_T)} MDF fence,", size=11, anchor="start")
    c.text(fx + MDF12_T + 1.2, 2.90,
           "glued and screwed to the base", size=11, anchor="start")
    c.dim_h(fx + MDF12_T, ox + GUIDE_BASE_W, 3.70, offset_px=-11, text=frac(behind))

    # --- saw base plate riding the fence, sliding on the base
    c.rect(ox, sy, show, shoe_t, fill=MAT["wall"])
    c.text(ox + 1.1, 4.15, "saw base plate", size=10)
    c.line(ox + 1.1, 4.32, ox + 1.1, sy - 0.07, stroke=LINE, sw=0.8)

    # --- cut line at the trimmed base edge
    c.line(ox, sy - 0.05, ox, base_y + work_t + 1.5, stroke=DIM, sw=1.8)
    c.text(ox + 0.3, base_y + work_t + 1.5,
           "trimmed base edge = CUT LINE", size=11, anchor="start", color=DIM)

    _caption(c, 0.2, 8.9,
             "Cross-section, schematic. One pass along the fence trims the base")
    _caption(c, 0.2, 9.4,
             "to the saw's own offset; after that, clamp the base edge to the mark.")
    name = "02-saw-guide.svg"
    c.save(os.path.join(outdir, name))
    return name, "Cross-section of the shop-made saw guide: 8 hardboard base, 3 MDF fence, base edge trimmed to the saw's offset"


# ---------------------------------------------------------------------------
def build(outdir):
    return [f(outdir) for f in (
        nest_spruce_58,
        nest_spruce_12,
        nest_mdf_58,
        nest_mdf_12_hardboard,
        sticks,
        saw_guide,
    )]


if __name__ == "__main__":
    for fn, cap in build("."):
        print(fn, "-", cap)
