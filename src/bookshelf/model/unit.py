"""One unit's panels as labeled Build123d boxes.

Inputs: settings, derived sizes and a unit's bay types left to right.
Outputs: labeled, coloured boxes; origin at the floor, front-left of the carcass.
Implements spec 3 (Furniture design) and 6.4 (Model).
"""

from build123d import CM, Align, Box, Color, Pos

from bookshelf.model.sizes import Sizes
from bookshelf.settings import Settings


def unit(settings: Settings, sizes: Sizes, bays: list[str]) -> list[Box]:
    """One unit's labeled panels, origin at the floor, front-left of the carcass."""
    c = settings
    t, s = sizes.t, sizes.s

    def panel(
        label: str, x: float, y: float, z: float, sx: float, sy: float, sz: float
    ) -> Box:
        solid = Pos(x * CM, y * CM, z * CM) * Box(
            sx * CM, sy * CM, sz * CM, align=Align.MIN
        )
        solid.label = label
        solid.color = Color(c.back_color if label == "back" else c.pine_color)
        return solid

    parts = [
        panel("side_1", 0, 0, 0, t, c.depth, c.height),
        panel("side_2", c.unit_width - t, 0, 0, t, c.depth, c.height),
        panel("top", t, 0, sizes.top_bottom, sizes.inner_width, c.depth, t),
        panel(
            "back",
            t,
            sizes.shelf_depth,
            0,
            sizes.inner_width,
            c.back_thickness,
            sizes.top_bottom,
        ),
    ]
    x = t
    for i, bay in enumerate(bays):
        if i:
            parts.append(
                panel(f"divider_{i}", x, 0, 0, t, sizes.shelf_depth, sizes.top_bottom)
            )
            x += t
        width = sizes.widths[bay]
        cabinet = bay == "wide"
        horizontal = (
            [("bottom", c.kickboard_height), ("cabinet_top", sizes.cabinet_line_bottom)]
            if cabinet
            else [("bottom", c.kickboard_height)]
        )
        shelves = (
            sizes.upper_shelves
            if cabinet
            else [*sizes.lower_shelves, sizes.cabinet_line_bottom, *sizes.upper_shelves]
        )
        parts += [
            *(
                panel(f"{bay} {n}", x, 0, z, width, sizes.shelf_depth, s)
                for n, z in horizontal
            ),
            *(
                panel(f"{bay} shelf_{j}", x, 0, z, width, sizes.shelf_depth, s)
                for j, z in enumerate(shelves, 1)
            ),
            panel(
                f"{bay} kickboard",
                x,
                c.kickboard_setback,
                0,
                width,
                s,
                c.kickboard_height,
            ),
        ]
        if cabinet:
            door_width = (width - 3 * c.door_gap) / 2
            parts += [
                *(
                    panel(
                        f"{bay} cabinet_shelf",
                        x,
                        sizes.shelf_depth - c.cabinet_shelf_depth,
                        z,
                        width,
                        c.cabinet_shelf_depth,
                        s,
                    )
                    for z in sizes.lower_shelves
                ),
                panel(
                    f"{bay} door_1",
                    x + c.door_gap,
                    0,
                    sizes.door_bottom,
                    door_width,
                    s,
                    sizes.door_height,
                ),
                panel(
                    f"{bay} door_2",
                    x + width - c.door_gap - door_width,
                    0,
                    sizes.door_bottom,
                    door_width,
                    s,
                    sizes.door_height,
                ),
            ]
        x += width
    return parts
