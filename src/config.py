"""Settings for the bookshelf model, in cm unless noted.

Inputs: none. Outputs: none; read by model.py as config.name.
Implements spec 6.3 (Settings).
"""

# --- Dimensions ---
wide_width = 83.6  # 78.8cm shelves, 3 per 243cm strip
narrow_width = 32  # 27.2cm shelves; one fits each side's offcut
height = 213
depth = 29.5  # 4 strips plus saw cuts and edge trim across a sheet
pine_thickness = 2.4  # measure the sheets; nominal is often a little under
back_thickness = 0.4
kickboard_height = 10
kickboard_setback = 5  # toe recess
cabinet_height = 87  # cabinet top; 1 door + 6 narrow shelves per strip
cabinet_shelf_depth = 25  # leaves room at the front for hinges
door_gap = 0.4  # between the pair, and split above and below
shelves_above_cabinet = 3  # 4 open compartments
narrow_lower_shelves = 1  # below the cabinet top line in narrow units
pocket_spacing = 15  # max gap between pocket screws; 2 per end on 29.5cm shelves
staple_spacing = 12.5
bolts_per_joint = 4
toggles_per_bracket = 2
finish_coats = 1
finish_coverage = 8  # m² per litre per coat; bare pine soaks up the first coat
hinge_from_door_end = 10  # hinge cup center from door top and bottom
knob_from_door_edge = 4  # knob center from the door's inner edge
knob_from_door_top = 6
sanding_coverage = 5  # m² per sponge, light sand of factory-smooth pine
roller_coverage = 6  # m² per sleeve per coat before it sheds or drags
kit_sleeves = 1  # assumed; the listing doesn't say
thin_pine_thickness = 1.8  # shelves, cabinet shelves, doors, kickboards; stock hinges

# --- Layout ---
layout = ["narrow", "wide", "fireplace", "wide", "narrow"]
fireplace_width = 60

# --- Sheets and cutting ---
sheet_length = 244
sheet_width = 122
edge_trim = 0.5  # squaring cut on each edge
kerf = 0.3  # saw width; confirm with the cutter

# --- Prices (€, estimates until quoted) ---
pine_sheet_price = 98.40
birch_sheet_price = 65.99
cut_price = 0  # own plunge saw; 0 shows as €0
delivery_price = 0  # 0 shows as unknown
hinge_pack = (2, 5.45)  # (pieces, price); Hafele, Screwfix 9205J
knob_pack = (1, 3.0)
pocket_jig_pack = (1, 0.0)  # Gunpla twin jig kit, €18.55, already bought
screw_pack = (100, 0.0)  # 4 × 40mm countersunk wood screws, already owned
washer_pack = (100, 0.0)  # M4 flat washers, already owned
plug_pack = (50, 7.99)  # Shiwaki pine, 9.5mm
staple_pack = (1000, 8.0)
glue_pack = (1, 12.0)  # 1L bottle
bolt_pack = (4, 4.0)
bracket_pack = (1, 4.0)
toggle_pack = (10, 10.0)
finish_pack = (
    0.75,
    21.91,
)  # (litres, price); Ronseal Interior Varnish, TJ O'Mahony sale price
brush_pack = (1, 4.95)  # Screwfix 173FM
sanding_pack = (3, 6.85)  # Screwfix 421VV
roller_pack = (1, 5.65)  # Axus Blonde mini roller kit, sale price
sleeve_pack = (10, 9.72)  # Axus Blonde 101mm sleeves, sale price
thin_pine_sheet_price = 69.68
short_screw_pack = (100, 0.0)  # 4 × 30mm countersunk, for 18mm panels, already owned

# --- Links ---
brush_url = "https://www.screwfix.ie/p/synthetic-paint-brush-3-/173fm"
pocket_jig_url = "https://www.amazon.ie/dp/B0BGWRQYNC"
plug_url = "https://www.amazon.ie/dp/B09P53GBG9"
finish_url = "https://tjomahony.ie/rn-int-varnish-antique-pine-satin-750ml-7536837.html"
roller_url = "https://tjomahony.ie/axus-blonde-100-natural-wool-mini-roller-kit-78axu-rkbln4.html"
sanding_url = "https://www.screwfix.ie/p/bosch-expert-superfine-fine-medium-grit-multi-material-hand-sanding-sponges-97mm-x-67mm-3-pack/421vv"
sleeve_url = "https://tjomahony.ie/axus-blonde-100-natural-wool-mini-sleeve-pack-of-10-4-101mm-78axu-rbln410.html"
hinge_url = "https://www.screwfix.ie/p/hafele-steel-110-soft-close-clip-on-concealed-hinges-64mm-2-pack/9205j"

# --- Viewer ---
hide_doors = False
pine_color = "#E3C08D"  # honey pine
birch_color = "#F1DFC0"  # pale birch
