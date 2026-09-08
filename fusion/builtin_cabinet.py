# Built-in wall cabinet: tall cabinet (left) + TV cabinet (right).
# Run inside Fusion (via MCP execute). Fully parametric via user parameters;
# every panel position and size is a sketch dimension / offset expression.
# World frame: X along rear wall from left wall, rear wall at Y=0 with the room at -Y
# (so Fusion's front view shows the door side, tall cabinet on the left), Z up. Inches.
# Layout expressions below use y measured from the rear wall into the room; panel() mirrors.
import adsk.core, adsk.fusion, traceback

def run(context):
    """Entry point: Fusion MCP execute and the Scripts panel both call run(context)."""
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    design.fusionUnitsManager.distanceDisplayUnits = adsk.fusion.DistanceUnits.InchDistanceUnits
    root = design.rootComponent
    out = []
    if root.bRepBodies.count:
        raise RuntimeError("document already has %d bodies; start from an empty design" % root.bRepBodies.count)

    # name, expression, unit, comment
    PARAMS = [
        ("wall_w", "199.6875", "in", "rear wall width, left wall to right wall"),
        ("tall_w", "18.375", "in", "tall cabinet outside width (measured)"),
        ("tall_h", "82.6875", "in", "tall cabinet outside height"),
        ("tall_depth", "24.4375", "in", "tall cabinet depth incl. door face (measured)"),
        ("tv_h", "15", "in", "TV cabinet outside height incl. top slab"),
        ("tv_depth", "16", "in", "TV cabinet depth incl. door face (confirmed)"),
        ("panel_h", "19.9375", "in", "wall panelling bottom edge above floor = TV cabinet top"),
        ("ply", "0.75", "in", "carcass / shelf / door stock thickness"),
        ("top_t", "0.75", "in", "TV top slab thickness (0.75 painted MDF, 1.5 for a wood top with nosing)"),
        ("top_overhang", "0", "in", "TV top slab overhang past the door faces (0 flush; 0.75 typical for wood)"),
        ("back_t", "0.25", "in", "back panel thickness"),
        ("reveal", "0.125", "in", "gap between neighbouring overlay doors, and door to top slab"),
        ("end_gap", "0.25", "in", "door edge clearance to a wall or to the tall cabinet side"),
        ("rail_h", "3.5", "in", "hanging rail width, top rear inside box (2x4 stock is 3-1/2 wide)"),
        ("rail_t", "1.5", "in", "hanging rail thickness (1-1/2 solid 2x4 on hand; was 0.75 ply)"),
        ("kick_setback", "2.5", "in", "TV cabinet kick plate recess behind door faces"),
        ("tall_kick_setback", "0", "in", "tall cabinet kick plate recess (0 = flush with doors)"),
        ("tall_shelves", "4", "", "shelf count in tall cabinet (rebuild script to change)"),
        ("tall_doors", "1", "", "door count on tall cabinet (rebuild script to change)"),
        ("tv_boxes", "3", "", "TV cabinet box count, 2 bays per box (rebuild script to change)"),
        ("gap", "panel_h - tv_h", "in", "floor to cabinet underside (kick or float)"),
        ("tv_w", "wall_w - tall_w", "in", "TV cabinet outside width"),
        ("box_w", "tv_w / tv_boxes", "in", "TV cabinet box outside width"),
        ("box_h", "tv_h - top_t", "in", "TV cabinet box height under the top slab"),
        ("bay_w", "(box_w - 3 * ply) / 2", "in", "TV cabinet clear bay width (2 bays per box)"),
        ("tv_door_w", "(tv_w - 2 * end_gap - (2 * tv_boxes - 1) * reveal) / (2 * tv_boxes)", "in", "TV overlay door width"),
        ("tv_door_h", "box_h - reveal", "in", "TV overlay door height (flush with box bottom, reveal under top slab)"),
        ("tall_door_w", "(tall_w - end_gap - (tall_doors - 1) * reveal) / tall_doors", "in", "tall overlay door width"),
    ]

    ups = design.userParameters
    for name, expr, unit, comment in PARAMS:
        p = ups.itemByName(name)
        if p:
            p.expression = expr
        else:
            p = ups.add(name, adsk.core.ValueInput.createByString(expr), unit, comment)

    # numeric shadow for zero checks and verification
    V = {}
    for name, expr, unit, _ in PARAMS:
        V[name] = eval(expr, {}, V)

    def ev(expr):
        return float(eval(expr, {}, dict(V)))

    IN = 2.54
    AX = {"x": 0, "y": 1, "z": 2}

    def dominant(vec):
        comps = [vec.x, vec.y, vec.z]
        i = max(range(3), key=lambda k: abs(comps[k]))
        return i, (1 if comps[i] > 0 else -1)

    def panel(comp, name, thin, lo, size):
        """lo/size: dicts axis->expression string (inches)."""
        base = {"x": comp.yZConstructionPlane, "y": comp.xZConstructionPlane, "z": comp.xYConstructionPlane}[thin]
        # Layout is written with y measured from the rear wall into the room. Fusion's
        # front view looks toward +Y, so mirror y: room side is -Y and the door side
        # faces the viewer with the tall cabinet on the left.
        lo = dict(lo)
        lo["y"] = "-((%s) + (%s))" % (lo["y"], size["y"])
        off_expr = lo[thin]
        if abs(ev(off_expr)) < 1e-9:
            plane = base
        else:
            pin = comp.constructionPlanes.createInput()
            pin.setByOffset(base, adsk.core.ValueInput.createByString(off_expr))
            plane = comp.constructionPlanes.add(pin)
            plane.name = name + "_plane"
        sk = comp.sketches.add(plane)
        name = comp.name + "_" + name
        sk.name = name
        lo_v = [ev(lo[a]) for a in "xyz"]
        hi_v = [lo_v[i] + ev(size[a]) for i, a in enumerate("xyz")]
        ti = AX[thin]
        mid_thin = lo_v[ti]
        def wpt(sel):  # sel: 3 flags 0=lo 1=hi, thin axis forced to plane
            c = [hi_v[i] if sel[i] else lo_v[i] for i in range(3)]
            c[ti] = mid_thin
            return adsk.core.Point3D.create(c[0] * IN, c[1] * IN, c[2] * IN)
        corners = [sk.modelToSketchSpace(wpt(s)) for s in ((0,0,0),(1,1,1))]
        xs = [p.x for p in corners]; ys = [p.y for p in corners]
        p1 = adsk.core.Point3D.create(min(xs), min(ys), 0)
        p2 = adsk.core.Point3D.create(max(xs), max(ys), 0)
        rect = sk.sketchCurves.sketchLines.addTwoPointRectangle(p1, p2)
        pts = {}
        for i in range(rect.count):
            for sp in (rect.item(i).startSketchPoint, rect.item(i).endSketchPoint):
                g = sp.geometry
                key = (round(g.x, 6), round(g.y, 6))
                pts[key] = sp
        def find(x, y):
            return min(pts.values(), key=lambda sp: (sp.geometry.x - x) ** 2 + (sp.geometry.y - y) ** 2)
        A = find(p1.x, p1.y); B = find(p2.x, p1.y); D = find(p1.x, p2.y)
        # map sketch axes to world axes
        xi, xsgn = dominant(sk.xDirection)
        yi, ysgn = dominant(sk.yDirection)
        axn = "xyz"
        dims = sk.sketchDimensions
        H = adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation
        Vo = adsk.fusion.DimensionOrientations.VerticalDimensionOrientation
        def tp(x, y):
            return adsk.core.Point3D.create(x, y, 0)
        d = dims.addDistanceDimension(A, B, H, tp((p1.x + p2.x) / 2, p1.y - 2))
        d.parameter.expression = size[axn[xi]]
        d = dims.addDistanceDimension(A, D, Vo, tp(p1.x - 2, (p1.y + p2.y) / 2))
        d.parameter.expression = size[axn[yi]]
        # position of A (min sketch corner) relative to origin
        for sk_axis, wi, sgn in (("x", xi, xsgn), ("y", yi, ysgn)):
            wa = axn[wi]
            pos_expr = lo[wa] if sgn > 0 else "(%s) + (%s)" % (lo[wa], size[wa])
            if ev(pos_expr) < 0:
                pos_expr = "-(%s)" % pos_expr
            if abs(ev(pos_expr)) < 1e-9:
                if sk_axis == "x":
                    sk.geometricConstraints.addVerticalPoints(A, sk.originPoint)
                else:
                    sk.geometricConstraints.addHorizontalPoints(A, sk.originPoint)
            else:
                if sk_axis == "x":
                    d = dims.addDistanceDimension(sk.originPoint, A, H, tp(p1.x / 2, p1.y - 4))
                else:
                    d = dims.addDistanceDimension(sk.originPoint, A, Vo, tp(p1.x - 4, p1.y / 2))
                d.parameter.expression = pos_expr
        prof = sk.profiles.item(0)
        ni, nsgn = dominant(plane.geometry.normal)
        dist = size[thin] if nsgn > 0 else "-(%s)" % size[thin]
        ext = comp.features.extrudeFeatures
        ein = ext.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        ein.setDistanceExtent(False, adsk.core.ValueInput.createByString(dist))
        f = ext.add(ein)
        f.name = name
        body = f.bodies.item(0)
        body.name = name
        # verify
        bb = body.boundingBox
        got = [bb.minPoint.x / IN, bb.minPoint.y / IN, bb.minPoint.z / IN, bb.maxPoint.x / IN, bb.maxPoint.y / IN, bb.maxPoint.z / IN]
        exp = lo_v + hi_v
        err = max(abs(g - e) for g, e in zip(got, exp))
        out.append("%-22s %s %s size %.3f x %.3f x %.3f%s" % (
            name, "OK " if err < 1e-3 else "BAD", "",
            hi_v[0] - lo_v[0], hi_v[1] - lo_v[1], hi_v[2] - lo_v[2],
            "" if err < 1e-3 else "  got %s exp %s" % (got, exp)))
        return body

    class Grp:
        """Part Design docs allow one component; group bodies by name prefix."""
        def __init__(self, name):
            self.name = name
            self.comp = root
            self.constructionPlanes = root.constructionPlanes
            self.sketches = root.sketches
            self.features = root.features
            self.xYConstructionPlane = root.xYConstructionPlane
            self.yZConstructionPlane = root.yZConstructionPlane
            self.xZConstructionPlane = root.xZConstructionPlane

    def new_comp(name):
        return Grp(name)

    def notch(target, tool, name):
        """Cut `tool` out of `target`, keeping the tool body."""
        tools = adsk.core.ObjectCollection.create()
        tools.add(tool)
        cin = root.features.combineFeatures.createInput(target, tools)
        cin.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
        cin.isKeepToolBodies = True
        cin.isNewComponent = False
        f = root.features.combineFeatures.add(cin)
        f.name = name
        out.append("%-22s NOTCH cut by %s" % (name, tool.name))

    # Construction: frameless 3/4" plywood boxes, full-overlay slab doors (MDF) so no
    # carcass edge shows from the front. Back panel (1/4") nailed over the rear edges, so
    # carcass panels start at y = back_t. Carcass front face sits one door thickness
    # behind the cabinet depth. Hanging rail (rail_t x rail_h solid lumber) inside each
    # box, top rear. Rails are 2x4, not plywood: see CUTLIST.md for the crosscut plan.
    # TV boxes carry one continuous MDF top slab. Materials: 3/4 plywood carcass; 3/4 MDF for
    # doors, top slab and the tall cabinet RIGHT side (the only exposed carcass face); 1/4 ply backs. Kick plate recessed, on adjustable legs.
    # ---------------- Tall cabinet ----------------
    tc = new_comp("TallCabinet")
    cd = "tall_depth - back_t - ply"   # carcass panel depth
    panel(tc, "LeftSide", "x", {"x": "0", "y": "back_t", "z": "gap"}, {"x": "ply", "y": cd, "z": "tall_h"})
    panel(tc, "RightSide", "x", {"x": "tall_w - ply", "y": "back_t", "z": "gap"}, {"x": "ply", "y": cd, "z": "tall_h"})
    panel(tc, "Bottom", "z", {"x": "ply", "y": "back_t", "z": "gap"}, {"x": "tall_w - 2*ply", "y": cd, "z": "ply"})
    panel(tc, "Top", "z", {"x": "ply", "y": "back_t", "z": "gap + tall_h - ply"}, {"x": "tall_w - 2*ply", "y": cd, "z": "ply"})
    panel(tc, "Back", "y", {"x": "0", "y": "0", "z": "gap"}, {"x": "tall_w", "y": "back_t", "z": "tall_h"})
    panel(tc, "RailTop", "y", {"x": "ply", "y": "back_t", "z": "gap + tall_h - ply - rail_h"}, {"x": "tall_w - 2*ply", "y": "rail_t", "z": "rail_h"})
    panel(tc, "RailBottom", "y", {"x": "ply", "y": "back_t", "z": "gap + ply"}, {"x": "tall_w - 2*ply", "y": "rail_t", "z": "rail_h"})
    n = int(V["tall_shelves"])
    for i in range(1, n + 1):
        panel(tc, "Shelf%d" % i, "z",
              {"x": "ply", "y": "back_t + ply", "z": "gap + %d*tall_h/(tall_shelves+1) - ply/2" % i},
              {"x": "tall_w - 2*ply", "y": "tall_depth - back_t - 2*ply", "z": "ply"})
    nd = int(V["tall_doors"])
    for k in range(nd):   # end_gap at the left wall; right door edge flush with the exposed right side
        panel(tc, "Door%d" % (k + 1), "y",
              {"x": "end_gap + %d*(tall_door_w + reveal)" % k, "y": "tall_depth - ply", "z": "gap"},
              {"x": "tall_door_w", "y": "ply", "z": "tall_h"})

    # ---------------- TV cabinet: tv_boxes separate boxes, 2 bays each ----------------
    tv = new_comp("TVCabinet")
    cd = "tv_depth - back_t - ply"
    nb = int(V["tv_boxes"])
    for j in range(nb):
        b = "B%d_" % (j + 1)
        x0 = "tall_w + %d*box_w" % j
        panel(tv, b + "LeftSide", "x", {"x": x0, "y": "back_t", "z": "gap"}, {"x": "ply", "y": cd, "z": "box_h"})
        panel(tv, b + "RightSide", "x", {"x": x0 + " + box_w - ply", "y": "back_t", "z": "gap"}, {"x": "ply", "y": cd, "z": "box_h"})
        panel(tv, b + "Bottom", "z", {"x": x0 + " + ply", "y": "back_t", "z": "gap"}, {"x": "box_w - 2*ply", "y": cd, "z": "ply"})
        panel(tv, b + "Top", "z", {"x": x0 + " + ply", "y": "back_t", "z": "gap + box_h - ply"}, {"x": "box_w - 2*ply", "y": cd, "z": "ply"})
        panel(tv, b + "Back", "y", {"x": x0, "y": "0", "z": "gap"}, {"x": "box_w", "y": "back_t", "z": "box_h"})
        rail_b = panel(tv, b + "Rail", "y", {"x": x0 + " + ply", "y": "back_t", "z": "gap + box_h - ply - rail_h"}, {"x": "box_w - 2*ply", "y": "rail_t", "z": "rail_h"})
        part_b = panel(tv, b + "Partition", "x", {"x": x0 + " + ply + bay_w", "y": "back_t", "z": "gap + ply"}, {"x": "ply", "y": cd, "z": "box_h - 2*ply"})
        # The rail runs the full inside width, so it crosses the centre partition. Cut the
        # notch with the rail itself as the tool body: it then tracks rail_t and rail_h
        # instead of being a hardcoded pocket. Hand saw and chisel in the real build.
        notch(part_b, rail_b, tv.name + "_" + b + "PartitionNotch")
        for k, side in enumerate(("L", "R")):
            bx0 = "%s + ply + %d*(bay_w + ply)" % (x0, k)
            panel(tv, b + "Shelf" + side, "z",
                  {"x": bx0, "y": "back_t", "z": "gap + box_h/2 - ply/2"},
                  {"x": "bay_w", "y": "tv_depth - back_t - ply", "z": "ply"})
    # overlay doors run across box joints: 2 per box, evenly spaced over the whole TV run
    for d in range(2 * nb):
        panel(tv, "Door%d" % (d + 1), "y",
              {"x": "tall_w + end_gap + %d*(tv_door_w + reveal)" % d, "y": "tv_depth - ply", "z": "gap"},
              {"x": "tv_door_w", "y": "ply", "z": "tv_door_h"})
    # continuous top slab: rear wall to door face, tall cabinet side to right wall
    panel(tv, "TopSlab", "z", {"x": "tall_w", "y": "0", "z": "gap + box_h"}, {"x": "tv_w", "y": "tv_depth + top_overhang", "z": "top_t"})

    # ---------------- Kick plates, recessed, stepped at the tall cabinet ----------------
    kk = new_comp("Kick")
    panel(kk, "Tall", "y", {"x": "0", "y": "tall_depth - tall_kick_setback - ply", "z": "0"}, {"x": "tall_w", "y": "ply", "z": "gap"})
    panel(kk, "Return", "x", {"x": "tall_w - ply", "y": "tv_depth - kick_setback - ply", "z": "0"},
          {"x": "ply", "y": "tall_depth - tall_kick_setback - ply - (tv_depth - kick_setback - ply)", "z": "gap"})
    panel(kk, "TV", "y", {"x": "tall_w", "y": "tv_depth - kick_setback - ply", "z": "0"}, {"x": "tv_w", "y": "ply", "z": "gap"})

    # selection sets (click one in the browser, press V to hide/show)
    for s_ in list(design.selectionSets):
        s_.deleteMe()
    def _rule(prefix=None, has=None):
        return lambda nm: (not prefix or nm.startswith(prefix)) and (not has or has in nm)
    for nm, rule in [("Tall cabinet", _rule(prefix="TallCabinet_")), ("TV cabinet", _rule(prefix="TVCabinet_")),
                     ("Doors", _rule(has="Door")), ("TV top slab", _rule(prefix="TVCabinet_TopSlab")),
                     ("Shelves", _rule(has="Shelf")), ("Kick", _rule(prefix="Kick_")),
                     ("Rails (2x4)", _rule(has="Rail"))]:
        design.selectionSets.add([b for b in root.bRepBodies if rule(b.name)], nm)

    out.append("gap = %.4f, tv_w = %.4f, box_w = %.4f, bay_w = %.4f, tv_door %.4f x %.4f, tall_door_w %.4f" % (V["gap"], V["tv_w"], V["box_w"], V["bay_w"], V["tv_door_w"], V["tv_door_h"], V["tall_door_w"]))
    print("\n".join(out))

if __name__ == "__main__":
    run(None)
