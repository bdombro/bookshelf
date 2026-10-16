"""Settings for the bookshelf model, in cm unless noted.

Inputs: none. Outputs: none; read by model.py as config.name.
Implements spec 6.3 (Settings).
"""

# --- Dimensions ---
unit_width = 113.7  # both bays' V-grooves symmetric; up to 115.6 fits the wall
narrow_width = 27.2  # narrow bay, inside; the wide bay takes the rest
height = 213
depth = 29.5  # sides and top; 4 strips plus saw cuts and edge trim across a sheet
pine_thickness = 3.7  # frame: sides, divider, top; measure the sheets
back_thickness = 0.9  # V-groove MDF, inside the frame behind the shelves
kickboard_height = 10
kickboard_setback = 5  # toe recess
cabinet_height = 87  # cabinet top; 1 door + 6 narrow shelves per strip
cabinet_shelf_depth = 22  # leaves room behind the inset doors for hinges
door_gap = 0.3  # between the pair and all round the inset doors
shelves_above_cabinet = 3  # 4 open compartments
narrow_lower_shelves = 1  # below the cabinet top line in narrow units
pocket_spacing = 15  # max gap between pocket screws; 2 per end on 28.6cm shelves
back_screw_spacing = 20
groove_spacing = 10  # V-groove centres on the back sheet
finish_coats = 1
finish_coverage = 11  # m² per litre per coat; label says 16, bare pine soaks up more
hinge_from_door_end = 10  # hinge cup center from door top and bottom
knob_from_door_edge = 4  # knob center from the door's inner edge
knob_from_door_top = 6
sanding_coverage = 5  # m² per sponge, light sand of factory-smooth pine
roller_coverage = 6  # m² per sleeve per coat before it sheds or drags
kit_sleeves = 1  # assumed; the listing doesn't say
thin_pine_thickness = (
    1.8  # bottoms, cabinet tops, shelves, kickboards, doors; stock hinges
)
paint_coats = 1  # over a primer coat
paint_coverage = 12  # m² per litre per coat; label says 9m² per 750ml
primer_coverage = 10  # m² per litre; estimate
top_screws_per_divider = 2  # down through the top
braces_per_end = 2  # corner braces under each end of a cabinet panel

# --- Layout ---
layout = ["narrow", "wide", "fireplace", "wide", "narrow"]
fireplace_width = 60

# --- Sheets and cutting ---
sheet_length = 244
sheet_width = 122
frame_sheet_length = 242  # Strahan 37mm board
frame_sheet_width = 121.5
edge_trim = 0.5  # squaring cut on each edge
kerf = 0.3  # saw width; confirm with the cutter

# --- Prices (€, estimates until quoted) ---
pine_sheet_price = 123.0  # 37mm
back_sheet_price = (
    57.50  # Strahan V-groove MR MDF, 100mm centres, grooved on the long edge
)
cut_price = 0  # own plunge saw; 0 shows as €0
delivery_price = 0  # own pickup
hinge_pack = (8, 18.58)  # (pieces, price); LOOTICH 110° inset, Amazon
knob_pack = (1, 0.0)  # already owned
screw_pack = (50, 7.0)  # 4 × 60mm countersunk; estimate
washer_pack = (100, 0.0)  # M4 flat washers, already owned
plug_pack = (50, 7.99)  # Shiwaki pine, 9.5mm
glue_pack = (1, 12.0)  # 1L bottle
bracket_pack = (1, 0.0)  # homemade
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
paint_pack = (0.75, 20.0)  # (litres, price); GoodHome Liberty black satin, B&Q
primer_pack = (0.75, 15.0)  # MDF primer; estimate, not yet priced
brace_pack = (10, 9.0)  # 40mm corner braces with screws; estimate, not yet priced

# --- Links ---
brush_url = "https://www.screwfix.ie/p/synthetic-paint-brush-3-/173fm"
plug_url = "https://www.amazon.ie/dp/B09P53GBG9"
finish_url = "https://tjomahony.ie/rn-int-varnish-antique-pine-satin-750ml-7536837.html"
roller_url = "https://tjomahony.ie/axus-blonde-100-natural-wool-mini-roller-kit-78axu-rkbln4.html"
sanding_url = "https://www.screwfix.ie/p/bosch-expert-superfine-fine-medium-grit-multi-material-hand-sanding-sponges-97mm-x-67mm-3-pack/421vv"
sleeve_url = "https://tjomahony.ie/axus-blonde-100-natural-wool-mini-sleeve-pack-of-10-4-101mm-78axu-rbln410.html"
hinge_url = "https://www.amazon.ie/dp/B07S52MPYH"
paint_url = "https://www.diy.ie/departments/goodhome-liberty-black-satin-interior-metal-wood-paint-750ml/5036581059460_BQ.prd"

# --- Viewer ---
hide_doors = False
pine_color = "#E3C08D"  # honey pine
back_color = "#2B2B2B"  # painted black
