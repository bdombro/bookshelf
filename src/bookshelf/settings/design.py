"""Design settings: dimensions, layout, limits, cutting and viewer, in cm unless noted.

Inputs: none. Outputs: none; read by settings.load() and passed to the model.
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
dowel_diameter = 0.8
dowel_length = 3.0  # 8 × 30mm; 1.5cm into each panel
dowel_hole_depth = 1.6  # into the side or divider; 1mm deeper than the dowel's share
dowel_end_hole_depth = 1.6  # into the panel's end
dowel_bay_offset = 2  # wide bay's holes sit this much further back than the narrow's
dowel_spacing = (
    15  # max gap between dowels, as for pockets; 2 per end on 28.6cm shelves
)
dowel_clearance = 0.8  # min gap between holes drilled from the divider's two faces
back_screw_spacing = 15  # the back is the main racking resistance
groove_spacing = 5  # V-groove centres on the back sheet; custom order
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
primer_coverage = 12  # m² per litre; label says 9m² per 750ml
top_screws_per_divider = 2  # down through the top
braces_per_end = 2  # corner braces under each end of a cabinet panel
cabinet_top_braces_per_end = 3  # carries the open compartments above
screws_per_brace_leg = 2
kickboard_screws = (
    4  # per wide kickboard, down through the bottom; 30mm into its top edge
)
max_unit_width = 115.6  # measured wall space each side of the fireplace
min_compartment = 29  # clear height; no records or oversized books
hinge_rating = (1.6, 1.9)  # door thicknesses the hinges are rated for
max_sheets = 2  # per material; a 3rd is a cost jump, so raise it deliberately

# --- Layout ---
layout = [["narrow", "wide"], ["wide", "narrow"]]  # units, then bays, left to right

# --- Cutting ---
edge_trim = 0.5  # squaring cut on each edge
kerf = 0.3  # plunge saw width; confirm by cutting an offcut
cut_price = 0  # saw is costed under Tools; 0 shows as €0
delivery_price = 0  # own pickup
mitre_capacity = 35.5  # widest crosscut on the sliding mitre saw, 14"

# --- Viewer ---
hide_doors = False
pine_color = "#E3C08D"  # honey pine
back_color = "#2B2B2B"  # painted black
