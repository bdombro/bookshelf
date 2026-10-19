"""Step-by-step assembly instructions with a shelf marking guide.

Inputs: Part, Hardware and Dowel rows, settings, derived sizes, the packing and the
pocketed panels.
Outputs: build/instructions.md, rendered from templates/instructions.md.j2; Python only
computes the values the template prints.
Implements spec 5 (Construction) and the instructions part of 6.5 (Outputs).
"""

import math
from collections import Counter
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from bookshelf.model.sizes import Sizes
from bookshelf.outputs.diagrams import diagram_name, sheet_title
from bookshelf.packing.packer import eps
from bookshelf.packing.sheets import Packed
from bookshelf.rows import Dowel, Hardware, Part
from bookshelf.settings import Settings
from bookshelf.text import size

templates = Path(__file__).parent / "templates"


def cut_sheets(packed: Packed) -> list[dict[str, Any]]:
    """Each sheet's strips and crosscuts, in cutting order."""
    sheets = []
    for m, count in packed.counts.items():
        for sheet in range(count):
            on_sheet = [p for p in packed.packings[m] if p.sheet == sheet]
            title = sheet_title(m, sheet, count)
            strips = []
            for strip in dict.fromkeys(p.strip for p in on_sheet):
                in_strip = [p for p in on_sheet if p.strip == strip]
                strips.append(
                    {
                        "width": in_strip[0].strip_width,
                        "cuts": [
                            {
                                "length": p.part.length,
                                "label": p.part.label,
                                "rip_to": p.part.width
                                if p.part.width < p.strip_width - eps
                                else None,
                            }
                            for p in in_strip
                        ],
                    }
                )
            sheets.append(
                {
                    "title": f"{title[0].upper()}{title[1:]}",
                    "strips": strips,
                    "diagram": diagram_name(m, sheet),
                }
            )
    return sheets


def pocket_count(width: float, spacing: float) -> int:
    """Pockets per end along a panel's width."""
    return max(2, math.ceil(width / spacing))


def context(
    parts: list[Part],
    hardware: list[Hardware],
    settings: Settings,
    sizes: Sizes,
    packed: Packed,
    pocketed_labels: set[str],
    dowels: list[Dowel],
) -> dict[str, Any]:
    """Every value the template prints."""
    c = settings
    bay_types = [k for k in dict.fromkeys(p.unit_type for p in parts) if k != "frame"]
    units = list(dict.fromkeys(p.unit for p in parts))
    pocketed = [p for p in parts if p.label in pocketed_labels]
    dowel_groups: dict[tuple[str, tuple[float, ...], float], list[str]] = {}
    for d in dowels:
        names = dowel_groups.setdefault((d.unit_type, d.positions, d.front), [])
        if d.name not in names:
            names.append(d.name)
    groups = Counter(
        (p.name, p.unit_type, p.length, p.width, p.thickness) for p in parts
    )
    kick = next(p for p in parts if p.name == "kickboard" and p.unit_type == "narrow")
    kick_n = pocket_count(kick.width, c.pocket_spacing)
    door = next((p for p in parts if p.name == "door"), None)
    shelf = next((p for p in parts if p.name == "cabinet_shelf"), None)
    counts = {row.item: row.quantity for row in hardware}
    return {
        "counts": counts,
        "unit_list": ", ".join(
            f"{unit} ({', '.join(bays)})"
            for unit, bays in zip(units, c.layout, strict=True)
        ),
        "kerf": c.kerf,
        "mitre_capacity": c.mitre_capacity,
        "edge_trim": c.edge_trim,
        "usable": [
            {"length": length, "width": width, "material": m}
            for m, (length, width) in packed.usable.items()
        ],
        "cut_sheets": cut_sheets(packed),
        "groove_offset": sizes.groove_offset,
        "groove_spacing": c.groove_spacing,
        "part_groups": [
            {
                "name": name,
                "kind": kind,
                "qty": qty,
                "length": length,
                "width": width,
                "thickness": thickness,
            }
            for (name, kind, length, width, thickness), qty in groups.items()
        ],
        "bays": [
            {
                "kind": kind,
                "width": sizes.widths[kind],
                "rows": [
                    {
                        "panel": p.label.split(" ")[-1],
                        "centre": (p.bottom + p.top) / 2
                        if p.name != "kickboard"
                        else None,
                        "bottom": p.bottom,
                        "top": p.top,
                        "span": f"{size(c.kickboard_setback)}"
                        f"–{size(c.kickboard_setback + p.thickness)}"
                        if p.name == "kickboard"
                        else f"{size(sizes.shelf_depth - p.width)}"
                        f"–{size(sizes.shelf_depth)}",
                    }
                    for p in sorted(
                        (
                            p
                            for p in parts
                            if p.unit == units[0]
                            and p.unit_type == kind
                            and p.name != "door"
                        ),
                        key=lambda p: p.bottom,
                    )
                ],
            }
            for kind in bay_types
        ],
        "pocket_thicknesses": [
            {
                "mm": thickness * 10,
                "names": list(
                    dict.fromkeys(p.name for p in pocketed if p.thickness == thickness)
                ),
            }
            for thickness in sorted({p.thickness for p in pocketed}, reverse=True)
        ],
        "pocket_spacing": c.pocket_spacing,
        "pocket_positions": [
            {
                "width": width,
                "names": list(
                    dict.fromkeys(
                        p.name
                        for p in pocketed
                        if p.width == width and p.name != "kickboard"
                    )
                ),
                "positions": [
                    width * (i + 0.5) / pocket_count(width, c.pocket_spacing)
                    for i in range(pocket_count(width, c.pocket_spacing))
                ],
            }
            for width in sorted({p.width for p in pocketed if p.name != "kickboard"})
        ],
        "dowel_count": counts["Dowels"],
        "dowel_groups": [
            {
                "bay": bay,
                "panels": names,
                "positions": positions,
                "from_panel": [x - front for x in positions],
                "front": front,
            }
            for (bay, positions, front), names in sorted(
                dowel_groups.items(), key=lambda kv: bay_types.index(kv[0][0])
            )
        ],
        "dowel_diameter_mm": c.dowel_diameter * 10,
        "dowel_length_mm": c.dowel_length * 10,
        "dowel_hole_mm": c.dowel_hole_depth * 10,
        "dowel_end_hole_mm": c.dowel_end_hole_depth * 10,
        "dowel_bay_offset": c.dowel_bay_offset,
        "dowel_thickness_mm": sizes.s * 10,
        "kickboard": {
            "count": kick_n,
            "positions": [kick.width * (i + 0.5) / kick_n for i in range(kick_n)],
        },
        "depth": c.depth,
        "shelf_depth": sizes.shelf_depth,
        "braces_per_end": c.braces_per_end,
        "kickboard_screws": c.kickboard_screws,
        "cabinet_top_braces_per_end": c.cabinet_top_braces_per_end,
        "kickboard_setback": c.kickboard_setback,
        "diagonal": math.hypot(c.unit_width, c.height),
        "back_screw_spacing": c.back_screw_spacing,
        "cabinet": {
            "shelf_bottom": shelf.bottom,
            "shelf_front": sizes.shelf_depth - shelf.width,
            "door_bottom": door.bottom,
            "door_top": door.top,
        }
        if door and shelf
        else None,
        "hinge_from_door_end": c.hinge_from_door_end,
        "door_gap": c.door_gap,
        "knob_from_door_edge": c.knob_from_door_edge,
        "knob_from_door_top": c.knob_from_door_top,
        "sweep": math.hypot(c.height, c.depth),
    }


def write_instructions(
    path: Path,
    parts: list[Part],
    hardware: list[Hardware],
    settings: Settings,
    sizes: Sizes,
    packed: Packed,
    pocketed: set[str],
    dowels: list[Dowel],
) -> None:
    """Render instructions.md from the template and the model's numbers."""
    env = Environment(
        loader=FileSystemLoader(templates),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    env.filters["size"] = size
    template = env.get_template("instructions.md.j2")
    path.write_text(
        template.render(
            context(parts, hardware, settings, sizes, packed, pocketed, dowels)
        )
    )
