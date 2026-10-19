"""Model and requirement checks; each returns error messages with actual and expected.

Inputs: settings, derived sizes and, for geometry, the Layout.
Outputs: lists of error strings; check_* raise ValueError listing them all.
Implements spec 7 (Quality).
"""

import math
from itertools import combinations

from build123d import CM

from bookshelf.model.layout import Layout, unit_gap
from bookshelf.model.sizes import Sizes
from bookshelf.rows import Dowel
from bookshelf.settings import Settings


def geometry_errors(settings: Settings, sizes: Sizes, layout: Layout) -> list[str]:
    """Bounding box, unit widths, overlaps and sheet fit of the built model."""
    c = settings
    errors = []
    units = layout.units
    expected = (
        len(units) * c.unit_width + (len(units) - 1) * unit_gap,
        c.depth,
        c.height,
    )
    actual = layout.assembly.bounding_box().size / CM
    for axis, a, e in zip(("width", "depth", "height"), actual, expected, strict=True):
        if abs(a - e) > 0.01:
            errors.append(f"bounding box {axis} {a:.1f}, expected {e:.1f}")
    for (label_a, a), (label_b, b) in combinations(layout.solids_by_label.items(), 2):
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
        if abs(unit_width - c.unit_width) > 0.01:
            errors.append(f"{u.label} width {unit_width:.1f}, expected {c.unit_width}")
    for p in layout.parts:
        sheet_length, sheet_width, *_ = sizes.sheets[p.material]
        usable_length = sheet_length - 2 * c.edge_trim
        usable_width = sheet_width - 2 * c.edge_trim
        if p.length > usable_length or p.width > usable_width:
            errors.append(
                f"{p.label} is {p.length} × {p.width}, expected to fit the usable "
                f"sheet {usable_length} × {usable_width} along the grain"
            )
    return errors


def requirement_errors(settings: Settings, sizes: Sizes) -> list[str]:
    """Groove symmetry, wall width, compartment height and hinge rating."""
    c = settings
    errors = []
    for bay, centre in zip(sizes.first_bays, sizes.bay_centres, strict=True):
        off = (centre - sizes.groove_offset) % (c.groove_spacing / 2)
        if min(off, c.groove_spacing / 2 - off) > 0.01:
            errors.append(
                f"{bay} bay's V-grooves are {off:.2f}cm off symmetric, expected 0; "
                "adjust unit_width"
            )
    if c.unit_width > c.max_unit_width:
        errors.append(
            f"unit width {c.unit_width}, expected at most {c.max_unit_width} "
            "to fit the wall"
        )
    for where, clear in (
        ("above the cabinet", sizes.upper_clear),
        ("below it", sizes.lower_clear),
    ):
        if clear < c.min_compartment:
            errors.append(
                f"compartments {where} are {clear:.1f} clear, expected at least "
                f"{c.min_compartment}"
            )
    low, high = c.hinge_rating
    if not low <= sizes.s <= high:
        errors.append(
            f"doors are {sizes.s} thick, expected {low}–{high} for the hinges"
        )
    return errors


def dowel_errors(settings: Settings, sizes: Sizes, dowels: list[Dowel]) -> list[str]:
    """Dowel fit, holes inside their panel and clearance between the divider's faces."""
    c = settings
    errors = []
    reach = c.dowel_hole_depth + c.dowel_end_hole_depth
    if reach < c.dowel_length:
        errors.append(
            f"dowel holes take {reach:.1f}cm, expected at least the dowel's "
            f"{c.dowel_length:.1f}"
        )
    if c.dowel_hole_depth >= sizes.t:
        errors.append(
            f"dowel holes {c.dowel_hole_depth:.1f}cm deep, expected under the "
            f"frame's {sizes.t:.1f}"
        )
    for d in dowels:
        for x in d.positions:
            if x - c.dowel_diameter / 2 < d.front or (
                x + c.dowel_diameter / 2 > d.front + d.depth
            ):
                errors.append(
                    f"{d.label} dowel at {x:.1f} is outside its panel "
                    f"{d.front:.1f}–{d.front + d.depth:.1f}"
                )
    for a, b in combinations(dowels, 2):
        if a.unit != b.unit or a.unit_type == b.unit_type:
            continue  # opposite faces of a divider belong to different bay types
        for x in a.positions:
            for y in b.positions:
                gap = math.hypot(x - y, a.height - b.height) - c.dowel_diameter
                if gap < c.dowel_clearance:
                    errors.append(
                        f"{a.label} and {b.label} dowel holes are {gap:.1f}cm apart "
                        f"at the divider, expected at least {c.dowel_clearance}"
                    )
    return errors


def raise_if(errors: list[str]) -> None:
    """Raise ValueError listing every error."""
    if errors:
        raise ValueError("Model checks failed:\n  " + "\n  ".join(errors))
