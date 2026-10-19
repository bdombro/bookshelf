# Bookshelf spec

Requirements for an app that generates plans for 2 mirrored laminated pine bookshelves:
what to build, the rules the design follows and why, and what the software must produce.
Figures the build computes (part sizes, heights, sheet counts, cuts, cost) live in
`build/materials.md` and `build/instructions.md`, not here.

All measurements are in centimeters.

## Contents

1. [Overview](#1-overview)
2. [Requirements](#2-requirements)
3. [Furniture design](#3-furniture-design)
4. [Materials and cost](#4-materials-and-cost)
5. [Construction](#5-construction)
6. [Software](#6-software)
7. [Quality](#7-quality)
8. [Decisions](#8-decisions)
9. [Status](#9-status)



## 1. Overview

A parametric 3D model of two laminated pine bookshelves in Build123d, managed with uv.
One build turns the model into everything needed to buy, cut and assemble them.

**At a glance:**

- Two units, one either side of a fireplace wall, mirrored: narrow bay, wide bay |
fireplace | wide bay, narrow bay.
- 213cm tall with a recessed kickboard; 29.5cm deep, inset doors flush with the frame.
- Wide bay: 4 open compartments over a 2-door cabinet with an inside shelf.
- Narrow bay: 6 open compartments, lined up with the wide bay's shelves.
- 37mm laminated pine frame (sides, divider, top); 18mm laminated pine for everything
inside it; 9mm V-groove MDF backs, painted black, screwed in.
- Shelves and bottoms sit on dry dowels, no glue; screws only where hidden. Each unit
is built face down, and comes apart.
- Bought for collection, cut at home with a plunge saw.

**Outputs** (all in `build/`, detailed in [Outputs](#65-outputs)):

- `bookshelf.step` and `bookshelf.stl`: the assembled layout for other tools.
- `front.svg`: front elevation of both units.
- `materials.md`: parts, sheets, hardware and cost.
- `sheets/*.svg`: one cutting diagram per sheet, plus `all.svg` and `all.png` with every
sheet stacked.
- `instructions.md`: step-by-step build with a shelf marking guide.



## 2. Requirements

**Room and use:**

- One unit each side of a 160cm fireplace wall, up to 115.6cm wide each (measured).
- Ceiling clears a unit's ~215cm diagonal, so it can be built face down and stood up.
- Plasterboard wall; the skirting boards come off before install.
- Books only, no records or oversized books: ~30cm clear compartments are enough.
- Closed storage at the bottom of the wide bay; open shelves everywhere else.

**Look:** a chunky built-in: thick honey pine frame, lighter shelves, a black panelled
back, doors flush with the frame.

**Safety:** every unit is anchored to the wall with an anti-tip bracket. Never drop it
from the hardware or instructions.

**Materials and tools:**

- Laminated (edge-glued) solid pine for every visible part, so edges need no banding.
- Grain: every pine part's length runs along the sheet's 244cm length.
- Sheets from one supplier, collected with a vehicle that takes 244 × 122cm sheets.
- Cut at home with a plunge saw on rigid foam, with about 2.6m of joined track; pocket
hole jig and most screws already owned; the tools are listed in
[Tools](#43-tools).
- Sheet yield: with the default settings, no more than 2 sheets of each material.

**Enforced by the build** ([Quality](#7-quality)): unit width within the wall, compartment
height, door thickness within the hinge rating, and the sheet limit, each a setting.

**Flexible sizes:** any dimension can change when that makes building, cutting or buying
simpler. Most sizes were picked for sheet yield or V-groove symmetry.

**Not modeled:** hardware, finish, and wall cutouts for sockets or switches (cut by hand
during install).



## 3. Furniture design

### 3.1 Layout

A left unit (narrow bay, wide bay) and a mirrored right unit (wide bay, narrow bay), with
the wide bays next to the fireplace. Each unit is one carcass: two outer sides and a
divider between the bays, under one full-width top.

### 3.2 Frame and bays

The frame (sides, divider, top) is 37mm pine. Everything inside it is 18mm: lighter
shelves in a heavier frame, and doors that suit stock inset hinges.

- **Unit width:** 113.7cm, the widest under 115.6cm where the back's 5cm V-groove
centres fall symmetrically in both bays (bay centres a multiple of half the groove
spacing apart). That offset depends only on the unit width, not the split between bays.
- **Narrow bay:** 27.2cm inside, 6 open compartments, no doors.
- **Wide bay:** the rest of the unit width; three of its shelves must still fit end to
end on one 243cm strip. 4 open compartments over a 2-door cabinet with one inside shelf.
- **Top:** between the outer sides, full depth, over the divider and the back.
- **Divider:** floor to the top's underside, at shelf depth, so the back runs behind it
in one piece.
- **Depth:** sides and top 29.5cm, so 4 strips plus saw cuts and edge trim fit across a
sheet. Shelves, bottoms and the divider are the back's thickness shallower, so the back
sits inside the frame.
- **Bottom:** an 18mm panel per bay, resting on its kickboard. A thicker bottom adds
weight, not strength; the screwed back keeps the base square.
- **Kickboard:** one per bay between the side and divider, set back 5cm for a toe recess;
the sides and divider run to the floor.
- **Shelves:** fixed, not adjustable, on dry dowels (no glue) at both ends. An 18mm shelf across the wide bay must sag under
the usual 1.3mm visible limit with a full load of books (20 lb/ft, ends simply
supported); the screwed back stiffens it further. Creep may roughly
double sag over years.

### 3.3 Heights

Measured from the floor. The marking table for each panel is generated in
`instructions.md`.

- Cabinet top at 87cm, close to a built-in's usual 85–90cm, and chosen so a door and 6
narrow shelves share one strip.
- Shelves above the cabinet top are evenly spaced up to the top, at the same heights in
both bays, so shelf lines run straight across a unit.
- The narrow bay has a shelf level with the wide bay's cabinet top, and one more shelf
evenly spaced below it.
- The wide bay's cabinet shelf sits at the narrow bay's lower shelf height. It's 22cm
deep against the back, leaving room at the front for the closed doors and hinge cups.

### 3.4 Doors

Wide bay only, a pair. Inset: inside the opening between the outer side, the divider,
the bottom and the cabinet top, faces flush with the frame's front, so the full 3.7cm
frame shows all round. A 0.3cm gap all round and between the pair. Grain vertical, 2
soft-close inset concealed hinges and one knob each; the hinges set the closed position,
so no stop is needed. Inset shows any out-of-square frame as a tapering gap, so the
carcass is squared before hanging and the hinges' adjustment evens the gaps.

### 3.5 Backs

9mm moisture-resistant MDF, V-grooved at 50mm centres (a custom order) along the sheet's length, so the
grooves run vertically. One per unit: between the outer sides, under the top, from the
floor behind the kickboards. Each is cut from its sheet so the grooves are symmetric in
both bays; the sheet is wider than the back, so the cut can always be placed, and the
grooves are measured at pickup. Primed and painted black before assembly. Screwed, not
glued, every 15cm into the rear edges of the divider and every horizontal panel: it's
the main racking resistance, and it can come off later. The frame hides its edges.



## 4. Materials and cost

What each material and item must be. The chosen products, sheet sizes, pack sizes,
prices and links are settings in `src/bookshelf/settings/catalog.py`; counts, packs and cost are generated
in `build/materials.md`. Prices are estimates until replaced with quotes.

### 4.1 Sheets

- **37mm laminated pine:** sides, divider, top.
- **18mm laminated pine:** bottoms, cabinet tops, shelves, cabinet shelves, kickboards,
doors.
- **9mm V-groove moisture-resistant MDF,** grooved along the sheet's length at 50mm
centres: backs.

Usable area is 1cm less each way after 0.5cm is trimmed off each edge for squaring.
Nominal thicknesses are often a little under, so measure the sheets and set the
thickness settings to match.

### 4.2 Hardware and finish

| Item | Requirement |
| ---- | ----------- |
| Hinges | soft-close inset concealed, rated for the door thickness (checked), with a drilling template |
| Dowels | 8mm fluted wooden, for every horizontal panel between a side and the divider; dry, no glue |
| Pocket screws, 18mm panels | narrow bottoms and narrow kickboards only, on hidden faces; black pan head, so no washer; short enough that the tip can't break out through a side's face |
| Long screws, 37mm top | long enough for the top's pockets and to go down through it into each divider; countersunk on washers |
| Kickboard screws | wide kickboards: countersunk, down through the bottom into the kickboard's top edge, from inside the cabinet |
| Back screws | countersunk, through the back every 15cm |
| Corner braces | on top of each end of the wide bottom and under each end of the cabinet top, inside the cabinet; short screws into the panel |
| Anti-tip brackets | one per unit; wall fixings from spares |
| Varnish | clear or tinted, water-based, satin; one coat, both faces |
| Primer and paint | grey primer, then black satin, one coat each on the backs |
| Roller, sleeves, brush, sponges | wool mini roller for varnish and paint, a synthetic brush for tipping off and edges, sponges for a light sand |

### 4.3 Tools

What each must do; tools bought for the project are costed in the Tools line, owned ones are €0, and all are listed in `materials.md`.

| Tool | Requirement |
| ---- | ----------- |
| Plunge saw, rails and blade | about 2.6m of joined rails for the full-length rips; a blade whose kerf matches the `kerf` setting |
| Pocket hole jig | pockets in 37mm and 18mm pine |
| Drill/driver | 8mm brad-point bit with a depth stop |
| Dowel jig | self-centring and centre-marked, centres 8mm holes in panel ends |
| Clamps | a couple to prop a side on its edge, plus clamping panels on their lines |
| Corner clamps | right-angle clamps to hold a panel square to the side during assembly |
| T-square | for squaring and marking across the panels |
| Tape measure | |
| Stud finder | for the anti-tip brackets |

### 4.4 Cost

`materials.md` totals sheets, cutting, hardware and finish, tools, and delivery. Cutting and
delivery are €0: the plunge saw is costed under Tools, pickup is our own.



## 5. Construction

What `instructions.md` must cover, in order. Each unit weighs roughly 75kg assembled, so
it's built in its room.

- **Cutting:** rip strips with the plunge saw, then crosscut each, on the mitre saw where the strip fits its capacity, following the cutting list and sheet
diagrams. Sheets on rigid foam, cut lines taped or scored against splintering. Check the
blade width against the `kerf` setting first.
- **Finishing:** sand and finish every face and edge of the panels flat before assembly; nothing is
glued, so nothing is taped off. Laminated pine blotches under
stain, so a clear or tinted water-based varnish, one coat, both faces equally so panels
don't cup. Raise the grain and sand 240 first; roll, then tip off at once along the grain
with a near-dry brush, and never rework areas that have started to set. Backs: one coat
of grey primer, then one of black satin, brushed into the grooves first, then rolled.
Bare MDF soaks up paint, so black alone won't cover.
- **Joinery:** dry dowels (8 × 30mm, no glue) locate every horizontal panel between a
side and the divider: shelves, bottoms, cabinet tops and cabinet shelves. Per end,
`max(2, ceil(depth / spacing))` dowels, measured from the carcass front (the cabinet
shelf sits back, so its offset is added). The wide bay's holes sit further back than the
narrow bay's, so holes from both faces of the divider at one height never meet. Panel
ends are drilled with a self-centring jig; the sides and divider are marked with centre
points, pressing each panel on its pencilled line with the front edges flush, and
drilled with a depth stop. A snug hand-pressed fit, tested on an offcut, holes a little
deeper than the dowel's share, edges chamfered. Screws only where hidden and tying the
carcass: the top (pocket screws, plus long screws down into each divider), the narrow
bay's bottom (pockets on its underside) and the narrow kickboards (pockets on their back face).
The wide kickboard is screwed down through the wide bottom into its top edge, from
inside the cabinet. Inside the cabinet, hidden by the doors, the wide bottom and cabinet top also sit on corner
braces (2 per end on top of the bottom, 3 under the cabinet top, which carries the
compartments above), set back so the doors and hinges clear them. Clamp each panel on
its line while driving. No dados.
- **Assembly:** face down on the front edges, since every panel is flush at the front, so
nothing turns over before the back is screwed on: prop one side on its edge with clamped
blocks, fit the first bay's horizontals (kickboard on spacer blocks), slide on the
divider, fit the second bay's, the other side, then the top.
- **Backs:** square each frame by its diagonals, drop the back in, and screw it every
15cm along the shelf and divider lines, pencilled on the back first. Then stand the unit
up and fit the corner braces through the cabinet opening; the wide bay's kickboard goes on last, screwed down through the bottom.
- **Doors:** hinges and doors, evening the gaps with the hinges'
adjustment.
- **Install:** remove the skirting boards. Tilt each unit up with at least two people.
Fix its anti-tip bracket through the top into a stud wherever possible, using spring or
snap toggles where there's no stud, never plain plugs.



## 6. Software

### 6.1 Architecture

A uv app (Python 3.12) with one package, `src/bookshelf/`, and a justfile. Generated
files go in `build/`; only `materials.md` and `instructions.md` are committed, so every
change's effect on the cut list, cost and instructions shows in the diff. Each module has
one job and a short docstring; the folders:

- `settings/`: every value a person would change. `design.py`: dimensions, layout,
limits, cutting, viewer. `catalog.py`: sheets and products with prices and links. Plain
lowercase values, no logic; `load()` gathers them into one namespace with optional
overrides, so tests can change a single value.
- `model/`: `sizes.py` (derived sizes), `unit.py` (one unit's panels), `layout.py`
(units placed, `Part` rows), `checks.py` (model and requirement checks), `hardware.py`
(counts and products), `dowels.py` (dowel positions).
- `packing/`: `packer.py` (strips, ordering search, self-check), `sheets.py` (each
material packed, sheet limit).
- `outputs/`: `cad.py` (STEP, STL, front view, viewer), `materials.py`, `diagrams.py`
(sheet SVGs), `instructions.py` with `templates/instructions.md.j2`.
- `rows.py`: the `Part`, `Hardware` and `Placement` rows. `text.py`: number formatting.
`build.py`: the entry point.

**Data flow:** `build.py` loads the settings, derives sizes, builds the layout, runs the
checks, then writes the CAD files, packs the sheets and writes `materials.md`, diagrams
and `instructions.md`. Every function takes the settings or values from them as
arguments and nothing below `settings/` imports it, so any value can be overridden.
Only `model/` and `outputs/cad.py` import Build123d; packing and text outputs work from
`Part` and `Hardware` rows.

### 6.2 Commands

- `just build`: runs `bookshelf.build`, writing everything to `build/`, then renders
`sheets/all.png` with `rsvg-convert` (librsvg).
- `just check`: ruff format and lint, basedpyright (standard mode), `typos`, `just
--fmt`, and pytest. Tool settings live in `pyproject.toml`.
- `just view`: builds and opens the model in the OCP CAD Viewer.

### 6.3 Settings

`src/bookshelf/settings/`, grouped under banner comments in `design.py` and
`catalog.py`:

- **Dimensions:** unit width, narrow bay width, height, depth, pine and back thickness,
kickboard, cabinet height and shelf depth, door gap, shelf counts, V-groove spacing,
screw and dowel spacing, dowel size and hole depths, hinge and knob positions, finish coats and coverage, and the limits the
build enforces (wall width, compartment height).
- **Layout:** units left to right, each its bays left to right, e.g.
`[["narrow", "wide"], ["wide", "narrow"]]`.
- **Sheets:** one tuple per material: length, width, price, link; and the sheet limit.
- **Cutting:** edge trim, kerf, cutting and delivery prices.
- **Hardware and finish:** one tuple per item: product, pack size, pack price, link; and
the hinge rating.
- **Tools:** the same tuple per tool, price 0 when owned.
- **Viewer:** `hide_doors`, and pine and back colours for the viewer and STEP file.

Derived sizes (wide bay width, shelf heights, door sizes) and hardware counts are
computed in `model/`, never repeated as settings or literals.

### 6.4 Model

- **Units:** Build123d is mm by convention and STEP/STL readers assume mm, so settings
are multiplied by `CM` when building.
- **Unit origin:** floor, front-left corner of the carcass. X width, Y depth, Z height.
- **Layout:** origin at the left end of the left unit; each unit starts a fixed 60cm
after the last. The gap only spaces the drawings, so it isn't a setting. Parts are labeled under their unit and bay, e.g.
`unit_1 / wide shelf_2`; frame parts have no bay (`unit_1 / divider_1`).
- **Assembly:** one labeled `Compound`, not fused, so each panel stays separate.
- **Checks** run before exports and exit with a clear message, so a bad model never
reaches `build/`.
- **Viewing:** `--view` shows it in the OCP CAD Viewer; `hide_doors` hides the
doors to see inside the cabinets.

### 6.5 Outputs

All overwrite `build/` on every run, and each path is printed.

`bookshelf.step` / `bookshelf.stl`: the named, coloured assembly for other CAD tools, and
a mesh for quick previews.

`front.svg`: front elevation of both units, projected from
straight in front; visible edges solid, hidden edges dashed on their own layer.

`materials.md`, written by `outputs/materials.py`:

- **Parts:** name, unit type, quantity across all units, length × width, thickness,
material. Identical panels grouped. Sizes from each part's bounding box, rounded to
0.1cm.
- **Sheets to buy:** per material: linked name, sheet size, count, share of area used,
price.
- **Hardware and finish:** counts derived from the parts and layout, with packs to buy
and cost:
  - hinges and knobs per door; 2 pockets per end of the top, narrow bottoms and
  kickboards, one screw each, washers for the long screws; 2 long screws per divider;
  - dowels: `max(2, ceil(depth / spacing))` per end of every dowelled panel;
  - corner braces per end of the cabinet's bottom and cabinet top, with a short screw
  and a side screw per brace;
  - back screws: rear edge length ÷ spacing plus one, per edge;
  - one anti-tip bracket per unit;
  - varnish litres = both faces of every pine part × coats ÷ coverage, then whole cans;
  - sanding sponges = that area ÷ coverage per sponge, rounded up;
  - roller sleeves = that area × coats ÷ coverage per sleeve, rounded up, less the one
  in the kit;
  - primer and black paint litres = the backs' front face × coats ÷ coverage, then whole
  cans.
- **Tools:** item, product, cost; owned tools show €0.00.
- **Cost:** sheets, cutting (with the cut count), hardware and finish, tools, delivery, total,
labeled estimates. A price of 0 shows as €0.00 (owned), own plunge saw, or own pickup.
- **Saw width warning:** ⚠️ under the sheet count and the cost, stating the assumed kerf
and to confirm it before cutting.

`sheets/*.svg`, from the same packing: each part's position, label, size and a grain
arrow; offcuts blank. `all.svg` stacks every sheet top to bottom. Plain SVG text.

`instructions.md`, written by `outputs/instructions.py` from a Jinja2 Markdown template, the prose in the
template and the model's numbers computed in Python.
Ordered steps, each listing the parts and hardware it uses:

1. **Cut:** per sheet, the strips to rip and parts to crosscut from each, in order, with
an extra rip for a part narrower than its strip and a link to the sheet's diagram. Saw
setup. Where to place each back's cut against the grooves.
2. **Check and label:** count panels against the parts table, then pencil each part's
label on an edge that will be hidden.
3. **Sand and finish** every face and edge; nothing is taped off.
4. **Mark shelf lines:** a table per bay of each horizontal panel's top and underside
from the floor. Each bay's outer side and the divider's matching face are marked
together, as mirror images. Fixed shelves leave no room for error, so this is the core
of the document.
5. **Drill dowel and pocket holes:** a position table per bay from the carcass front; panel
ends with the jig, sides and divider marked from the table, with a depth stop; pocket holes
only in the top, narrow bottoms and kickboards.
6. **Assemble each carcass** in its room, face down: side, first bay, divider, second bay,
other side, top.
7. **Square and fix the back:** the diagonal to match, then screw positions.
8. **Stand up and fit the corner braces,** then the wide bay's kickboard.
9. **Hinges and doors:** hinge cup and plate positions, knob position, adjusting the gaps.
10. **Anchor:** fix the anti-tip brackets.

Finish product instructions and wall cutouts are left out.

### 6.6 Packing

How `packing/` turns part rows into sheets and a cutting list.

- **Method:** pack the way a panel saw cuts: rip strips across the sheet, crosscut parts
from each strip, a kerf per cut, inside each material's usable area. Each part's length
runs along the sheet's length.
- **Offcuts:** a part goes into an existing strip's leftover length when it's no wider
than the strip.
- **Shared sheets:** parts from all units share sheets, grouped by material, each with
its own sheet size.
- **Search:** a single greedy pass can miss the best layout, so the packer tries several
part orderings and keeps the one with the fewest sheets.



## 7. Quality

What the app verifies on every build.

- **Model checks** in `model/checks.py`, before any export:
  - the layout's bounding box is the unit widths plus the gaps, by depth, by height;
  - every unit is `unit_width` wide;
  - every bay's centre falls on the V-groove pattern (a groove or midway between two);
  - no two panels overlap;
  - every panel fits its usable sheet with its length along the grain;
  - dowels: the holes are at least as deep as the dowel is long, shallower than the
  frame, inside their panel, and holes drilled from the divider's two faces at one
  height stay `dowel_clearance` apart.
- **Requirement checks** from [Requirements](#2-requirements), before any export:
  - unit width within the wall (`max_unit_width`);
  - every compartment at least `min_compartment` clear;
  - door thickness within the hinge rating (`hinge_rating`).
- **Sheet limit:** after packing and before writing, no material needs more than
`max_sheets`. Raise it only as a deliberate cost decision.
- **Packer self-check:** every part placed exactly once, within the usable area, no
overlaps, a kerf between neighbors; otherwise the build fails. A wrong cutting list is
the costliest bug here.
- **Tests** (`tests/`): the packer's self-check rejects each kind of broken layout, a
part longer than any sheet fails clearly, and each model, requirement and sheet-limit
check fails on settings that break it, with actual and expected values. One test builds
the defaults cleanly. Output text is covered by the committed output diff.
- **Messages** show actual and expected values, e.g. "unit_1 width 115.6, expected 113.7".



## 8. Decisions

Options considered and why they lost. Newest first within each group.

**Material:**

- 24mm pine frame, 18mm insides, glued and stapled 3.2mm hardboard backs: the 37mm frame
looks chunkier and needs only 2 frame sheets once the bottoms and cabinet tops are 18mm;
the V-groove back adds a panelled look.
- 37mm bottoms and cabinet tops: heavier, no structural gain.
- Laminated red deal stair treads for the frame: crosscuts only, but 27cm deep, redder,
possibly nosed.
- Pre-cut 37mm pine shelf boards (220 × 37 × 890mm): too short and narrow for the frame.
- 225mm PAO pine planks instead of sheets: too shallow for the shelves; two glued
boards per panel erode the saving.
- 3.2mm hardboard backs painted black: V-groove MDF looks far better behind black, is
stiffer, and comes from the same supplier as the pine.
- 12mm V-groove: heavier and dearer, no gain at this size.
- 100mm groove centres (Strahan stock): 50mm gives a finer panelled look; same unit width stays symmetric.
- Glued backs: screws alone resist racking, need no taping off, and let the back come
off. Pocket holes in the back: 9mm is under the jig's minimum.
- Rebated back: shallower shelves get the same result with no router.
- Crown Quick Dry white primer: GoodHome grey is better reviewed and hides better under
black.
- Two coats of black on the backs: primer plus one coat covers better for less.
- All 24mm pine: 24mm doors are past every affordable concealed hinge's rating.
- 18mm for hidden parts only: mixes thicknesses where open shelves show.
- 18mm pine for everything: cheaper and lighter, but a slimmer look.
- Thin nailed-on or inset 18mm backs, 4mm birch, 4mm poplar, 6mm birch, 12mm pine, red
deal tongue and groove, hardwood ply, pine ply, white-faced hardboard: cost, colour,
racking resistance or paint grip each ruled them out before the V-groove MDF.
- 18mm plywood frames (the original spec): laminated pine's solid edges need no banding.
MDF sags under books.
- Strahan cutting the sheets on their panel saw (~€75): a plunge saw at home saves it.

**Dimensions:**

- 115.6cm units: fill the wall, but the back's grooves sat 0.95cm off centre in the wide
bay; the next symmetric width up, 123.7cm, doesn't fit. Strahan's custom groove centres
were the alternative.
- Cabinet top at 90cm: the longer doors no longer share a strip with six narrow shelves,
costing an extra sheet.
- Cabinet top at 76cm (desk height): 87cm gives a taller, more built-in cabinet at the
same sheet count.
- 88cm shelves: only two per strip, costing extra sheets.
- 26.4cm narrow shelves: tight for books.
- 30cm depth: 4 strips needed 121.9cm of a 122cm sheet; 29.5cm leaves margin for trim.

**Layout and features:**

- Pocket screws and plugs on the open shelves: the pockets show on the underside, and the
plugs show too; dry dowels leave nothing visible.
- Glued dowels: a glue-up race with many joints at once, squeeze-out on finished panels,
and a carcass that can't come apart. Dry dowels hold square, and the back and top screws
tie the carcass.
- Assembling on its side: turning a loose carcass face down to fit the back.
- Assembling on its back: the fronts don't self-align and the back can't go on without
flipping it.
- Iron brackets under every shelf, or visible retro brackets on the wide shelves:
bolder and stiffer, but busy and dearer than pocket screws; reverted to pocket screws.
- Adjustable shelves on pins above the cabinet: visible pin holes and fewer fixing points
for the back.
- 4 braces per end everywhere: the back's screws are the main racking resistance; only
the cabinet top went to 3 per end and the back screws to every 15cm.
- Corner braces under the cabinet shelf: it's lightly loaded and sits on dowels instead.
- Pocket screws inside the cabinet: braces are quicker, need no jig, and the doors hide
them.
- Full overlay doors: cheaper and forgiving of an out-of-square frame, but hid most of
the 37mm frame's edge and stood 1.8cm proud.
- Four separate units bolted in two sets: one carcass per side drops two sides, the bolts
and a doubled 4.8cm line, and gives one back per unit.
- One row of four bolted units, shared sides: superseded by one carcass per side.
- Blum inset hinges (Screwfix): local and a stronger brand, but much dearer with far fewer
reviews. Hettich Sensys and LOOTICH overlay: superseded by inset doors.
- Dropping the cabinet shelves: saves nothing, they come from an otherwise spare strip.
- Push-to-open latches: don't work with soft-close hinges.
- Skirting notches: the skirting is removed instead.
- Hanging strip: anti-tip brackets through the top instead.
- Bought anti-tip brackets and toggles: brackets are homemade, fixings from spares.

**Finish and hardware:**

- Corner braces under the wide bottom: unreachable once the unit is assembled; now on top, fitted through the cabinet opening.
- Pocket-holed wide kickboard: its pockets are enclosed by the back; screwed down through the bottom instead.
- Owned countersunk 4 × 30mm screws on washers in the 18mm pockets: black pan heads sit
flat without washers. A 45mm Jyvex is too short for the 37mm top, so those stay 60mm
countersunk on washers.
- Confirmat screws: heads show on every outer side.
- Two coats of varnish: one coat saves time and cans; add a second on shelf tops and
doors if they mark.
- 8m²/L varnish coverage: too cautious against the label's 16m²/L; 11m²/L is used.

**Software:**

- Fireplace width setting and a `"fireplace"` layout entry: nothing built depends on the
gap, so it's a fixed drawing constant and the layout lists units directly.
- Separate price, pack and link settings per item, and product names in the model: one
tuple per product in `catalog.py` makes a swap one edit.
- Sheet limit, wall width and hinge rating as review rules only: easy to forget; now
build checks.
- Four files only, `unit()` as the only function, no `main()`, a plain folder and not a
package: agent-invented limits that kept code from being organized by job; modules and
folders now follow what each does.
- Scripts at the repo root: cluttered; moved to `src/`.
- UPPER_CASE constants, or frozen settings dataclasses: plain lowercase settings modules
are simpler for a person to edit.
- A packing library (e.g. rectpack): no panel-saw strip order for the cutting list.
- No unit tests: nothing proved the self-check rejects a bad layout. Broader unit tests:
would repeat the model checks and the output diff.
- Ignoring all of `build/`: output changes were invisible in review.
- Bare tuples or dicts between scripts: untyped; replaced by `NamedTuple` rows in
`rows.py`.
- basedpyright strict, ruff `D` and `PL`, mypy: noisy or redundant.
- pre-commit, Markdown formatters: extra tooling; formatters rewrap the spec.
- ImageMagick for `all.png`: drops outlines and the grain arrow; librsvg instead.
- PNG front view: SVG needs no extra dependency and scales cleanly.



## 9. Status

Progress: ⬜ unblocked · 🛑 blocked · 🔄 in progress · ✅ done · ❓ undecided · ⏸️ paused · 🚫 not doing

- ✅ Design confirmed
- ✅ Setup and justfile ([6.2](#62-commands))
- ✅ Settings and model ([6.3](#63-settings), [6.4](#64-model))
- ✅ Model checks ([7](#7-quality))
- ✅ STEP, STL and front view ([6.5](#65-outputs))
- ✅ Packing, packer tests and material spec ([6.6](#66-packing), [7](#7-quality), [6.5](#65-outputs))
- ✅ Sheet diagrams ([6.5](#65-outputs))
- ✅ Assembly instructions ([6.5](#65-outputs))
- ✅ Two units with a 37mm frame and V-groove backs ([3](#3-furniture-design))
- ✅ Corner braces inside the cabinet ([5](#5-construction))
- ✅ Inset doors ([3.4](#34-doors))
- ✅ Symmetric V-grooves: 113.7cm units ([3.2](#32-frame-and-bays))
- ✅ Spec rewritten as requirements ([Contents](#contents))
- ✅ Requirement checks, one setting per product ([7](#7-quality), [6.3](#63-settings))
- ✅ Code split into settings, model, packing and outputs; check tests; instruction template ([6.1](#61-architecture), [7](#7-quality))
- ✅ Dry dowels and face-down assembly ([3.2](#32-frame-and-bays), [5](#5-construction), [4.3](#43-tools))
- ✅ Tools bought, wide bottom braces on top, screwed wide kickboard ([4.3](#43-tools), [5](#5-construction))
- ⬜ Real prices: saw width, hardware, long screws, corner braces, 50mm V-groove quote ([4](#4-materials-and-cost))
