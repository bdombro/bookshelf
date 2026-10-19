"""CAD outputs: STEP, STL, the front view and the OCP CAD Viewer.

Inputs: the Layout, settings and the build folder.
Outputs: build/bookshelf.step, bookshelf.stl and front.svg; --view shows the model.
Implements spec 6.5 (Outputs).
"""

from pathlib import Path

from build123d import CM, ExportSVG, LineType, export_step, export_stl

from bookshelf.model.layout import Layout
from bookshelf.settings import Settings


def write_cad(settings: Settings, layout: Layout, build: Path) -> None:
    """Write the STEP and STL models and the front elevation."""
    assembly = layout.assembly
    export_step(assembly, build / "bookshelf.step")
    export_stl(assembly, build / "bookshelf.stl")

    center = assembly.bounding_box().center()
    visible, hidden = assembly.project_to_viewport(
        (center.X, -10 * settings.height * CM, center.Z),
        viewport_up=(0, 0, 1),
        look_at=(center.X, 0, center.Z),
    )
    svg = ExportSVG(scale=0.25)
    svg.add_layer("visible")
    svg.add_layer("hidden", line_color=(150, 150, 150), line_type=LineType.ISO_DASH)
    svg.add_shape(visible, layer="visible")
    svg.add_shape(hidden, layer="hidden")
    svg.write(build / "front.svg")


def view(settings: Settings, layout: Layout) -> None:
    """Show the units in the OCP CAD Viewer, doors hidden if set."""
    from ocp_vscode import show

    show(
        [
            child
            for u in layout.units
            for child in u.children
            if not (settings.hide_doors and child.label.startswith("door"))
        ]
    )
