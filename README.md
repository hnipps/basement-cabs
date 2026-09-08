# Built-in wall cabinet

Parametric Fusion model of a wall-to-wall built-in: a tall cabinet on the left and a
low TV cabinet run to the right wall, both painted black.

## Files

- `fusion/builtin_cabinet.py` — builds the whole model from an empty Fusion Part design.
  All dimensions are Fusion user parameters (Modify > Change Parameters). Edit a
  parameter to move geometry. Changing the shelf, door, or box counts needs a rerun
  on an empty design.
- `fusion/cabinet_views.py` — creates Selection Sets (one per view) and can isolate a
  view. Run it from Scripts and Add-Ins (Shift+S) and pick a number.

## Viewing parts of the model

Six Selection Sets live in the Fusion browser. Click one, press V to hide it, V again to
show it. Or run the `cabinet_views` script (Shift+S, Scripts tab, double-click) and type a
number to show only that group. The script also rebuilds the sets after a model rebuild.

| Set | Hide it to | Show only it to |
|---|---|---|
| Doors | see inside every box, check shelves and rails | check door sizes and reveals |
| TV top slab | see the TV box tops and where the slab seam lands | measure the slab |
| Tall cabinet | work on the TV run alone | build the tall cabinet |
| TV cabinet | work on the tall cabinet alone | build the TV boxes |
| Shelves | see the bare carcass | check shelf sizes |
| Kick | see the legs zone | cut the kick plates |

The script folder is symlinked into
`~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/` so Fusion finds
it without importing.

## Frame

X runs along the rear wall from the left wall. Rear wall is Y = 0, the room is at -Y,
so Fusion's Front view shows the door side with the tall cabinet on the left. Z up.
Inches.

## Build guides

Step-by-step guides live in `guides/`, starting at `guides/00-overview.md`. The cut
list is `CUTLIST.md`.
