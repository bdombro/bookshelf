"""Packer self-check tests: each kind of broken layout must be rejected."""

import pytest

from materials import Part, Placement, best_packing, check_layout

length, width, kerf = 243, 121, 0.3


def part(label: str, part_length: float = 50, part_width: float = 30) -> Part:
    return Part(label, "u", "shelf", "wide", part_length, part_width, 2.4, "pine", 0, 0)


def place(p: Part, x: float, y: float, sheet: int = 0) -> Placement:
    return Placement(p, sheet, 0, x, y, p.width)


def test_valid_layout_passes() -> None:
    a, b = part("a"), part("b")
    check_layout([place(a, 0, 0), place(b, 50 + kerf, 0)], [a, b], length, width, kerf)


def test_overlap_rejected() -> None:
    a, b = part("a"), part("b")
    with pytest.raises(ValueError, match="overlap"):
        check_layout([place(a, 0, 0), place(b, 40, 0)], [a, b], length, width, kerf)


def test_missing_part_rejected() -> None:
    a, b = part("a"), part("b")
    with pytest.raises(ValueError, match="placed 0 times"):
        check_layout([place(a, 0, 0)], [a, b], length, width, kerf)


def test_missing_kerf_rejected() -> None:
    a, b = part("a"), part("b")
    with pytest.raises(ValueError, match="kerf"):
        check_layout([place(a, 0, 0), place(b, 50, 0)], [a, b], length, width, kerf)


def test_off_sheet_rejected() -> None:
    a = part("a")
    with pytest.raises(ValueError, match="off the usable sheet"):
        check_layout([place(a, 200, 0)], [a], length, width, kerf)


def test_oversized_part_fails_clearly() -> None:
    with pytest.raises(ValueError, match="larger than the usable sheet"):
        best_packing([part("long", 250)], length, width, kerf)


def test_packing_passes_self_check() -> None:
    parts = [part(f"p{i}", 78.8, 29.5) for i in range(12)]
    placements = best_packing(parts, length, width, kerf)
    assert max(p.sheet for p in placements) == 0
