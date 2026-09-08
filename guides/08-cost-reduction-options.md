# 8. Cost reduction options (2026-09-08)

Prices are CAD, Home Depot Canada unless noted, mostly estimates anchored to RONA, IKEA and
Amazon.ca snippets (homedepot.ca blocks price fetches). Treat every figure as ±20% and
verify by postal code before buying. Tax excluded. Kreg 320 jig ($58) excluded as a tool.

## Unit prices used

| Item | CAD |
|---|---|
| 3/4" birch plywood 4x8 | 85 |
| 5/8" spruce plywood 4x8 | 45 |
| 1/2" spruce plywood 4x8 | 38 |
| 3/4" MDF 49x97 | 60 |
| 5/8" MDF 49x97 | 52 |
| 1/2" MDF 49x97 | 47 |
| 1/4" plywood underlay 4x8 | 35 |
| 1/8" hardboard 4x8 | 20 |
| 2x2x8 SPF | 4 |
| Euro hinge 110° soft-close full overlay, Amazon.ca 10-pk / 20-pk | 30 / 45 |
| Same hinge, HD Richelieu 105° soft-close 2-pk | 15.48 |
| IKEA UTRUSTA 110° soft-close 2-pk | 22 |
| 5 mm shelf pins, 50 | 13 |
| Kreg pocket screws 1-1/4" x100 / 2-1/2" x50 | 13 / 11 |
| GRK R4 #10 x 4" x50 | 26 |
| #8 x 2-1/2" construction screws x100 | 12 |
| Cabinet legs 4-pk / kick clips 20-pk | 12 / 12 |
| Bar pulls black 15-pk | 42 |
| Zinsser 1-2-3 primer gal + Behr Premium Plus black eggshell gal + rollers/pads | 50 + 48 + 22 = 120 |

## Option totals

| | Current design | Opt 1: open TV ladder | Opt 2: doored TV ladder | Opt 2-lite | Opt 3: 5/8 spruce boxes |
|---|---:|---:|---:|---:|---:|
| Sheet goods + lumber | 675 | 251 | 300 | 286 | 371 |
| Hinges (Amazon) | 45 | 30 | 60 | 60 | 45 |
| Legs + clips | 60 | 0 | 0 | 0 | 0 |
| Shelf pins | 13 | 13 | 13 | 13 | 13 |
| Screws | 88 | 62 | 62 | 62 | 88 |
| Paint + sundries | 120 | 120 | 120 | 120 | 120 |
| Pulls (optional) | 42 | 0 | 42 | 42 | 42 |
| **Total without pulls** | **1001** | **476** | **555** | **541** | **637** |
| With HD Richelieu hinges instead | +94 | +47 | +72 | +72 | +94 |

IKEA BESTÅ equivalent (4 frames 120x40x38 + 8 LAPPVIKEN doors + rails + hinges, plus one
60x40x192 frame with 3 doors and 4 shelves): about **985** before tax.

## The options

Common to all: five hanging rails from the 2x4s on hand; every visible face is MDF; all
doors 5/8" MDF (a 35 mm hinge cup in 1/2" MDF breaks through); 1/2" MDF top slab in 2
pieces; tall cabinet carcass 5/8" spruce behind its door; 1/8" hardboard tall back.

**Opt 1, open TV ladder, wall as back.** TV run is a 181" ladder of 2x2 stringers (bottom
front and rear, 7 cross blocks) with the 2x4 rails as the top rear member screwed to studs.
No back panel, no box tops, no box sides. Three 1/2" MDF bottoms, six 1/2" MDF dividers
notched for the rail, 1/2" MDF top on continuous stringers. No TV doors, no TV shelves.
Tall cabinet: 5/8" spruce carcass, 3/4" MDF exposed right side and door from one sheet.
Sheets: 2x 1/2" MDF, 1x 3/4" MDF, 1x 5/8" spruce, 1x hardboard, 8x 2x2.
Downside: open bays, contents on show; 1/2" dividers cannot take hinges later.

**Opt 2, doored TV ladder (recommended if doors stay).** Same ladder. Bottoms and dividers
in 5/8" MDF so dividers take hinge plates. All 7 doors from one 5/8" MDF sheet (needs a
true 49" sheet). Every TV door hinges on the divider to its left and swings the same way:
door 1 full overlay, doors 2 to 6 half overlay (second hinge SKU). Tall exposed side 5/8"
MDF. Sheets: 3x 5/8" MDF, 1x 1/2" MDF, 1x 5/8" spruce, 1x hardboard, 8x 2x2.
Downside: run only comes square on the wall; 82" 5/8" door must be primed both faces same
session or it bows; TV bay interior drops to 12-3/8".

**Opt 2-lite.** Opt 2 with bottoms and dividers in 1/2" spruce instead of 5/8" MDF. Saves
one 5/8 MDF sheet for a 1/2 spruce sheet. Hinge plates in 1/2" ply hold, but use the
longest plate screws. Spruce is hidden behind doors.

**Opt 3, current layout in 5/8" spruce.** Three frameless boxes and tall box in 5/8"
spruce sheathing, 1/8" hardboard backs, 1/2" MDF top glued on, 5/8" MDF doors and
exposed side. Boxes square on the floor, stock full-overlay hinges only. Sheets: 4x 5/8"
spruce, 2x 5/8" MDF, 1x 1/2" MDF, 2x hardboard. Downside: knotty spruce interior under
black paint (skim or accept), most cutting and painting of the four.

**Opt 4, melamine shelving boards.** 12 boards run about the same as 6 sheets, particleboard
sags and strips screws. Not cheaper. Dropped.

## Where the money goes

Paint and sundries ($120) plus screws and pins ($75) are fixed at roughly $195 whatever
the carcass. Sheet goods for the cheapest doored design are about $290. So $300 all-in is
not reachable with paint and hardware included; $300 is reachable for sheet goods alone.
Under $500 needs Opt 1 (open bays) or Opt 2-lite with Amazon hinges, no pulls, and no
price surprises.

Cheap wins that apply to any option: buy hinges as a 20-pack on Amazon.ca (saves $70 to
$95 versus Home Depot pairs), skip legs and clips (2x2 sleepers and shims behind the
kick), skip pulls (push latches or finger pull at the door edge), one primer gallon not
BIN (use a BIN quart only on MDF edges if they fuzz).

## Fusion model changes for Opt 2 (`fusion/builtin_cabinet.py`)

`box_t` 3/4 to 5/8, tall right side as 5/8 MDF; `door_t` 3/4 to 5/8; `slab_t` 3/4 to 1/2
and TV frame height 14-1/4 to 14-1/2; TV `back_t` to 0 (carcass depth = depth minus door),
tall `back_t` to 1/8; TV boxes 3 to 0, replaced by a ladder body (2x2 stringers front and
rear at the bottom, 7 cross blocks, one 2x2 top front stringer), 3 bottoms and 6 dividers
at equal pitch notched by the rail body; per-door hinge side (all left, door 1 full
overlay, rest half overlay); TV door height 14-3/8; kicks in MDF. CUTLIST.md and guides
1 to 4 and 7 need regenerating after the script rerun.
