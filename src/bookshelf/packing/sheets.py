"""Pack every material's parts onto its sheets and enforce the sheet limit.

Inputs: Part rows, sheet sizes, edge trim, kerf and the sheet limit.
Outputs: usable sizes, a packing and a sheet count per material.
Implements spec 6.6 (Packing) and 7 (Quality).
"""

from typing import NamedTuple

from bookshelf.packing.packer import best_packing
from bookshelf.rows import Part, Placement

type SheetSpec = tuple[float, float, float, str]  # length, width, price, url


class Packed(NamedTuple):
    """Usable area, placements and sheet count per material."""

    usable: dict[str, tuple[float, float]]
    packings: dict[str, list[Placement]]
    counts: dict[str, int]


def pack_materials(
    parts: list[Part],
    sheets: dict[str, SheetSpec],
    edge_trim: float,
    kerf: float,
    max_sheets: int,
) -> Packed:
    """Pack each material; raise ValueError if any needs more than max_sheets."""
    materials = list(dict.fromkeys(p.material for p in parts))
    usable = {
        m: (sheets[m][0] - 2 * edge_trim, sheets[m][1] - 2 * edge_trim)
        for m in materials
    }
    packings = {
        m: best_packing([p for p in parts if p.material == m], *usable[m], kerf)
        for m in materials
    }
    counts = {m: 1 + max(p.sheet for p in packings[m]) for m in materials}
    over = [
        f"{m}: {n} sheets, expected at most {max_sheets}"
        for m, n in counts.items()
        if n > max_sheets
    ]
    if over:
        raise ValueError(
            "Sheet limit exceeded; improve the packer or raise max_sheets:\n  "
            + "\n  ".join(over)
        )
    return Packed(usable, packings, counts)
