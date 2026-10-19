"""Build entry point: settings, model, checks, packing, then every output in build/.

Inputs: optional settings overrides; --view opens the OCP CAD Viewer.
Outputs: build/bookshelf.step, bookshelf.stl, front.svg, materials.md, sheets/*.svg and
instructions.md.
Implements spec 6.1 (Architecture), 6.5 (Outputs) and 7 (Quality).
"""

import sys
from pathlib import Path

from bookshelf import settings as settings_module
from bookshelf.model.checks import (
    dowel_errors,
    geometry_errors,
    raise_if,
    requirement_errors,
)
from bookshelf.model.dowels import dowel_rows
from bookshelf.model.hardware import hardware_rows
from bookshelf.model.layout import Layout, build_layout
from bookshelf.model.sizes import Sizes, derive
from bookshelf.outputs.cad import view, write_cad
from bookshelf.outputs.diagrams import write_diagrams
from bookshelf.outputs.instructions import write_instructions
from bookshelf.outputs.materials import write_materials
from bookshelf.packing.sheets import pack_materials
from bookshelf.settings import Settings

root = Path(__file__).parent.parent.parent


def build(settings: Settings, out: Path) -> tuple[Sizes, Layout]:
    """Model, check, pack and write every output; raise ValueError on failure."""
    c = settings
    sizes = derive(c)
    layout = build_layout(c, sizes)
    dowels = dowel_rows(c, sizes, layout.parts)
    raise_if(
        [
            *geometry_errors(c, sizes, layout),
            *requirement_errors(c, sizes),
            *dowel_errors(c, sizes, dowels),
        ]
    )

    out.mkdir(exist_ok=True)
    write_cad(c, layout, out)

    rows = hardware_rows(c, sizes, layout.parts, len(layout.units))
    packed = pack_materials(
        layout.parts, sizes.sheets, c.edge_trim, c.kerf, c.max_sheets
    )
    write_materials(
        layout.parts,
        rows.hardware,
        rows.tools,
        out / "materials.md",
        sizes.sheets,
        packed,
        c.kerf,
        c.cut_price,
        c.delivery_price,
    )
    write_diagrams(out / "sheets", packed, sizes.sheets, c.edge_trim)
    write_instructions(
        out / "instructions.md",
        layout.parts,
        rows.hardware,
        c,
        sizes,
        packed,
        rows.pocketed,
        dowels,
    )

    for path in sorted(out.rglob("*")):
        if path.is_file():
            print(path.relative_to(out.parent))
    print("Sheets: " + ", ".join(f"{n} × {m}" for m, n in packed.counts.items()))
    return sizes, layout


def main() -> None:
    """Build into build/; with --view also open the OCP CAD Viewer."""
    c = settings_module.load()
    try:
        _, layout = build(c, root / "build")
    except ValueError as error:
        sys.exit(str(error))
    if "--view" in sys.argv:
        view(c, layout)


if __name__ == "__main__":
    main()
