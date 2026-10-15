"""Parametric model of four laminated pine bookshelves either side of a fireplace.

Inputs: settings in config.py; --view opens the OCP CAD Viewer.
Outputs: build/bookshelf.step, bookshelf.stl, front.svg, materials.md, sheets/*.svg and
instructions.md.
Implements spec 3 (Furniture design), 6.4 (Model), 6.5 (Outputs) and 7 (Quality).
"""

import math
import sys
from itertools import combinations, pairwise
from pathlib import Path

from build123d import (
    CM,
    Align,
    Box,
    Color,
    Compound,
    ExportSVG,
    LineType,
    Pos,
    Solid,
    export_step,
    export_stl,
)

import config
import instructions
import materials
from materials import Hardware, Part

# --- Derived sizes ---

eps = 1e-6  # rounds float halves like 107.85 up
t = config.pine_thickness
s = config.thin_pine_thickness
door_bottom = config.kickboard_height + config.door_gap / 2
door_top = config.cabinet_height - config.door_gap / 2
door_height = door_top - door_bottom
cabinet_top_bottom = config.cabinet_height - t
cabinet_line_bottom = config.cabinet_height - s  # narrow shelf level with cabinet top
top_bottom = config.height - t
upper_clear = (
    top_bottom - config.cabinet_height - config.shelves_above_cabinet * s
) / (config.shelves_above_cabinet + 1)
upper_shelves = [
    config.cabinet_height + (i + 1) * upper_clear + i * s
    for i in range(config.shelves_above_cabinet)
]
bottom_top = config.kickboard_height + t
lower_clear = (cabinet_line_bottom - bottom_top - config.narrow_lower_shelves * s) / (
    config.narrow_lower_shelves + 1
)
lower_shelves = [
    bottom_top + (i + 1) * lower_clear + i * s
    for i in range(config.narrow_lower_shelves)
]
widths = {"wide": config.wide_width, "narrow": config.narrow_width}
pine = f"{materials.size(t * 10)}mm laminated pine"
thin_pine = f"{materials.size(s * 10)}mm laminated pine"
birch = f"{materials.size(config.back_thickness * 10)}mm birch plywood"
usable_length = config.sheet_length - 2 * config.edge_trim
usable_width = config.sheet_width - 2 * config.edge_trim


# --- Unit ---


def unit(width: float, cabinet: bool) -> list[Box]:
    """One unit's labeled panels, origin at the floor, front-left of the carcass."""
    inner = width - 2 * t

    def panel(
        label: str, x: float, y: float, z: float, sx: float, sy: float, sz: float
    ) -> Box:
        solid = Pos(x * CM, y * CM, z * CM) * Box(
            sx * CM, sy * CM, sz * CM, align=Align.MIN
        )
        solid.label = label
        solid.color = Color(
            config.birch_color if label == "back" else config.pine_color
        )
        return solid

    horizontal = (
        [("bottom", config.kickboard_height), ("cabinet_top", cabinet_top_bottom)]
        if cabinet
        else [("bottom", config.kickboard_height)]
    )
    shelves = (
        upper_shelves
        if cabinet
        else [*lower_shelves, cabinet_line_bottom, *upper_shelves]
    )
    parts = [
        panel("side_1", 0, 0, 0, t, config.depth, config.height),
        panel("side_2", width - t, 0, 0, t, config.depth, config.height),
        *(panel(n, t, 0, z, inner, config.depth, t) for n, z in horizontal),
        *(
            panel(f"shelf_{i}", t, 0, z, inner, config.depth, s)
            for i, z in enumerate(shelves, 1)
        ),
        panel("top", t, 0, top_bottom, inner, config.depth, t),
        panel(
            "kickboard",
            t,
            config.kickboard_setback,
            0,
            inner,
            s,
            config.kickboard_height,
        ),
        panel("back", 0, config.depth, 0, width, config.back_thickness, config.height),
    ]
    if cabinet:
        door_width = (width - config.door_gap) / 2
        parts += [
            *(
                panel(
                    "cabinet_shelf",
                    t,
                    config.depth - config.cabinet_shelf_depth,
                    z,
                    inner,
                    config.cabinet_shelf_depth,
                    s,
                )
                for z in lower_shelves
            ),
            panel("door_1", 0, -s, door_bottom, door_width, s, door_height),
            panel(
                "door_2",
                width - door_width,
                -s,
                door_bottom,
                door_width,
                s,
                door_height,
            ),
        ]
    return parts


# --- Layout ---

units: list[Compound] = []
parts: list[Part] = []
x = 0.0
counts = {"wide": 0, "narrow": 0}
for kind in config.layout:
    if kind == "fireplace":
        x += config.fireplace_width
        continue
    counts[kind] += 1
    name = f"{kind}_{counts[kind]}"
    solids = []
    for solid in unit(widths[kind], kind == "wide"):
        label = solid.label
        moved = Pos(x * CM, 0, 0) * solid
        moved.label = label
        solids.append(moved)
        box = moved.bounding_box()
        along = 2 if label.startswith(("side", "door", "back")) else 0  # grain axis
        length = round(tuple(box.size)[along] / CM + eps, 1)
        thickness, width = sorted(
            round(v / CM + eps, 1) for i, v in enumerate(tuple(box.size)) if i != along
        )
        parts.append(
            Part(
                label=f"{name} / {label}",
                unit=name,
                name=label.rstrip("_0123456789"),
                unit_type=kind,
                length=length,
                width=width,
                thickness=thickness,
                material=birch
                if label == "back"
                else pine
                if abs(thickness - t) < eps
                else thin_pine,
                bottom=round(box.min.Z / CM + eps, 1),
                top=round(box.max.Z / CM + eps, 1),
            )
        )
    units.append(Compound(children=solids, label=name))
    x += widths[kind]
assembly = Compound(children=units, label="bookshelf")
solids_by_label = {
    f"{u.label} / {s.label}": s
    for u in units
    for s in u.children
    if isinstance(s, Solid)
}
joints = sum(a != "fireplace" and b != "fireplace" for a, b in pairwise(config.layout))

# --- Checks ---

errors = []
expected = (
    sum(widths[k] for k in config.layout if k != "fireplace") + config.fireplace_width,
    config.depth + config.back_thickness + s,
    config.height,
)
actual = assembly.bounding_box().size / CM
for axis, a, e in zip(("width", "depth", "height"), actual, expected, strict=True):
    if abs(a - e) > 0.01:
        errors.append(f"bounding box {axis} {a:.1f}, expected {e:.1f}")
for (label_a, a), (label_b, b) in combinations(solids_by_label.items(), 2):
    box_a, box_b = a.bounding_box(), b.bounding_box()
    overlap = [
        min(box_a.max.X, box_b.max.X) - max(box_a.min.X, box_b.min.X),
        min(box_a.max.Y, box_b.max.Y) - max(box_a.min.Y, box_b.min.Y),
        min(box_a.max.Z, box_b.max.Z) - max(box_a.min.Z, box_b.min.Z),
    ]
    if min(overlap) > 0.01:
        errors.append(
            f"{label_a} and {label_b} overlap by "
            + " × ".join(f"{v / CM:.1f}" for v in overlap)
            + "cm, expected no overlap"
        )
for p in parts:
    if p.length > usable_length or p.width > usable_width:
        errors.append(
            f"{p.label} is {p.length} × {p.width}, expected to fit the usable sheet "
            f"{usable_length} × {usable_width} along the grain"
        )
if errors:
    sys.exit("Model checks failed:\n  " + "\n  ".join(errors))

# --- Exports ---

build = Path(__file__).parent.parent / "build"
build.mkdir(exist_ok=True)

export_step(assembly, build / "bookshelf.step")
export_stl(assembly, build / "bookshelf.stl")

center = assembly.bounding_box().center()
visible, hidden = assembly.project_to_viewport(
    (center.X, -10 * config.height * CM, center.Z),
    viewport_up=(0, 0, 1),
    look_at=(center.X, 0, center.Z),
)
svg = ExportSVG(scale=0.25)
svg.add_layer("visible")
svg.add_layer("hidden", line_color=(150, 150, 150), line_type=LineType.ISO_DASH)
svg.add_shape(visible, layer="visible")
svg.add_shape(hidden, layer="hidden")
svg.write(build / "front.svg")

doors = [p for p in parts if p.name == "door"]
backs = [p for p in parts if p.name == "back"]
horizontals = [p for p in parts if p.name not in ("side", "door", "back")]
pockets = {
    p.label: 2 * max(2, math.ceil(p.width / config.pocket_spacing)) for p in horizontals
}
thin_labels = {p.label for p in horizontals if p.material == thin_pine}
staple_length = sum(
    2 * (b.length + b.width)
    + b.width
    * sum(
        p.unit == b.unit and p.name in ("shelf", "cabinet_top", "cabinet_shelf")
        for p in horizontals
    )
    for b in backs
)
pine_area = sum(p.length * p.width for p in parts if p.material != birch) * 2 / 10_000
finish_litres = round(pine_area * config.finish_coats / config.finish_coverage, 1)
unit_count = sum(counts.values())


hardware = [
    Hardware(
        "Hinges",
        f"Hafele 110° soft-close full overlay, rated 14–22mm for {thin_pine[:4]} doors",
        2 * len(doors),
        *config.hinge_pack,
        config.hinge_url,
    ),
    Hardware("Knobs", "one per door", len(doors), *config.knob_pack),
    Hardware(
        "Wood screws",
        f"4 × 40mm countersunk, coarse thread, one per pocket in {pine[:4]} panels",
        sum(n for label, n in pockets.items() if label not in thin_labels),
        *config.screw_pack,
    ),
    Hardware(
        "Short wood screws",
        f"4 × 30mm countersunk, one per pocket in {thin_pine[:4]} panels",
        sum(n for label, n in pockets.items() if label in thin_labels),
        *config.short_screw_pack,
    ),
    Hardware(
        "Washers",
        "M4 flat, under each pocket screw head",
        sum(pockets.values()),
        *config.washer_pack,
    ),
    Hardware(
        "Pocket plugs",
        "for open shelf pockets in view",
        sum(
            n
            for label, n in pockets.items()
            if label.split(" / ")[1].startswith("shelf")
        ),
        *config.plug_pack,
        config.plug_url,
    ),
    Hardware(
        "Pocket hole jig",
        f"Gunpla twin kit, set for {pine[:4]} and {thin_pine[:4]}",
        1,
        *config.pocket_jig_pack,
        config.pocket_jig_url,
    ),
    Hardware(
        "Staples",
        "narrow crown, 16–19mm legs",
        math.ceil(staple_length / config.staple_spacing),
        *config.staple_pack,
    ),
    Hardware("Wood glue", "1L", 1, *config.glue_pack),
    Hardware(
        "Connector bolts",
        f"{config.bolts_per_joint} per joint between units in a set",
        joints * config.bolts_per_joint,
        *config.bolt_pack,
    ),
    Hardware("Anti-tip brackets", "one per unit", unit_count, *config.bracket_pack),
    Hardware(
        "Plasterboard toggles",
        "spring or snap, for fixings that miss a stud",
        unit_count * config.toggles_per_bracket,
        *config.toggle_pack,
    ),
    Hardware(
        "Varnish (litres)",
        f"Ronseal Antique Pine satin, {config.finish_coats} coat, both faces",
        finish_litres,
        *config.finish_pack,
        config.finish_url,
    ),
    Hardware(
        "Roller kit",
        "Axus Blonde natural wool mini, 101mm",
        1,
        *config.roller_pack,
        config.roller_url,
    ),
    Hardware(
        "Roller sleeves",
        f"refills beyond the kit's {config.kit_sleeves}",
        max(
            0,
            math.ceil(pine_area * config.finish_coats / config.roller_coverage)
            - config.kit_sleeves,
        ),
        *config.sleeve_pack,
        config.sleeve_url,
    ),
    Hardware(
        "Brush",
        "Screwfix 173FM synthetic, 3 inch",
        1,
        *config.brush_pack,
        config.brush_url,
    ),
    Hardware(
        "Sanding sponges",
        "Bosch Expert 421VV, superfine/fine/medium",
        math.ceil(pine_area / config.sanding_coverage),
        *config.sanding_pack,
        config.sanding_url,
    ),
]

sheet_counts, cutting_list = materials.write_materials(
    parts,
    hardware,
    build / "materials.md",
    build / "sheets",
    config.sheet_length,
    config.sheet_width,
    config.edge_trim,
    config.kerf,
    {
        pine: config.pine_sheet_price,
        thin_pine: config.thin_pine_sheet_price,
        birch: config.birch_sheet_price,
    },
    config.cut_price,
    config.delivery_price,
)

shared = [p for p in parts if p.unit == "narrow_1" and p.name not in ("side", "back")]
compartments = sorted(
    (a.top + b.bottom) / 2
    for a, b in pairwise(sorted(shared, key=lambda p: p.bottom))
    if b.bottom > a.top
)
step = (len(compartments) - 1) / max(1, config.bolts_per_joint - 1)
bolt_heights = [
    round(compartments[round(i * step)], 1) for i in range(config.bolts_per_joint)
]
instructions.write_instructions(
    build / "instructions.md",
    parts,
    hardware,
    widths,
    config.height,
    config.depth,
    config.kickboard_setback,
    config.pocket_spacing,
    config.staple_spacing,
    config.door_gap,
    config.hinge_from_door_end,
    config.knob_from_door_edge,
    config.knob_from_door_top,
    config.kerf,
    cutting_list,
    bolt_heights,
    config.layout,
)

for path in sorted(build.rglob("*")):
    if path.is_file():
        print(path.relative_to(build.parent))
print("Sheets: " + ", ".join(f"{n} × {m}" for m, n in sheet_counts.items()))

if "--view" in sys.argv:
    from ocp_vscode import show

    show(
        [
            s
            for u in units
            for s in u.children
            if not (config.hide_doors and s.label.startswith("door"))
        ]
    )
