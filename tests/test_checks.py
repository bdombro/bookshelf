"""Model, requirement and sheet-limit checks: each fails on settings that break it."""

from pathlib import Path

import pytest

from bookshelf.build import build
from bookshelf.model.checks import (
    dowel_errors,
    geometry_errors,
    raise_if,
    requirement_errors,
)
from bookshelf.model.dowels import dowel_rows
from bookshelf.model.layout import Layout, build_layout
from bookshelf.model.sizes import derive
from bookshelf.packing.sheets import pack_materials
from bookshelf.settings import load


def requirement(**overrides: object) -> list[str]:
    settings = load(**overrides)
    return requirement_errors(settings, derive(settings))


def geometry(layout_settings: dict[str, object], **overrides: object) -> list[str]:
    """Geometry errors for a layout built from one settings and checked with another."""
    built = load(**layout_settings)
    layout = build_layout(built, derive(built))
    checked = load(**{**layout_settings, **overrides})
    return geometry_errors(checked, derive(checked), layout)


def test_defaults_pass_requirement_checks() -> None:
    assert requirement() == []


def test_defaults_pass_geometry_checks() -> None:
    assert geometry({}) == []


def test_unit_wider_than_wall_rejected() -> None:
    errors = requirement(unit_width=118.7)  # symmetric grooves, but too wide
    assert errors == ["unit width 118.7, expected at most 115.6 to fit the wall"]


def test_compartment_below_minimum_rejected() -> None:
    errors = requirement(min_compartment=40)
    assert len(errors) == 2
    assert (
        "compartments above the cabinet are 29.2 clear, expected at least 40"
        in (errors[0])
    )
    assert "compartments below it" in errors[1]


def test_door_outside_hinge_rating_rejected() -> None:
    errors = requirement(thin_pine_thickness=2.4)
    assert "doors are 2.4 thick, expected 1.6–1.9 for the hinges" in errors


def test_hinge_rating_limit_is_a_setting() -> None:
    assert requirement(hinge_rating=(2.0, 2.5)) == [
        "doors are 1.8 thick, expected 2.0–2.5 for the hinges"
    ]


def test_groove_asymmetry_rejected() -> None:
    errors = requirement(unit_width=114.7)
    assert errors
    assert all("off symmetric, expected 0" in e for e in errors)


def test_overlapping_panels_rejected() -> None:
    settings = load()
    layout = build_layout(settings, derive(settings))
    first = next(iter(layout.solids_by_label.values()))
    doubled = Layout(
        layout.units,
        layout.assembly,
        layout.parts,
        {**layout.solids_by_label, "copy": first},
    )
    errors = geometry_errors(settings, derive(settings), doubled)
    assert any("overlap by" in e and "expected no overlap" in e for e in errors)


def test_bounding_box_mismatch_rejected() -> None:
    errors = geometry({}, depth=31)
    assert errors == ["bounding box depth 29.5, expected 31.0"]


def test_unit_width_mismatch_rejected() -> None:
    errors = geometry({}, unit_width=110)
    assert any("width 113.7, expected 110" in e for e in errors)


def test_panel_longer_than_sheet_rejected() -> None:
    errors = geometry({}, frame_sheet=(200, 121.5, 123.0, ""))
    assert any("expected to fit the usable sheet" in e for e in errors)


def test_raise_if_lists_every_error() -> None:
    with pytest.raises(ValueError, match="Model checks failed:\n  a\n  b"):
        raise_if(["a", "b"])
    raise_if([])


def test_sheet_count_over_limit_rejected() -> None:
    settings = load(max_sheets=1)
    sizes = derive(settings)
    layout = build_layout(settings, sizes)
    with pytest.raises(ValueError, match=r"sheets, expected at most 1"):
        pack_materials(layout.parts, sizes.sheets, settings.edge_trim, settings.kerf, 1)


def test_unknown_setting_rejected() -> None:
    with pytest.raises(ValueError, match="unknown settings"):
        load(no_such_setting=100)


def test_defaults_build_cleanly(tmp_path: Path) -> None:
    sizes, layout = build(load(), tmp_path)
    assert len(layout.units) == 2
    assert sizes.groove_offset > 0
    for name in ("materials.md", "instructions.md", "front.svg", "bookshelf.stl"):
        assert (tmp_path / name).stat().st_size > 0


def dowels(**overrides: object) -> list[str]:
    settings = load(**overrides)
    sizes = derive(settings)
    rows = dowel_rows(settings, sizes, build_layout(settings, sizes).parts)
    return dowel_errors(settings, sizes, rows)


def test_defaults_pass_dowel_checks() -> None:
    assert dowels() == []


def test_dowel_holes_meeting_at_divider_rejected() -> None:
    errors = dowels(dowel_bay_offset=0)
    assert errors
    assert all(
        "dowel holes are -0.8cm apart at the divider, expected at least 0.8" in e
        for e in errors
    )


def test_dowel_longer_than_holes_rejected() -> None:
    assert dowels(dowel_length=4.0) == [
        "dowel holes take 3.2cm, expected at least the dowel's 4.0"
    ]


def test_dowel_outside_panel_rejected() -> None:
    errors = dowels(dowel_bay_offset=9)
    assert any("is outside its panel" in e for e in errors)
