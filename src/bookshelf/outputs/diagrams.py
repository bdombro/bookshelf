"""Sheet cutting diagrams as SVG.

Inputs: Placement rows, sheet sizes and edge trim.
Outputs: SVG elements per sheet and the stacked all-sheets file.
Implements spec 6.5 (Outputs).
"""

from pathlib import Path

from bookshelf.packing.sheets import Packed, SheetSpec
from bookshelf.rows import Placement
from bookshelf.text import size


def sheet_svg(
    placements: list[Placement],
    title: str,
    sheet_length: float,
    sheet_width: float,
    edge_trim: float,
) -> tuple[str, float, float]:
    """One sheet's cutting diagram as SVG elements, with its width and height."""
    scale = 5
    margin = 30
    w = sheet_length * scale + 2 * margin
    h = sheet_width * scale + 2 * margin + 30
    out = [
        f'<text x="{margin}" y="20" font-size="16">{title}</text>',
        f'<rect x="{margin}" y="{margin}" width="{sheet_length * scale}" '
        f'height="{sheet_width * scale}" fill="#f4f4f4" stroke="#000"/>',
    ]
    arrow_y = margin + sheet_width * scale + 20
    out.append(
        f'<text x="{margin}" y="{arrow_y + 4}" font-size="12">grain ⟶ along the '
        f"{size(sheet_length)}cm length</text>"
    )
    for p in placements:
        x = margin + (edge_trim + p.x) * scale
        y = margin + (edge_trim + p.y) * scale
        pw = p.part.length * scale
        ph = p.part.width * scale
        cx = x + pw / 2
        cy = y + ph / 2
        out += [
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{pw:.1f}" height="{ph:.1f}" '
            'fill="#e8c98f" stroke="#7a5420"/>',
            f'<line x1="{x + 8:.1f}" y1="{y + ph - 8:.1f}" x2="{x + 38:.1f}" '
            f'y2="{y + ph - 8:.1f}" stroke="#7a5420"/>',
            f'<text x="{x + 40:.1f}" y="{y + ph - 4:.1f}" font-size="10" '
            'fill="#7a5420">&gt;</text>',
            f'<text x="{cx:.1f}" y="{cy - 2:.1f}" font-size="12" '
            f'text-anchor="middle">{p.part.label}</text>',
            f'<text x="{cx:.1f}" y="{cy + 12:.1f}" font-size="11" '
            f'text-anchor="middle">{size(p.part.length)} × '
            f"{size(p.part.width)}</text>",
        ]
    return "\n".join(out), w, h


def svg_file(body: str, w: float, h: float) -> str:
    """Wrap SVG elements in a document of the given size."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" font-family="sans-serif">\n{body}\n</svg>\n'
    )


def write_diagrams(
    sheets_dir: Path,
    packed: Packed,
    sheets: dict[str, SheetSpec],
    edge_trim: float,
) -> None:
    """Write one SVG per sheet and all.svg stacking them."""
    sheets_dir.mkdir(parents=True, exist_ok=True)
    for old in sheets_dir.glob("*.svg"):
        old.unlink()
    stacked: list[str] = []
    stacked_w = stacked_h = 0.0
    for m, count in packed.counts.items():
        for sheet in range(count):
            on_sheet = [p for p in packed.packings[m] if p.sheet == sheet]
            title = sheet_title(m, sheet, count)
            body, w, h = sheet_svg(on_sheet, title, *sheets[m][:2], edge_trim)
            (sheets_dir / diagram_name(m, sheet)).write_text(svg_file(body, w, h))
            stacked.append(f'<g transform="translate(0 {stacked_h})">\n{body}\n</g>')
            stacked_w, stacked_h = max(stacked_w, w), stacked_h + h
    (sheets_dir / "all.svg").write_text(
        svg_file("\n".join(stacked), stacked_w, stacked_h)
    )


def diagram_name(material: str, sheet: int) -> str:
    """File name of a sheet's diagram."""
    return f"{material.replace(' ', '_')}_{sheet + 1}.svg"


def sheet_title(material: str, sheet: int, count: int) -> str:
    """Title of a sheet's diagram, e.g. "18mm laminated pine sheet 1 of 2"."""
    return f"{material} sheet {sheet + 1} of {count}"
