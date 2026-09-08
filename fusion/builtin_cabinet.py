# Built-in wall cabinet: tall cabinet (left) + TV run (right), "Option 2-lite" construction.
# Run inside Fusion (via MCP execute). Fully parametric via user parameters;
# every panel position and size is a sketch dimension / offset expression.
# World frame: X along rear wall from left wall, rear wall at Y=0 with the room at -Y
# (so Fusion's front view shows the door side, tall cabinet on the left), Z up. Inches.
# Layout expressions below use y measured from the rear wall into the room; panel() mirrors.
#
# Construction (see guides/08-cost-reduction-options.md, "Opt 2-lite"):
#   Tall cabinet: frameless 5/8 spruce ply box (left side, top, bottom, 3 shelves), right
#     exposed side 5/8 MDF, 1/8 hardboard back nailed over the rear edges, two 2x4 rails,
#     one 5/8 MDF door hinged at the wall side.
#   TV run: no boxes and no back panel (the wall is the back). A 2x2 ladder: bottom-front and
#     bottom-rear stringers full length, 2x2 cross blocks under every divider and at both
#     ends, the three 2x4 rails end to end as the top-rear member, and six short 2x2
#     top-front stringers between dividers. Three 1/2 spruce bottoms on the stringers,
#     six 1/2 spruce dividers notched rear-top for the rail, 1/2 MDF top slab in two pieces
#     with the joint over a divider, six 5/8 MDF doors. Every TV door hinges on the divider
#     to its left (door 1 on the tall cabinet side) and opens to the right: door 1 full
#     overlay, doors 2-6 half overlay covering 9 mm of the divider. Divider positions are
#     therefore derived from the doors, not an equal pitch.
#   Kicks: 5/8 MDF on 2x2 sleeper blocks (sleepers not modelled). No adjustable legs.

import adsk.core
import adsk.fusion


def run(context):
    """Entry point: Fusion MCP execute and the Scripts panel both call run(context)."""
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    design.fusionUnitsManager.distanceDisplayUnits = (
        adsk.fusion.DistanceUnits.InchDistanceUnits
    )
    root = design.rootComponent
    out = []
    if root.bRepBodies.count:
        raise RuntimeError(
            "document already has %d bodies; start from an empty design"
            % root.bRepBodies.count
        )

    # name, expression, unit, comment
    PARAMS = [
        ("wall_w", "199.375", "in", "rear wall width, left wall to right wall"),
        ("tall_w", "18.375", "in", "tall cabinet outside width (measured)"),
        ("tall_h", "82.6875", "in", "tall cabinet outside height"),
        (
            "tall_depth",
            "24.4375",
            "in",
            "tall cabinet depth incl. door face (measured)",
        ),
        ("tv_h", "15", "in", "TV run outside height incl. top slab"),
        ("tv_depth", "16", "in", "TV run depth incl. door face (confirmed)"),
        ("panel_h", "19.9375", "in", "wall panelling bottom edge above floor = TV top"),
        (
            "box_t",
            "0.625",
            "in",
            "tall carcass stock (5/8 spruce ply; right side 5/8 MDF)",
        ),
        ("tv_panel_t", "0.5", "in", "TV bottoms and dividers (1/2 spruce ply)"),
        ("door_t", "0.625", "in", "door stock (5/8 MDF)"),
        ("slab_t", "0.5", "in", "TV top slab (1/2 MDF)"),
        ("top_overhang", "0", "in", "TV top slab overhang past the door faces"),
        (
            "back_t",
            "0.125",
            "in",
            "tall cabinet back (1/8 hardboard); TV run has no back",
        ),
        ("stringer", "1.5", "in", "2x2 ladder stock, actual 1-1/2 square"),
        (
            "reveal",
            "0.125",
            "in",
            "gap between neighbouring doors, and door to top slab",
        ),
        (
            "end_gap",
            "0.25",
            "in",
            "door edge clearance to a wall or to the tall cabinet side",
        ),
        (
            "overlay_half",
            "0.354331",
            "in",
            "half-overlay hinge: door covers 9 mm of the divider edge",
        ),
        ("rail_h", "3.5", "in", "hanging rail width (2x4 stock is 3-1/2 wide)"),
        ("rail_t", "1.5", "in", "hanging rail thickness (1-1/2 solid 2x4 on hand)"),
        ("kick_setback", "2.5", "in", "TV kick plate recess behind door faces"),
        (
            "tall_kick_setback",
            "0",
            "in",
            "tall cabinet kick plate recess (0 = flush with door)",
        ),
        (
            "tall_shelves",
            "3",
            "",
            "shelf count in tall cabinet (rebuild script to change)",
        ),
        ("tv_doors", "6", "", "TV door / bay count (rebuild script to change)"),
        ("gap", "panel_h - tv_h", "in", "floor to cabinet underside (kick height)"),
        ("tv_w", "wall_w - tall_w", "in", "TV run outside width"),
        (
            "tv_cd",
            "tv_depth - door_t",
            "in",
            "TV run carcass depth: wall to back of doors",
        ),
        (
            "tv_door_w",
            "(tv_w - 2 * end_gap - (tv_doors - 1) * reveal) / tv_doors",
            "in",
            "TV door width",
        ),
        (
            "tv_door_h",
            "tv_h - slab_t - reveal",
            "in",
            "TV door height (flush with front stringer underside, reveal under slab)",
        ),
        (
            "div_h",
            "tv_h - slab_t - tv_panel_t - stringer",
            "in",
            "TV divider height (sits on the bottom panel, under the slab)",
        ),
        (
            "tall_door_w",
            "tall_w - end_gap",
            "in",
            "tall door width (end_gap at the wall, flush at the exposed side)",
        ),
        ("rail_len", "tv_w / 3", "in", "TV rail length, three rails end to end"),
    ]
    # divider k (1..5) left face: door k+1 hinges on it and covers overlay_half of its edge,
    # so the divider's right face = door(k+1) left edge + overlay_half.
    for k in range(1, 6):
        PARAMS.append(
            (
                "div%d_x" % k,
                "tall_w + end_gap + %d * (tv_door_w + reveal) + overlay_half - tv_panel_t"
                % k,
                "in",
                "TV divider %d left face X (derived from door %d hinge overlay)"
                % (k, k + 1),
            )
        )

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
        base = {
            "x": comp.yZConstructionPlane,
            "y": comp.xZConstructionPlane,
            "z": comp.xYConstructionPlane,
        }[thin]
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

        corners = [sk.modelToSketchSpace(wpt(s)) for s in ((0, 0, 0), (1, 1, 1))]
        xs = [p.x for p in corners]
        ys = [p.y for p in corners]
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
            return min(
                pts.values(),
                key=lambda sp: (sp.geometry.x - x) ** 2 + (sp.geometry.y - y) ** 2,
            )

        A = find(p1.x, p1.y)
        B = find(p2.x, p1.y)
        D = find(p1.x, p2.y)
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
                    d = dims.addDistanceDimension(
                        sk.originPoint, A, H, tp(p1.x / 2, p1.y - 4)
                    )
                else:
                    d = dims.addDistanceDimension(
                        sk.originPoint, A, Vo, tp(p1.x - 4, p1.y / 2)
                    )
                d.parameter.expression = pos_expr
        prof = sk.profiles.item(0)
        ni, nsgn = dominant(plane.geometry.normal)
        dist = size[thin] if nsgn > 0 else "-(%s)" % size[thin]
        ext = comp.features.extrudeFeatures
        ein = ext.createInput(
            prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        ein.setDistanceExtent(False, adsk.core.ValueInput.createByString(dist))
        f = ext.add(ein)
        f.name = name
        body = f.bodies.item(0)
        body.name = name
        # verify
        bb = body.boundingBox
        got = [
            bb.minPoint.x / IN,
            bb.minPoint.y / IN,
            bb.minPoint.z / IN,
            bb.maxPoint.x / IN,
            bb.maxPoint.y / IN,
            bb.maxPoint.z / IN,
        ]
        exp = lo_v + hi_v
        err = max(abs(g - e) for g, e in zip(got, exp))
        out.append(
            "%-26s %s size %.3f x %.3f x %.3f%s"
            % (
                name,
                "OK " if err < 1e-3 else "BAD",
                hi_v[0] - lo_v[0],
                hi_v[1] - lo_v[1],
                hi_v[2] - lo_v[2],
                "" if err < 1e-3 else "  got %s exp %s" % (got, exp),
            )
        )
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

    def notch(target, tool_bodies, name):
        """Cut the `tool_bodies` out of `target`, keeping the tools."""
        tools = adsk.core.ObjectCollection.create()
        for t in tool_bodies:
            tools.add(t)
        cin = root.features.combineFeatures.createInput(target, tools)
        cin.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
        cin.isKeepToolBodies = True
        cin.isNewComponent = False
        f = root.features.combineFeatures.add(cin)
        f.name = name
        out.append(
            "%-26s NOTCH cut by %s" % (name, ", ".join(t.name for t in tool_bodies))
        )

    def xrange_of(body):
        bb = body.boundingBox
        return bb.minPoint.x / IN, bb.maxPoint.x / IN

    # ---------------- Tall cabinet: frameless 5/8 box ----------------
    tc = new_comp("TallCabinet")
    cd = "tall_depth - back_t - door_t"  # carcass panel depth
    panel(
        tc,
        "LeftSide",
        "x",
        {"x": "0", "y": "back_t", "z": "gap"},
        {"x": "box_t", "y": cd, "z": "tall_h"},
    )
    panel(
        tc,
        "RightSideMDF",
        "x",
        {"x": "tall_w - box_t", "y": "back_t", "z": "gap"},
        {"x": "box_t", "y": cd, "z": "tall_h"},
    )
    panel(
        tc,
        "Bottom",
        "z",
        {"x": "box_t", "y": "back_t", "z": "gap"},
        {"x": "tall_w - 2*box_t", "y": cd, "z": "box_t"},
    )
    panel(
        tc,
        "Top",
        "z",
        {"x": "box_t", "y": "back_t", "z": "gap + tall_h - box_t"},
        {"x": "tall_w - 2*box_t", "y": cd, "z": "box_t"},
    )
    panel(
        tc,
        "Back",
        "y",
        {"x": "0", "y": "0", "z": "gap"},
        {"x": "tall_w", "y": "back_t", "z": "tall_h"},
    )
    panel(
        tc,
        "RailTop",
        "y",
        {"x": "box_t", "y": "back_t", "z": "gap + tall_h - box_t - rail_h"},
        {"x": "tall_w - 2*box_t", "y": "rail_t", "z": "rail_h"},
    )
    panel(
        tc,
        "RailBottom",
        "y",
        {"x": "box_t", "y": "back_t", "z": "gap + box_t"},
        {"x": "tall_w - 2*box_t", "y": "rail_t", "z": "rail_h"},
    )
    n = int(V["tall_shelves"])
    for i in range(1, n + 1):
        panel(
            tc,
            "Shelf%d" % i,
            "z",
            {
                "x": "box_t",
                "y": "back_t",
                "z": "gap + %d*tall_h/(tall_shelves+1) - box_t/2" % i,
            },
            {
                "x": "tall_w - 2*box_t",
                "y": "tall_depth - back_t - door_t - box_t",
                "z": "box_t",
            },
        )
    # end_gap at the left wall; right door edge flush with the exposed right side; 5 hinges on the wall side
    panel(
        tc,
        "Door",
        "y",
        {"x": "end_gap", "y": "tall_depth - door_t", "z": "gap"},
        {"x": "tall_door_w", "y": "door_t", "z": "tall_h"},
    )

    # ---------------- TV run: 2x2 ladder, wall as back ----------------
    tv = new_comp("TVRun")
    nd = int(V["tv_doors"])
    div_lo = ["div%d_x" % k for k in range(1, nd)]  # left faces of dividers 1..5
    bay_lo = ["tall_w"] + [
        "%s + tv_panel_t" % d for d in div_lo
    ]  # clear-bay left edges
    bay_hi = div_lo + ["wall_w"]  # clear-bay right edges
    # bottom stringers, full length (cut as 3 pieces in the shop, joints under dividers 2 and 4)
    panel(
        tv,
        "StringerBottomRear",
        "y",
        {"x": "tall_w", "y": "0", "z": "gap"},
        {"x": "tv_w", "y": "stringer", "z": "stringer"},
    )
    panel(
        tv,
        "StringerBottomFront",
        "y",
        {"x": "tall_w", "y": "tv_cd - stringer", "z": "gap"},
        {"x": "tv_w", "y": "stringer", "z": "stringer"},
    )
    # cross blocks between the stringers: both ends and centred under each divider
    blocks = (
        ["tall_w"]
        + ["%s + tv_panel_t/2 - stringer/2" % d for d in div_lo]
        + ["wall_w - stringer"]
    )
    for i, bx in enumerate(blocks):
        panel(
            tv,
            "CrossBlock%d" % (i + 1),
            "x",
            {"x": bx, "y": "stringer", "z": "gap"},
            {"x": "stringer", "y": "tv_cd - 2*stringer", "z": "stringer"},
        )
    # three bottoms on the stringers, joints under dividers 2 and 4
    joints = ["tall_w", "div2_x + tv_panel_t/2", "div4_x + tv_panel_t/2", "wall_w"]
    for i in range(3):
        panel(
            tv,
            "Bottom%d" % (i + 1),
            "z",
            {"x": joints[i], "y": "0", "z": "gap + stringer"},
            {
                "x": "(%s) - (%s)" % (joints[i + 1], joints[i]),
                "y": "tv_cd",
                "z": "tv_panel_t",
            },
        )
    # top-rear member: three 2x4 rails end to end, screwed to the studs
    rails = []
    for j in range(3):
        rails.append(
            panel(
                tv,
                "Rail%d" % (j + 1),
                "y",
                {
                    "x": "tall_w + %d*rail_len" % j,
                    "y": "0",
                    "z": "gap + tv_h - slab_t - rail_h",
                },
                {"x": "rail_len", "y": "rail_t", "z": "rail_h"},
            )
        )
    # dividers on the bottom panel, notched rear-top for the rail (rail body is the cutting tool)
    for k, dx in enumerate(div_lo):
        dv = panel(
            tv,
            "Divider%d" % (k + 1),
            "x",
            {"x": dx, "y": "0", "z": "gap + stringer + tv_panel_t"},
            {"x": "tv_panel_t", "y": "tv_cd", "z": "div_h"},
        )
        dlo, dhi = xrange_of(dv)
        tools = [
            r
            for r in rails
            if xrange_of(r)[1] > dlo + 1e-6 and xrange_of(r)[0] < dhi - 1e-6
        ]
        notch(dv, tools, tv.name + "_Divider%dNotch" % (k + 1))
    # top-front stringers: six separate pieces between dividers, no notch at the front
    for i in range(nd):
        panel(
            tv,
            "StringerTopFront%d" % (i + 1),
            "y",
            {
                "x": bay_lo[i],
                "y": "tv_cd - stringer",
                "z": "gap + tv_h - slab_t - stringer",
            },
            {
                "x": "(%s) - (%s)" % (bay_hi[i], bay_lo[i]),
                "y": "stringer",
                "z": "stringer",
            },
        )
    # doors: door 1 hinges on the tall cabinet side (half-overlay hinge on a 5/8 packer, or inset-crank), doors 2-6 on the divider to their left (half overlay)
    for d in range(nd):
        panel(
            tv,
            "Door%d" % (d + 1),
            "y",
            {
                "x": "tall_w + end_gap + %d*(tv_door_w + reveal)" % d,
                "y": "tv_depth - door_t",
                "z": "gap",
            },
            {"x": "tv_door_w", "y": "door_t", "z": "tv_door_h"},
        )
    # top slab in two pieces, joint over the middle of divider 3
    slab_joint = "div3_x + tv_panel_t/2"
    panel(
        tv,
        "TopSlab1",
        "z",
        {"x": "tall_w", "y": "0", "z": "gap + tv_h - slab_t"},
        {
            "x": "(%s) - tall_w" % slab_joint,
            "y": "tv_depth + top_overhang",
            "z": "slab_t",
        },
    )
    panel(
        tv,
        "TopSlab2",
        "z",
        {"x": slab_joint, "y": "0", "z": "gap + tv_h - slab_t"},
        {
            "x": "wall_w - (%s)" % slab_joint,
            "y": "tv_depth + top_overhang",
            "z": "slab_t",
        },
    )

    # ---------------- Kick plates (5/8 MDF), recessed, stepped at the tall cabinet ----------------
    kk = new_comp("Kick")
    panel(
        kk,
        "Tall",
        "y",
        {"x": "0", "y": "tall_depth - tall_kick_setback - door_t", "z": "0"},
        {"x": "tall_w", "y": "door_t", "z": "gap"},
    )
    panel(
        kk,
        "Return",
        "x",
        {"x": "tall_w - door_t", "y": "tv_depth - kick_setback - door_t", "z": "0"},
        {
            "x": "door_t",
            "y": "tall_depth - tall_kick_setback - door_t - (tv_depth - kick_setback - door_t)",
            "z": "gap",
        },
    )
    panel(
        kk,
        "TV",
        "y",
        {"x": "tall_w", "y": "tv_depth - kick_setback - door_t", "z": "0"},
        {"x": "tv_w", "y": "door_t", "z": "gap"},
    )

    # selection sets (click one in the browser, press V to hide/show)
    for s_ in list(design.selectionSets):
        s_.deleteMe()

    def _rule(prefix=None, has=None):
        return lambda nm: (
            (not prefix or nm.startswith(prefix)) and (not has or has in nm)
        )

    for nm, rule in [
        ("Tall cabinet", _rule(prefix="TallCabinet_")),
        ("TV run", _rule(prefix="TVRun_")),
        ("Doors", _rule(has="Door")),
        ("TV top slab", _rule(prefix="TVRun_TopSlab")),
        ("Ladder (2x2)", lambda nm: "Stringer" in nm or "CrossBlock" in nm),
        ("Kick", _rule(prefix="Kick_")),
        ("Rails (2x4)", _rule(has="Rail")),
    ]:
        design.selectionSets.add([b for b in root.bRepBodies if rule(b.name)], nm)

    out.append(
        "gap = %.4f, tv_w = %.4f, tv_door %.4f x %.4f, div_h %.4f, tall_door_w %.4f, rail_len %.4f"
        % (
            V["gap"],
            V["tv_w"],
            V["tv_door_w"],
            V["tv_door_h"],
            V["div_h"],
            V["tall_door_w"],
            V["rail_len"],
        )
    )
    out.append(
        "divider left faces X (from left wall): "
        + ", ".join("%d: %.4f" % (k, V["div%d_x" % k]) for k in range(1, nd))
    )
    out.append("bodies: %d" % root.bRepBodies.count)
    print("\n".join(out))


if __name__ == "__main__":
    run(None)
