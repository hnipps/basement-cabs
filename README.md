# Built-in wall cabinet

Parametric Fusion model of a wall-to-wall built-in: a tall cabinet on the left and a
low TV run to the right wall, both painted black. "Option 2-lite" construction (see
`guides/08-cost-reduction-options.md`): the tall cabinet is a frameless 5/8 spruce
plywood box with a 5/8 MDF exposed side and a 1/8 hardboard back; the TV run has no
boxes and no back, just a 2x2 ladder on the wall with the three 2x4 hanging rails as
its top-rear member, 1/2 spruce bottoms and dividers, a 1/2 MDF top slab in two
pieces and six 5/8 MDF doors that all hinge on the divider to their left. Both stand
on 2x2 sleepers behind 5/8 MDF kicks.

## Files

- `CUTLIST.md` — every part with size and nesting, generated from the model. The
  source of truth for the guides.
- `fusion/builtin_cabinet.py` — builds the whole model (48 bodies) from an empty
  Fusion Part design. All dimensions are Fusion user parameters (Modify > Change
  Parameters). Edit a parameter to move geometry; divider positions derive from the
  door width and hinge overlay. Changing the shelf or door count needs a rerun on an
  empty design.
- `fusion/cabinet_views/cabinet_views.py` — creates Selection Sets (one per view) and
  can isolate a view. Run it from Scripts and Add-Ins (Shift+S) and pick a number.
- `guides/00-overview.md` … `08-cost-reduction-options.md` — build guides, below.

## Viewing parts of the model

Seven Selection Sets live in the Fusion browser. Click one, press V to hide it, V
again to show it. Or run the `cabinet_views` script (Shift+S, Scripts tab,
double-click) and type a number to show only that group. The script also rebuilds the
sets after a model rebuild.

| Set | Hide it to | Show only it to |
|---|---|---|
| Doors | see the bays, dividers and rails | check door sizes and reveals |
| TV top slab | see the divider tops and where the slab seam lands | measure the slab |
| Tall cabinet | work on the TV run alone | build the tall cabinet |
| TV run | work on the tall cabinet alone | build the ladder |
| Ladder (2x2) | see bottoms and dividers without the stringers | cut and place the stringers and cross blocks |
| Rails (2x4) | see the divider notches empty | mark the stud screws |
| Kick | see the sleeper zone | cut the kick plates |

The script folder is symlinked into
`~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/` so Fusion finds
it without importing.

## Frame

X runs along the rear wall from the left wall. Rear wall is Y = 0, the room is at -Y,
so Fusion's Front view shows the door side with the tall cabinet on the left. Z up.
Inches.

## Build guides

| # | File | Covers |
|---|---|---|
| 0 | `guides/00-overview.md` | design summary, order of work, vocabulary |
| 1 | `guides/01-materials-and-tools.md` | shopping list with estimated cost |
| 2 | `guides/02-cutting.md` | nesting per sheet, 2x2 and 2x4 crosscut plans |
| 3 | `guides/03-tall-box-and-ladder.md` | tall box pocket-screw assembly; ladder build on the wall |
| 4 | `guides/04-doors-hinges-shelves.md` | hinge layout per door, cups, plates, shelf pins |
| 5 | `guides/05-finishing.md` | MDF-first priming, paint schedule |
| 6 | `guides/06-install.md` | studs, sleepers, tall cabinet, ladder, kicks, doors |
| 7 | `guides/07-top-slab.md` | 1/2 MDF slab in two pieces, seam fill |
| 8 | `guides/08-cost-reduction-options.md` | the options considered and unit prices |
