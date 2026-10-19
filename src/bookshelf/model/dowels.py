"""Dowel positions: which panels sit on dry dowels and where the holes go.

Inputs: settings, derived sizes and Part rows.
Outputs: Dowel rows, positions measured from the carcass front.
Implements spec 3.2 (Frame and bays) and 5 (Construction).
"""

import math

from bookshelf.model.sizes import Sizes
from bookshelf.rows import Dowel, Part
from bookshelf.settings import Settings

dowel_names = ("shelf", "bottom", "cabinet_top", "cabinet_shelf")


def dowel_rows(settings: Settings, sizes: Sizes, parts: list[Part]) -> list[Dowel]:
    """A row per panel that sits on dowels between a side and the divider."""
    c = settings
    rows = []
    for p in parts:
        if p.name not in dowel_names:
            continue
        count = max(2, math.ceil(p.width / c.dowel_spacing))
        front = round(
            sizes.shelf_depth - p.width, 2
        )  # the cabinet shelf sits against the back
        shift = c.dowel_bay_offset if p.unit_type == "wide" else 0
        rows.append(
            Dowel(
                label=p.label,
                unit=p.unit,
                name=p.name,
                unit_type=p.unit_type,
                height=(p.bottom + p.top) / 2,
                front=front,
                depth=p.width,
                positions=tuple(
                    round(front + p.width * (i + 0.5) / count + shift, 2)
                    for i in range(count)
                ),
            )
        )
    return rows
