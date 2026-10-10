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
confirmat_spacing = 12  # max gap between confirmats along a joint
staple_spacing = 12.5
bolts_per_joint = 4
toggles_per_bracket = 2
finish_coats = 2
finish_coverage = 12  # m² per litre per coat
hinge_from_door_end = 10  # hinge cup center from door top and bottom
knob_from_door_edge = 4  # knob center from the door's inner edge
knob_from_door_top = 6

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
cut_price = 1.0  # estimate; Strahan quote pending
delivery_price = 0  # 0 shows as unknown
hinge_pack = (2, 10.0)  # (pieces, price)
knob_pack = (1, 3.0)
confirmat_pack = (100, 12.0)
drill_bit_pack = (1, 10.0)
staple_pack = (1000, 8.0)
glue_pack = (1, 12.0)  # 1L bottle
bolt_pack = (4, 4.0)
bracket_pack = (1, 4.0)
toggle_pack = (10, 10.0)
finish_pack = (1, 15.0)  # (litres, price)

# --- Viewer ---
hide_doors = False
pine_color = "#E3C08D"  # honey pine
birch_color = "#F1DFC0"  # pale birch
