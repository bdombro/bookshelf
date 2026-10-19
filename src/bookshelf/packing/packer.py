"""Strip packer: ripped strips, crosscuts, ordering search and a self-check.

Inputs: Part rows plus the usable sheet size and kerf.
Outputs: Placement rows; raises ValueError for a part too big or a broken layout.
Implements spec 6.6 (Packing) and 7 (Quality).
"""

import random
from collections import Counter

from bookshelf.rows import Part, Placement

eps = 1e-6


def pack_strips(
    parts: list[Part], length: float, width: float, kerf: float
) -> list[Placement]:
    """Pack parts into ripped strips and crosscut them, greedily in the given order."""
    sheets: list[float] = []  # used width per sheet
    strips: list[list[float]] = []  # [sheet, y, width, used length]
    placements: list[Placement] = []
    for part in parts:
        if part.length > length + eps or part.width > width + eps:
            raise ValueError(
                f"{part.label} is {part.length} × {part.width}, "
                f"larger than the usable sheet {length} × {width}"
            )
        fits = [
            (strip[2] - part.width, index)
            for index, strip in enumerate(strips)
            if part.width <= strip[2] + eps
            and strip[3] + (kerf if strip[3] else 0) + part.length <= length + eps
        ]
        if fits:
            index = min(fits)[1]
        else:
            sheet = next(
                (
                    i
                    for i, used in enumerate(sheets)
                    if used + kerf + part.width <= width + eps
                ),
                None,
            )
            if sheet is None:
                sheets.append(0)
                sheet = len(sheets) - 1
            y = sheets[sheet] + (kerf if sheets[sheet] else 0)
            sheets[sheet] = y + part.width
            strips.append([sheet, y, part.width, 0])
            index = len(strips) - 1
        strip = strips[index]
        x = strip[3] + (kerf if strip[3] else 0)
        strip[3] = x + part.length
        placements.append(Placement(part, int(strip[0]), index, x, strip[1], strip[2]))
    return placements


def best_packing(
    parts: list[Part], length: float, width: float, kerf: float, tries: int = 400
) -> list[Placement]:
    """Try several part orderings; keep the fewest sheets, then strips."""
    orderings = [
        sorted(parts, key=lambda p: (-p.width, -p.length)),
        sorted(parts, key=lambda p: (-p.length, -p.width)),
        sorted(parts, key=lambda p: -p.length * p.width),
    ]
    shuffler = random.Random(0)
    for _ in range(tries):
        shuffled = parts.copy()
        shuffler.shuffle(shuffled)
        orderings.append(shuffled)

    def score(placements: list[Placement]) -> tuple[int, int]:
        return (
            1 + max(p.sheet for p in placements),
            1 + max(p.strip for p in placements),
        )

    best = min((pack_strips(o, length, width, kerf) for o in orderings), key=score)
    check_layout(best, parts, length, width, kerf)
    return best


def check_layout(
    placements: list[Placement],
    parts: list[Part],
    length: float,
    width: float,
    kerf: float,
) -> None:
    """Raise ValueError unless every part is placed once, on the sheet, kerf apart."""
    errors = []
    placed = Counter(p.part for p in placements)
    for part, count in (Counter(parts) - placed).items():
        errors.append(f"{part.label}: placed {placed[part]} times, expected {count}")
    for part, count in (placed - Counter(parts)).items():
        errors.append(f"{part.label}: placed {count} times, expected fewer")
    for p in placements:
        if (
            p.x < -eps
            or p.y < -eps
            or p.x + p.part.length > length + eps
            or p.y + p.part.width > width + eps
        ):
            errors.append(
                f"{p.part.label} at ({p.x:.1f}, {p.y:.1f}) size "
                f"{p.part.length} × {p.part.width} is off the usable sheet "
                f"{length} × {width}"
            )
    for i, a in enumerate(placements):
        for b in placements[i + 1 :]:
            if a.sheet != b.sheet:
                continue
            apart = (
                a.x + a.part.length + kerf <= b.x + eps
                or b.x + b.part.length + kerf <= a.x + eps
                or a.y + a.part.width + kerf <= b.y + eps
                or b.y + b.part.width + kerf <= a.y + eps
            )
            if not apart:
                errors.append(
                    f"{a.part.label} and {b.part.label} on sheet {a.sheet + 1} "
                    f"overlap or are closer than the {kerf}cm kerf"
                )
    if errors:
        raise ValueError("Packing self-check failed:\n  " + "\n  ".join(errors))


def cut_count(placements: list[Placement]) -> int:
    """Rips per strip, a crosscut per part and an extra rip per narrower part."""
    strips = {p.strip for p in placements}
    narrower = sum(p.part.width < p.strip_width - eps for p in placements)
    return len(strips) + len(placements) + narrower
