"""Place the units side by side and derive each panel's Part row from its solid.

Inputs: settings and derived sizes.
Outputs: a Layout of unit compounds, the assembly, Part rows and solids by label.
Implements spec 6.4 (Model).
"""

from typing import NamedTuple

from build123d import CM, Compound, Pos
from build123d.topology import Shape

from bookshelf.model.sizes import Sizes
from bookshelf.model.unit import unit
from bookshelf.rows import Part
from bookshelf.settings import Settings

eps = 1e-6  # rounds float halves like 107.85 up
unit_gap = 60  # between units in the drawings and models; nothing built depends on it


class Layout(NamedTuple):
    units: list[Compound]
    assembly: Compound
    parts: list[Part]
    solids_by_label: dict[str, Shape]


def build_layout(settings: Settings, sizes: Sizes) -> Layout:
    """Every unit built, moved into place and labeled, with its part rows."""
    c, z = settings, sizes
    units: list[Compound] = []
    parts: list[Part] = []
    for n, bays in enumerate(c.layout, 1):
        name = f"unit_{n}"
        x = (n - 1) * (c.unit_width + unit_gap)
        solids = []
        for solid in unit(c, z, bays):
            label = solid.label
            moved = Pos(x * CM, 0, 0) * solid
            moved.label = label
            solids.append(moved)
            bay, _, piece = label.rpartition(" ")
            part_name = piece.rstrip("_0123456789")
            box = moved.bounding_box()
            along = (
                2 if part_name in ("side", "divider", "door", "back") else 0
            )  # grain
            length = round(tuple(box.size)[along] / CM + eps, 1)
            thickness, width = sorted(
                round(v / CM + eps, 1)
                for i, v in enumerate(tuple(box.size))
                if i != along
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
                    material=z.back_material
                    if part_name == "back"
                    else z.pine
                    if abs(thickness - z.t) < eps
                    else z.thin_pine,
                    bottom=round(box.min.Z / CM + eps, 1),
                    top=round(box.max.Z / CM + eps, 1),
                )
            )
        units.append(Compound(children=solids, label=name))
    assembly = Compound(children=units, label="bookshelf")
    solids_by_label = {
        f"{u.label} / {child.label}": child for u in units for child in u.children
    }
    return Layout(units, assembly, parts, solids_by_label)
