"""Sizes derived from the settings: shelf heights, bay widths, grooves, materials.

Inputs: settings. Outputs: a Sizes record, all in cm.
Implements spec 3 (Furniture design) and 6.4 (Model).
"""

from dataclasses import dataclass

from bookshelf.settings import Settings
from bookshelf.text import size


@dataclass(frozen=True)
class Sizes:
    t: float  # frame pine thickness
    s: float  # thin pine thickness
    shelf_depth: float
    cabinet_line_bottom: float
    top_bottom: float
    upper_clear: float
    upper_shelves: list[float]
    bottom_top: float
    lower_clear: float
    lower_shelves: list[float]
    door_bottom: float
    door_height: float
    first_bays: list[str]
    inner_width: float
    widths: dict[str, float]
    bay_centres: list[float]  # across the back, from its edge on the first bay's side
    groove_offset: float
    pine: str
    thin_pine: str
    back_material: str
    sheets: dict[str, tuple[float, float, float, str]]


def derive(settings: Settings) -> Sizes:
    """Every size the model and outputs need, computed from the settings."""
    c = settings
    t = c.pine_thickness
    s = c.thin_pine_thickness
    shelf_depth = c.depth - c.back_thickness
    cabinet_line_bottom = c.cabinet_height - s
    top_bottom = c.height - t
    upper_clear = (top_bottom - c.cabinet_height - c.shelves_above_cabinet * s) / (
        c.shelves_above_cabinet + 1
    )
    upper_shelves = [
        c.cabinet_height + (i + 1) * upper_clear + i * s
        for i in range(c.shelves_above_cabinet)
    ]
    bottom_top = c.kickboard_height + s
    lower_clear = (cabinet_line_bottom - bottom_top - c.narrow_lower_shelves * s) / (
        c.narrow_lower_shelves + 1
    )
    lower_shelves = [
        bottom_top + (i + 1) * lower_clear + i * s
        for i in range(c.narrow_lower_shelves)
    ]
    first_bays = c.layout[0]
    inner_width = c.unit_width - 2 * t
    widths = {
        "narrow": c.narrow_width,
        "wide": (
            inner_width
            - (len(first_bays) - 1) * t
            - first_bays.count("narrow") * c.narrow_width
        )
        / first_bays.count("wide"),
    }
    bay_centres = []
    edge = 0.0
    for bay in first_bays:
        bay_centres.append(edge + widths[bay] / 2)
        edge += widths[bay] + t
    groove_offset = (bay_centres[0] + c.groove_spacing / 2) % c.groove_spacing
    pine = f"{size(t * 10)}mm laminated pine"
    thin_pine = f"{size(s * 10)}mm laminated pine"
    back_material = f"{size(c.back_thickness * 10)}mm V-groove MDF"
    return Sizes(
        t=t,
        s=s,
        shelf_depth=shelf_depth,
        cabinet_line_bottom=cabinet_line_bottom,
        top_bottom=top_bottom,
        upper_clear=upper_clear,
        upper_shelves=upper_shelves,
        bottom_top=bottom_top,
        lower_clear=lower_clear,
        lower_shelves=lower_shelves,
        door_bottom=bottom_top + c.door_gap,
        door_height=cabinet_line_bottom - c.door_gap - (bottom_top + c.door_gap),
        first_bays=first_bays,
        inner_width=inner_width,
        widths=widths,
        bay_centres=bay_centres,
        groove_offset=groove_offset,
        pine=pine,
        thin_pine=thin_pine,
        back_material=back_material,
        sheets={
            pine: c.frame_sheet,
            thin_pine: c.thin_sheet,
            back_material: c.back_sheet,
        },
    )
