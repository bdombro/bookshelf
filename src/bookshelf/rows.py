"""Rows passed between the model, the packer and the outputs.

Inputs: none. Outputs: Part, Hardware and Placement tuples.
Implements spec 6.1 (Architecture).
"""

from typing import NamedTuple


class Part(NamedTuple):
    label: str  # e.g. "unit_1 / wide shelf_2"
    unit: str  # e.g. "unit_1"
    name: str  # e.g. "shelf"
    unit_type: str  # bay type, "wide" or "narrow", or "frame"
    length: float  # along the grain
    width: float
    thickness: float
    material: str
    bottom: float  # height above the floor
    top: float


class Hardware(NamedTuple):
    item: str
    quantity: float
    use: str  # where it goes, from the model
    product: str
    pack_size: float
    pack_price: float
    url: str


class Placement(NamedTuple):
    part: Part
    sheet: int
    strip: int
    x: float  # along the sheet's length, from the usable area's corner
    y: float  # across the sheet
    strip_width: float


class Dowel(NamedTuple):
    label: str  # the panel's label
    unit: str
    name: str
    unit_type: str  # bay type, "wide" or "narrow"
    height: float  # centre of the holes above the floor
    front: float  # the panel's front edge, from the carcass front
    depth: float  # the panel's depth
    positions: tuple[float, ...]  # hole centres from the carcass front
