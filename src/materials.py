"""Sheet packing, cost totals, the material spec and sheet cutting diagrams.

Inputs: Part and Hardware rows plus sheet, saw and price settings from model.py.
Outputs: build/materials.md and build/sheets/*.svg.
Implements spec 4 (Materials and cost), 6.5 (Outputs) and 6.6 (Packing).
"""

import math
import random
from collections import Counter
from pathlib import Path
from typing import NamedTuple

eps = 1e-6


class Part(NamedTuple):
    label: str  # e.g. "wide_1 / shelf_2"
    unit: str  # e.g. "wide_1"
    name: str  # e.g. "shelf"
    unit_type: str  # "wide" or "narrow"
    length: float  # along the grain
    width: float
    thickness: float
    material: str
    bottom: float  # height above the floor
    top: float


class Hardware(NamedTuple):
    item: str
    spec: str
    quantity: int
    pack_size: int
    pack_price: float


class Placement(NamedTuple):
    part: Part
    sheet: int
    strip: int
    x: float  # along the sheet's length, from the usable area's corner
    y: float  # across the sheet
    strip_width: float


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


def hardware_cost(row: Hardware) -> float:
    """Whole packs needed for the count, priced."""
    return math.ceil(row.quantity / row.pack_size) * row.pack_price


def money(value: float) -> str:
    """Euro amount, or unknown for an unpriced 0."""
    return f"€{value:,.2f}" if value else "unknown"


def size(value: float) -> str:
    """A cm figure to 0.1cm, without a trailing .0."""
    return f"{value:.1f}".removesuffix(".0")


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


def write_materials(
    parts: list[Part],
    hardware: list[Hardware],
    path: Path,
    sheets_dir: Path,
    sheet_length: float,
    sheet_width: float,
    edge_trim: float,
    kerf: float,
    sheet_prices: dict[str, float],
    cut_price: float,
    delivery_price: float,
) -> dict[str, int]:
    """Pack each material, write materials.md and sheet diagrams; return counts."""
    usable_length = sheet_length - 2 * edge_trim
    usable_width = sheet_width - 2 * edge_trim
    materials = list(dict.fromkeys(p.material for p in parts))
    packings = {
        m: best_packing(
            [p for p in parts if p.material == m], usable_length, usable_width, kerf
        )
        for m in materials
    }
    counts = {m: 1 + max(p.sheet for p in packings[m]) for m in materials}
    cuts = sum(cut_count(packings[m]) for m in materials)
    warning = (
        f"⚠️ **Saw width:** the packing assumes a {size(kerf * 10)}mm saw cut. Panel "
        "saws often cut ~4mm; confirm the cutter's saw width and update `kerf` before "
        "ordering precut."
    )

    lines = [
        "# Materials",
        "",
        "Generated by `just build`; do not edit. Prices are estimates until quoted.",
        "",
        "## Parts",
        "",
        "| Part | Unit type | Qty | Length × width (cm) | Thickness (cm) | Material |",
        "| ---- | --------- | --: | ------------------- | -------------: | -------- |",
    ]
    groups = Counter(
        (p.name, p.unit_type, p.length, p.width, p.thickness, p.material) for p in parts
    )
    for (name, unit_type, length, width, thickness, material), qty in groups.items():
        lines.append(
            f"| {name} | {unit_type} | {qty} | {size(length)} × {size(width)} | "
            f"{size(thickness)} | {material} |"
        )

    lines += [
        "",
        "## Sheets to buy",
        "",
        "| Material | Sheet (cm) | Count | Area used | Price each | Total |",
        "| -------- | ---------- | ----: | --------: | ---------: | ----: |",
    ]
    sheet_total = 0.0
    for m in materials:
        area = sum(p.length * p.width for p in parts if p.material == m)
        used = area / (counts[m] * sheet_length * sheet_width)
        total = counts[m] * sheet_prices[m]
        sheet_total += total
        lines.append(
            f"| {m} | {size(sheet_length)} × {size(sheet_width)} | {counts[m]} | "
            f"{used:.0%} | {money(sheet_prices[m])} | {money(total)} |"
        )
    lines += ["", warning, "", "## Cutting list", ""]
    lines.append(
        f"Each sheet is trimmed {size(edge_trim)}cm on every edge, leaving "
        f"{size(usable_length)} × {size(usable_width)}cm. Rip the strips across the "
        f"sheet in order, then crosscut each strip. Every part's length runs along "
        f"the grain. Saw cut {size(kerf)}cm."
    )
    sheets_dir.mkdir(parents=True, exist_ok=True)
    for old in sheets_dir.glob("*.svg"):
        old.unlink()
    stacked: list[str] = []
    stacked_w = stacked_h = 0.0
    for m in materials:
        slug = m.replace(" ", "_")
        for sheet in range(counts[m]):
            on_sheet = [p for p in packings[m] if p.sheet == sheet]
            title = f"{m} sheet {sheet + 1} of {counts[m]}"
            lines += ["", f"### {title[0].upper()}{title[1:]}", ""]
            strip_ids = list(dict.fromkeys(p.strip for p in on_sheet))
            for n, strip in enumerate(strip_ids, 1):
                in_strip = [p for p in on_sheet if p.strip == strip]
                lines.append(f"{n}. Rip a {size(in_strip[0].strip_width)}cm strip:")
                for p in in_strip:
                    extra = (
                        f", then rip to {size(p.part.width)}cm"
                        if p.part.width < p.strip_width - eps
                        else ""
                    )
                    lines.append(
                        f"   - crosscut {size(p.part.length)}cm: {p.part.label}{extra}"
                    )
            diagram = sheets_dir / f"{slug}_{sheet + 1}.svg"
            body, w, h = sheet_svg(
                on_sheet, title, sheet_length, sheet_width, edge_trim
            )
            diagram.write_text(svg_file(body, w, h))
            stacked.append(f'<g transform="translate(0 {stacked_h})">\n{body}\n</g>')
            stacked_w, stacked_h = max(stacked_w, w), stacked_h + h
            lines.append(f"\nDiagram: `sheets/{diagram.name}`")
    (sheets_dir / "all.svg").write_text(
        svg_file("\n".join(stacked), stacked_w, stacked_h)
    )
    lines.append("\nAll sheets stacked: `sheets/all.svg`")

    lines += [
        "",
        "## Hardware and finish",
        "",
        "| Item | Spec | Count | Packs | Cost |",
        "| ---- | ---- | ----: | ----: | ---: |",
    ]
    hardware_total = 0.0
    for row in hardware:
        cost = hardware_cost(row)
        hardware_total += cost
        packs = math.ceil(row.quantity / row.pack_size)
        lines.append(
            f"| {row.item} | {row.spec} | {row.quantity} | {packs} × {row.pack_size} | "
            f"{money(cost)} |"
        )
    cut_total = cuts * cut_price
    total = sheet_total + cut_total + hardware_total + delivery_price
    lines += [
        "",
        "## Cost",
        "",
        "All figures are estimates until replaced with quotes.",
        "",
        "| | Estimate |",
        "| - | -------: |",
        f"| Sheets | {money(sheet_total)} |",
        f"| Cutting ({cuts} cuts at {money(cut_price)}) | {money(cut_total)} |",
        f"| Hardware and finish | {money(hardware_total)} |",
        f"| Delivery | {money(delivery_price)} |",
        f"| **Total** | **{money(total)}**"
        f"{' before delivery' if not delivery_price else ''} |",
        "",
        warning,
        "",
    ]
    path.write_text("\n".join(lines))
    return counts
