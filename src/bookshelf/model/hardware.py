"""Hardware and finish rows: counts from the parts, products from the catalog.

Inputs: settings, derived sizes, Part rows and the unit count.
Outputs: Hardware rows, tool rows and the labels of panels with pocket holes.
Implements spec 4 (Materials and cost) and 5 (Construction).
"""

import math
from typing import NamedTuple

from bookshelf.model.dowels import dowel_names
from bookshelf.model.sizes import Sizes
from bookshelf.rows import Hardware, Part
from bookshelf.settings import Settings
from bookshelf.text import size


class HardwareRows(NamedTuple):
    hardware: list[Hardware]
    tools: list[Hardware]
    pocketed: set[str]  # panels fixed with pocket screws


def hardware_rows(
    settings: Settings, sizes: Sizes, parts: list[Part], unit_count: int
) -> HardwareRows:
    """Count every screw, brace, door fitting and finish product the parts need."""
    c, z = settings, sizes
    low, high = c.hinge_rating
    frame_names = ("side", "divider", "door", "back")
    doors = [p for p in parts if p.name == "door"]
    horizontals = [p for p in parts if p.name not in frame_names]
    braced = {
        p.label
        for p in horizontals
        if p.unit_type == "wide" and p.name in ("bottom", "cabinet_top")
    }
    brace_count = sum(
        2
        * (c.cabinet_top_braces_per_end if "cabinet_top" in label else c.braces_per_end)
        for label in braced
    )
    pockets = {
        p.label: 2 * max(2, math.ceil(p.width / c.pocket_spacing))
        for p in horizontals
        if (p.name not in dowel_names or (p.name == "bottom" and p.label not in braced))
        and not (p.name == "kickboard" and p.unit_type == "wide")
    }
    wide_kickboards = sum(
        p.name == "kickboard" and p.unit_type == "wide" for p in parts
    )
    thin_labels = {p.label for p in horizontals if p.material == z.thin_pine}
    dividers = sum(p.name == "divider" for p in parts)
    back_screws = sum(
        math.ceil(p.length / c.back_screw_spacing) + 1
        for p in parts
        if p.name in ("divider", "bottom", "cabinet_top", "cabinet_shelf", "shelf")
    )
    back_area = (
        sum(p.length * p.width for p in parts if p.material == z.back_material) / 10_000
    )
    pine_area = (
        sum(p.length * p.width for p in parts if p.material != z.back_material)
        * 2
        / 10_000
    )
    finish_litres = round(pine_area * c.finish_coats / c.finish_coverage, 1)

    long_screw_count = (
        sum(n for label, n in pockets.items() if label not in thin_labels)
        + c.top_screws_per_divider * dividers
    )
    hardware = [
        Hardware(
            "Hinges",
            2 * len(doors),
            f"rated {size(low * 10)}–{size(high * 10)}mm for {z.thin_pine[:4]} doors",
            *c.hinges,
        ),
        Hardware("Knobs", len(doors), "one per door", *c.knobs),
        Hardware(
            "Wood screws",
            long_screw_count,
            f"one per pocket in the {z.pine[:4]} top, plus "
            f"{c.top_screws_per_divider} down through the top into each divider",
            *c.long_screws,
        ),
        Hardware(
            "Short wood screws",
            sum(n for label, n in pockets.items() if label in thin_labels),
            "one per pocket in the narrow bottoms and kickboards",
            *c.pocket_screws,
        ),
        Hardware(
            "Back screws",
            back_screws,
            f"through the back every {size(c.back_screw_spacing)}cm",
            *c.short_screws,
        ),
        Hardware(
            "Corner braces",
            brace_count,
            f"on top of each end of the wide bottom ({c.braces_per_end}) and "
            f"under each end of the cabinet top ({c.cabinet_top_braces_per_end})",
            *c.braces,
        ),
        Hardware(
            "Kickboard screws",
            c.kickboard_screws * wide_kickboards,
            "down through the wide bottom into the kickboard's top edge",
            *c.short_screws,
        ),
        Hardware(
            "Brace screws",
            c.screws_per_brace_leg * brace_count,
            "for each brace's leg under a panel",
            *c.brace_screws,
        ),
        Hardware(
            "Brace side screws",
            c.screws_per_brace_leg * brace_count,
            "for each brace's leg on a side or divider",
            *c.short_screws,
        ),
        Hardware(
            "Washers",
            long_screw_count,
            "under each 60mm countersunk screw",
            *c.washers,
        ),
        Hardware(
            "Dowels",
            sum(
                2 * max(2, math.ceil(p.width / c.dowel_spacing))
                for p in horizontals
                if p.name in dowel_names
            ),
            "dry, no glue: shelves, bottoms, cabinet tops and cabinet shelves",
            *c.dowels,
        ),
        Hardware("Anti-tip brackets", unit_count, "one per unit", *c.brackets),
        Hardware(
            "Varnish (litres)",
            finish_litres,
            f"{c.finish_coats} coat, both faces",
            *c.varnish,
        ),
        Hardware(
            "Primer (litres)",
            round(back_area / c.primer_coverage, 1),
            "one coat on the backs' grooved face",
            *c.primer,
        ),
        Hardware(
            "Black paint (litres)",
            round(back_area * c.paint_coats / c.paint_coverage, 1),
            f"{c.paint_coats} coat over the primer",
            *c.paint,
        ),
        Hardware("Roller kit", 1, "", *c.roller),
        Hardware(
            "Roller sleeves",
            max(
                0,
                math.ceil(pine_area * c.finish_coats / c.roller_coverage)
                - c.kit_sleeves,
            ),
            f"refills beyond the kit's {c.kit_sleeves}",
            *c.sleeves,
        ),
        Hardware("Brush", 1, "", *c.brush),
        Hardware(
            "Sanding sponges",
            math.ceil(pine_area / c.sanding_coverage),
            "",
            *c.sponges,
        ),
    ]
    tools = [
        Hardware("Plunge saw", 1, "", *c.plunge_saw),
        Hardware("Mitre saw", 1, "crosscuts on narrower strips", *c.mitre_saw),
        Hardware("Guide rails", 1, "", *c.guide_rails),
        Hardware("Saw blade", 1, "for the mitre saw (owned)", *c.saw_blade),
        Hardware("Pocket hole jig", 1, "", *c.pocket_jig),
        Hardware("Drill/driver", 1, "", *c.drill),
        Hardware("Clamps", 1, "", *c.clamps),
        Hardware(
            "Corner clamps", 1, "hold a panel square to the side", *c.corner_clamps
        ),
        Hardware("T-square", 1, "", *c.t_square),
        Hardware("Tape measure", 1, "", *c.tape_measure),
        Hardware("Stud finder", 1, "", *c.stud_finder),
        Hardware("Dowel jig", 1, "centred 8mm holes in panel ends", *c.dowel_jig),
    ]
    return HardwareRows(hardware, tools, set(pockets))
