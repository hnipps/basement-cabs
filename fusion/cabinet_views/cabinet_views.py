# Cabinet view helper for the built-in cabinet model (see builtin_cabinet.py).
# Creates one Fusion Selection Set per view (browser > Selection Sets; click a set,
# press V to hide/show it) and can isolate a single view.
#
# Run from Fusion's Scripts and Add-Ins panel (Shift+S) for an interactive prompt,
# or via MCP with INTERACTIVE = False and ISOLATE set to a view name (or "All").
import adsk.core, adsk.fusion

INTERACTIVE = True
ISOLATE = None  # e.g. "TV run"

def _rule(prefix=None, has=None, without=()):
    def f(n):
        if prefix and not n.startswith(prefix):
            return False
        if has and has not in n:
            return False
        return not any(w in n for w in without)
    return f

# ordered: name -> membership rule on body name
VIEWS = [
    ("All",          _rule()),
    ("Tall cabinet", _rule(prefix="TallCabinet_")),
    ("TV run",       _rule(prefix="TVRun_")),
    ("Doors",        lambda n: "Door" in n and "Packer" not in n),
    ("TV top slab",  _rule(prefix="TVRun_TopSlab")),
    ("Ladder (2x2)", lambda n: "Stringer" in n or "CrossBlock" in n),
    ("Kick",         _rule(prefix="Kick_")),
    ("Sleepers",     _rule(prefix="Sleeper_")),
    ("Rails (2x4)",  _rule(has="Rail")),
]

def run(context):
    app = adsk.core.Application.get()
    ui = app.userInterface
    design = adsk.fusion.Design.cast(app.activeProduct)
    root = design.rootComponent
    bodies = list(root.bRepBodies)
    sets = design.selectionSets
    # refresh selection sets
    for s in list(sets):
        s.deleteMe()   # this script owns all selection sets in the document
    made = []
    for name, rule in VIEWS:
        if name == "All":
            continue
        members = [b for b in bodies if rule(b.name)]
        if members:
            sets.add(members, name)
            made.append("%s (%d)" % (name, len(members)))
    choice = ISOLATE
    if INTERACTIVE:
        menu = "\n".join("%2d  %s" % (i + 1, v) for i, (v, _) in enumerate(VIEWS))
        ans, cancelled = ui.inputBox("Isolate which view? (number, blank = leave as is)\n" + menu, "Cabinet views", "1")
        if not cancelled and ans.strip():
            try:
                choice = VIEWS[int(ans.strip()) - 1][0]
            except (ValueError, IndexError):
                choice = None
    if choice:
        rule = dict(VIEWS)[choice]
        shown = 0
        for b in bodies:
            b.isVisible = rule(b.name)
            shown += b.isVisible
        app.activeViewport.fit()
        print("isolated '%s': %d of %d bodies visible" % (choice, shown, len(bodies)))
    print("selection sets: " + "; ".join(made))
