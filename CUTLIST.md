# Cut list — built-in cabinet (generated from the Fusion model, 2026-09-08)

Dimensions in inches, length x width. Thickness per material. Rip and cross-cut to
these sizes; the model is the source of truth (`fusion/builtin_cabinet.py`).

Parameters at time of export: wall 199-11/16, tall cabinet 18-3/8 W x 82-11/16 H x
24-7/16 D, TV cabinet 181-5/16 W x 15 H x 16 D, 3 TV boxes, 4-15/16 gap under.

## 3/4" plywood (carcass) — 3.2 sheets net, buy 5

| qty | length   | width   | part |
|----:|----------|---------|------|
| 1 | 82-11/16 | 23-7/16 | tall left side |
| 2 | 23-7/16  | 16-7/8  | tall top, bottom |
| 4 | 22-11/16 | 16-7/8  | tall shelves |
| 6 | 58-15/16 | 15      | TV box tops, bottoms |
| 6 | 15       | 14-1/4  | TV box sides |
| 3 | 15       | 12-3/4  | TV centre partitions — notch rear top corner 3-1/2 x 1-1/2 for the rail |
| 6 | 29-3/32  | 15      | TV shelves |
| 1 | 18-3/8   | 4-15/16 | kick, tall (flush) |
| 1 | 10-15/16 | 4-15/16 | kick return |
| 1 | 181-5/16 | 4-15/16 | kick, TV (recessed) — cut as 3 pieces, joints behind box seams |

## 3/4" MDF (paint-grade faces) — 1.9 sheets net, buy 3

| qty | length   | width   | part |
|----:|----------|---------|------|
| 1 | 82-11/16 | 23-7/16 | tall right side (exposed face) |
| 1 | 82-11/16 | 18-1/8  | tall door |
| 6 | 30-1/32  | 14-1/8  | TV doors |
| 1 | 181-5/16 | 16      | TV top slab — 2 pieces, joint over a box, fill and paint |

## 1/4" plywood (backs) — 0.9 sheets net, buy 1 (tight) or 2

| qty | length   | width   | part |
|----:|----------|---------|------|
| 1 | 82-11/16 | 18-3/8  | tall back |
| 3 | 60-7/16  | 14-1/4  | TV box backs |

## Solid lumber — 2x4 on hand (1-1/2" x 3-1/2" actual)

All five hanging rails come from 2x4 stock already on hand, not plywood. A 2x4 arrives
at exactly 3-1/2" wide with parallel factory edges, so every rail is a miter-saw
crosscut and none of the five long narrow rips are needed.

| qty | length   | width | part |
|----:|----------|-------|------|
| 3 | 58-15/16 | 3-1/2 | TV hanging rails |
| 2 | 16-7/8   | 3-1/2 | tall hanging rails |

Crosscut plan from the boards on hand:

| board | cut | leftover |
|---|---|---|
| 8' (96") #1 | one TV rail 58-15/16 | 37" |
| 8' (96") #2 | one TV rail 58-15/16 | 37" |
| 6-1/2' (78") #1 | one TV rail 58-15/16 | 19" |
| 47" | both tall rails 16-7/8 | 13" |
| 6-1/2' (78") #2 | untouched | 78" |

Uses 210-9/16 of the 395" available. Leftover: one full 78" 2x4 plus 106" of offcut.
The 8' 2x2 has no part in the design; keep it for cauls and spacer sticks.

## Notes

- Backs are nailed over the rear edges of the box, so carcass depth = cabinet depth
  minus 1/4" back minus 3/4" door.
- Doors are full overlay: 1/8" reveal between doors and under the top slab, 1/4"
  clearance at walls and at the tall cabinet side.
- Kick plates sit on adjustable legs (100 mm size), not modelled.
- Rails are 1-1/2 thick solid lumber, not 3/4 plywood. Each one projects 3/4 further
  into the box, so the top 3-1/2 band of every box loses 3/4 of depth. Confirmed
  acceptable: nothing deep goes in a TV top bay. Tall cabinet rails sit tight under
  the top and on top of the bottom, above and below every shelf, so nothing fouls.
- Wall screws must be #10 x 4", not 3". The stack to the stud is rail 1-1/2 + back
  1/4 + drywall 1/2 = 2-1/4, leaving 1-3/4 of stud bite. A 3" screw reaches only 3/4.
- Pocket holes in the rail ends: set the jig for 1-1/2 stock, 2-1/2" coarse screws,
  two pockets per end. Screwing into a 1-1/2 rail end beats a 3/4 plywood edge.
- Plane the rounded factory arris off both long edges of each rail's rear face so the
  1/4 back nails flat against it.
- The rail crosses the TV centre partition, so each partition needs its rear top
  corner notched 3-1/2 (up) x 1-1/2 (in) to let the rail run through in one piece.
  This notch was always needed; it was 3/4 deep when the rail was plywood. The Fusion
  model cuts it parametrically, using the rail body as the cutting tool, so it tracks
  `rail_t` and `rail_h`. Removed volume per partition: 3-15/16 cubic inches.
- Sight every 2x4 for bow before cutting and use the two straightest for the 58-15/16
  rails; a bowed rail pushes the box out of plumb.
