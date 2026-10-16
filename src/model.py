"""Parametric model of two laminated pine bookshelves either side of a fireplace.

Inputs: settings in config.py; --view opens the OCP CAD Viewer.
Outputs: build/bookshelf.step, bookshelf.stl, front.svg, materials.md, sheets/*.svg and
instructions.md.
Implements spec 3 (Furniture design), 6.4 (Model), 6.5 (Outputs) and 7 (Quality).
"""

import math
import sys
from itertools import combinations
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
shelf_depth = config.depth - config.back_thickness
cabinet_line_bottom = config.cabinet_height - s
top_bottom = config.height - t
upper_clear = (
    top_bottom - config.cabinet_height - config.shelves_above_cabinet * s
) / (config.shelves_above_cabinet + 1)
upper_shelves = [
    config.cabinet_height + (i + 1) * upper_clear + i * s
    for i in range(config.shelves_above_cabinet)
]
bottom_top = config.kickboard_height + s
lower_clear = (cabinet_line_bottom - bottom_top - config.narrow_lower_shelves * s) / (
    config.narrow_lower_shelves + 1
)
lower_shelves = [
    bottom_top + (i + 1) * lower_clear + i * s
    for i in range(config.narrow_lower_shelves)
]
door_bottom = bottom_top + config.door_gap
door_height = cabinet_line_bottom - config.door_gap - door_bottom
unit_bays = [group.split() for group in " ".join(config.layout).split("fireplace")]
first_bays = unit_bays[0]
inner_width = config.unit_width - 2 * t
widths = {
    "narrow": config.narrow_width,
    "wide": (
        inner_width
        - (len(first_bays) - 1) * t
        - first_bays.count("narrow") * config.narrow_width
    )
    / first_bays.count("wide"),
}
bay_centres = []  # across the back, from its edge on the first bay's side
edge = 0.0
for bay in first_bays:
    bay_centres.append(edge + widths[bay] / 2)
    edge += widths[bay] + t
groove_offset = (bay_centres[0] + config.groove_spacing / 2) % config.groove_spacing
pine = f"{materials.size(t * 10)}mm laminated pine"
thin_pine = f"{materials.size(s * 10)}mm laminated pine"
back_material = f"{materials.size(config.back_thickness * 10)}mm V-groove MDF"
sheets = {
    pine: (
        config.frame_sheet_length,
        config.frame_sheet_width,
        config.pine_sheet_price,
    ),
    thin_pine: (config.sheet_length, config.sheet_width, config.thin_pine_sheet_price),
    back_material: (config.sheet_length, config.sheet_width, config.back_sheet_price),
}


# --- Unit ---


def unit(bays: list[str]) -> list[Box]:
    """One unit's labeled panels, origin at the floor, front-left of the carcass."""

    def panel(
        label: str, x: float, y: float, z: float, sx: float, sy: float, sz: float
    ) -> Box:
        solid = Pos(x * CM, y * CM, z * CM) * Box(
            sx * CM, sy * CM, sz * CM, align=Align.MIN
        )
        solid.label = label
        solid.color = Color(config.back_color if label == "back" else config.pine_color)
        return solid

    parts = [
        panel("side_1", 0, 0, 0, t, config.depth, config.height),
        panel("side_2", config.unit_width - t, 0, 0, t, config.depth, config.height),
        panel("top", t, 0, top_bottom, inner_width, config.depth, t),
        panel(
            "back", t, shelf_depth, 0, inner_width, config.back_thickness, top_bottom
        ),
    ]
    x = t
    for i, bay in enumerate(bays):
        if i:
            parts.append(panel(f"divider_{i}", x, 0, 0, t, shelf_depth, top_bottom))
            x += t
        width = widths[bay]
        cabinet = bay == "wide"
        horizontal = (
            [("bottom", config.kickboard_height), ("cabinet_top", cabinet_line_bottom)]
            if cabinet
            else [("bottom", config.kickboard_height)]
        )
        shelves = (
            upper_shelves
            if cabinet
            else [*lower_shelves, cabinet_line_bottom, *upper_shelves]
        )
        parts += [
            *(
                panel(f"{bay} {n}", x, 0, z, width, shelf_depth, s)
                for n, z in horizontal
            ),
            *(
                panel(f"{bay} shelf_{j}", x, 0, z, width, shelf_depth, s)
                for j, z in enumerate(shelves, 1)
            ),
            panel(
                f"{bay} kickboard",
                x,
                config.kickboard_setback,
                0,
                width,
                s,
                config.kickboard_height,
            ),
        ]
        if cabinet:
            door_width = (width - 3 * config.door_gap) / 2
            parts += [
                *(
                    panel(
                        f"{bay} cabinet_shelf",
                        x,
                        shelf_depth - config.cabinet_shelf_depth,
                        z,
                        width,
                        config.cabinet_shelf_depth,
                        s,
                    )
                    for z in lower_shelves
                ),
                panel(
                    f"{bay} door_1",
                    x + config.door_gap,
                    0,
                    door_bottom,
                    door_width,
                    s,
                    door_height,
                ),
                panel(
                    f"{bay} door_2",
                    x + width - config.door_gap - door_width,
                    0,
                    door_bottom,
                    door_width,
                    s,
                    door_height,
                ),
            ]
        x += width
    return parts


# --- Layout ---

units: list[Compound] = []
parts: list[Part] = []
for n, bays in enumerate(unit_bays, 1):
    name = f"unit_{n}"
    x = (n - 1) * (config.unit_width + config.fireplace_width)
    solids = []
    for solid in unit(bays):
        label = solid.label
        moved = Pos(x * CM, 0, 0) * solid
        moved.label = label
        solids.append(moved)
        bay, _, piece = label.rpartition(" ")
        part_name = piece.rstrip("_0123456789")
        box = moved.bounding_box()
        along = 2 if part_name in ("side", "divider", "door", "back") else 0  # grain
        length = round(tuple(box.size)[along] / CM + eps, 1)
        thickness, width = sorted(
            round(v / CM + eps, 1) for i, v in enumerate(tuple(box.size)) if i != along
        )
        parts.append(
            Part(
                label=f"{name} / {label}",
                unit=name,
                name=part_name,
                unit_type=bay or "frame",
                length=length,
                width=width,
                thickness=thickness,
                material=back_material
                if part_name == "back"
                else pine
                if abs(thickness - t) < eps
                else thin_pine,
                bottom=round(box.min.Z / CM + eps, 1),
                top=round(box.max.Z / CM + eps, 1),
            )
        )
    units.append(Compound(children=solids, label=name))
assembly = Compound(children=units, label="bookshelf")
solids_by_label = {
    f"{u.label} / {s.label}": s
    for u in units
    for s in u.children
    if isinstance(s, Solid)
}

# --- Checks ---

errors = []
expected = (
    len(units) * config.unit_width
    + config.layout.count("fireplace") * config.fireplace_width,
    config.depth,
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
for u in units:
    unit_width = u.bounding_box().size.X / CM
    if abs(unit_width - config.unit_width) > 0.01:
        errors.append(f"{u.label} width {unit_width:.1f}, expected {config.unit_width}")
for p in parts:
    sheet_length, sheet_width, _ = sheets[p.material]
    usable_length = sheet_length - 2 * config.edge_trim
    usable_width = sheet_width - 2 * config.edge_trim
    if p.length > usable_length or p.width > usable_width:
        errors.append(
            f"{p.label} is {p.length} × {p.width}, expected to fit the usable sheet "
            f"{usable_length} × {usable_width} along the grain"
        )
for bay, centre in zip(first_bays, bay_centres, strict=True):
    off = (centre - groove_offset) % (config.groove_spacing / 2)
    if min(off, config.groove_spacing / 2 - off) > 0.01:
        errors.append(
            f"{bay} bay's V-grooves are {off:.2f}cm off symmetric, expected 0; "
            "adjust unit_width"
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

frame_names = ("side", "divider", "door", "back")
doors = [p for p in parts if p.name == "door"]
horizontals = [p for p in parts if p.name not in frame_names]
braced = {
    p.label
    for p in horizontals
    if p.unit_type == "wide" and p.name in ("bottom", "cabinet_top", "cabinet_shelf")
}
pockets = {
    p.label: 2 * max(2, math.ceil(p.width / config.pocket_spacing))
    for p in horizontals
    if p.label not in braced
}
thin_labels = {p.label for p in horizontals if p.material == thin_pine}
dividers = sum(p.name == "divider" for p in parts)
back_screws = sum(
    math.ceil(p.length / config.back_screw_spacing) + 1
    for p in parts
    if p.name in ("divider", "bottom", "cabinet_top", "cabinet_shelf", "shelf")
)
back_area = (
    sum(p.length * p.width for p in parts if p.material == back_material) / 10_000
)
pine_area = (
    sum(p.length * p.width for p in parts if p.material != back_material) * 2 / 10_000
)
finish_litres = round(pine_area * config.finish_coats / config.finish_coverage, 1)


hardware = [
    Hardware(
        "Hinges",
        f"LOOTICH 110° soft-close inset, rated 16–19mm for {thin_pine[:4]} doors",
        2 * len(doors),
        *config.hinge_pack,
        config.hinge_url,
    ),
    Hardware("Knobs", "one per door", len(doors), *config.knob_pack),
    Hardware(
        "Wood screws",
        f"4 × 60mm countersunk, one per pocket in the {pine[:4]} top, plus "
        f"{config.top_screws_per_divider} down through the top into each divider",
        sum(n for label, n in pockets.items() if label not in thin_labels)
        + config.top_screws_per_divider * dividers,
        *config.screw_pack,
    ),
    Hardware(
        "Short wood screws",
        f"4 × 30mm countersunk, one per pocket in {thin_pine[:4]} panels",
        sum(n for label, n in pockets.items() if label in thin_labels),
        *config.short_screw_pack,
    ),
    Hardware(
        "Back screws",
        f"4 × 30mm countersunk, through the back every "
        f"{materials.size(config.back_screw_spacing)}cm, already owned",
        back_screws,
        *config.short_screw_pack,
    ),
    Hardware(
        "Corner braces",
        f"40mm, {config.braces_per_end} under each end of the cabinet's bottom, "
        "cabinet top and cabinet shelf, screws included",
        2 * config.braces_per_end * len(braced),
        *config.brace_pack,
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
        sum(pockets[p.label] for p in horizontals if p.name == "shelf"),
        *config.plug_pack,
        config.plug_url,
    ),
    Hardware("Wood glue", "1L", 1, *config.glue_pack),
    Hardware(
        "Anti-tip brackets", "homemade, one per unit", len(units), *config.bracket_pack
    ),
    Hardware(
        "Varnish (litres)",
        f"Ronseal Antique Pine satin, {config.finish_coats} coat, both faces",
        finish_litres,
        *config.finish_pack,
        config.finish_url,
    ),
    Hardware(
        "Primer (litres)",
        "MDF primer, one coat on the backs' grooved face",
        round(back_area / config.primer_coverage, 1),
        *config.primer_pack,
    ),
    Hardware(
        "Black paint (litres)",
        f"GoodHome Liberty black satin, {config.paint_coats} coat over the primer",
        round(back_area * config.paint_coats / config.paint_coverage, 1),
        *config.paint_pack,
        config.paint_url,
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
    sheets,
    config.edge_trim,
    config.kerf,
    config.cut_price,
    config.delivery_price,
)

instructions.write_instructions(
    build / "instructions.md",
    parts,
    hardware,
    widths,
    config.unit_width,
    config.height,
    shelf_depth,
    config.depth,
    config.kickboard_setback,
    config.pocket_spacing,
    config.back_screw_spacing,
    config.door_gap,
    config.hinge_from_door_end,
    config.knob_from_door_edge,
    config.knob_from_door_top,
    config.kerf,
    config.braces_per_end,
    cutting_list,
    groove_offset,
    config.groove_spacing,
    config.layout,
    braced,
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
