# Bookshelf spec

A spec for an application that generates plans for making 2 mirrored bookshelves.

What this project builds, why each choice was made, and how the code produces it. This
describes the current design; when something changes, update the section it belongs to
and log the old option under [Decisions](#8-decisions).

All measurements are in centimeters.

## Contents

1. [Overview](#1-overview)
2. [Requirements and constraints](#2-requirements-and-constraints)
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

- Two units, one either side of a 160cm fireplace wall, mirrored: narrow bay, wide bay |
fireplace | wide bay, narrow bay. Each unit is 113.7cm wide, so the back's V-grooves sit
symmetrically in both bays; 387.4cm overall.
- Every unit is 213cm tall with a recessed 10cm kickboard. Sides and top are 29.5cm deep;
shelves and divider 28.6cm, with the back set in behind them. The cabinet doors are
inset, flush with the frame.
- Wide bay (75.4cm inside): 4 open compartments over a 2-door cabinet with an inside
shelf.
- Narrow bay (27.2cm inside): 6 open compartments, lined up with the wide bay's shelves.
- 37mm laminated pine frame (two sides, a divider, the top); 18mm laminated pine bottoms,
cabinet tops, shelves, cabinet shelves, doors and kickboards; 9mm V-groove MDF backs,
primed and painted black, screwed in.
- Estimated cost ~€716, all collected: 2 × 37mm pine, 2 × 18mm pine and 2 V-groove MDF
sheets €500.36, cut at home with a plunge saw, hardware and finish ~€215.

**Outputs** (all in `build/`, detailed in [Outputs](#65-outputs)):

- `bookshelf.step` and `bookshelf.stl`: the assembled layout for other tools.
- `front.svg`: front elevation of both units.
- `materials.md`: parts, sheets, hardware and cost.
- `sheets/*.svg`: one cutting diagram per sheet, plus `all.svg` with every sheet stacked
vertically and `all.png` rendered from it.
- `instructions.md`: step-by-step assembly with a shelf marking guide.



## 2. Requirements and constraints

- **Room:** a 160cm fireplace wall with one unit on each side. Up to 115.6cm per unit fits
(confirmed by the owner). Ceiling must clear ~215cm to tilt a unit upright. Plasterboard wall; skirting boards come off before install.
No records or oversized books, so ~30cm compartments are enough. The fireplace's
clearance is fine.
- **Sheets:** standard Irish 244 × 122cm; Strahan's 37mm pine board is 242 × 121.5cm.
Usable area is 1cm less each way after 0.5cm is trimmed off each edge for squaring.
- **Grain:** laminated pine's strips run along the sheet's 244cm length. Every pine part
keeps its length along them: sides, divider and doors vertical, shelves the long way.
- **Saw width:** `config.kerf` setting, 0.3cm; plunge saw blades cut 0.22–0.28cm; the
layout fits either way.
- **Flexible sizes:** exact dimensions can change whenever that makes building, cutting
or buying simpler. Most sizes below were picked for sheet yield.
- **Not modeled:** hardware, wall cutouts for sockets or switches (cut by hand during
install), finish.



## 3. Furniture design



### 3.1 Layout

A left unit (narrow bay, wide bay) and a mirrored right unit (wide bay, narrow bay), with
the wide bays next to the fireplace wall. Each unit is 113.7cm; the layout is 2 × 113.7 +
160 = 387.4cm. Each unit is one carcass: two outer sides and a divider between the bays,
all 37mm, under one full-width top.

### 3.2 Frame and bays

The frame (sides, divider, top) is 37mm pine, for a chunky built-in look. Everything
inside it is 18mm: lighter shelves inside a heavier frame, and doors that suit stock
inset concealed hinges.

- **Top:** 106.3cm between the outer sides, full 29.5cm depth, over the divider and the
back. The divider stops under it.
- **Divider:** floor to the top's underside, 28.6cm deep, so the back runs behind it in
one piece.
- **Wide bay (75.4cm inside):** what's left of 113.7cm after three 3.7cm verticals and the
narrow bay; three shelves still fit end to end on a 243cm strip.
- **Unit width:** 113.7cm, picked so the back's 10cm V-groove centres fall symmetrically in
both bays: the bay centres are 55cm apart, a multiple of half the groove spacing. The
offset between them depends only on the unit width, not the split between bays. At 115.6cm
the wide bay was 0.95cm off; the next symmetric width up, 123.7cm, doesn't fit. 4 open compartments over
a 2-door cabinet with one inside shelf.
- **Narrow bay (27.2cm inside):** 6 open compartments, no doors.
- **Bottom:** an 18mm panel per bay on its kickboard, fixed to the side and divider:
pocket-screwed in the narrow bay, on corner braces in the wide bay's cabinet. A 37mm bottom would add weight, not strength; the screwed back keeps the base
square.
- **Depth:** sides and top are 29.5cm, so four strips plus saw cuts and edge trim fit
across a sheet. Shelves, bottoms and the divider are 28.6cm, leaving the rear 0.9cm for
the back, inside the frame. The inset doors add nothing at the front.
- **Shelves:** all fixed. A 75.4cm span of 18mm pine sags under 1mm under a full shelf of
books (20 lb/ft, ends simply supported), under the usual 1.3mm visible limit; screwed ends
and the screwed back stiffen it further. Creep may roughly double it over years.
- **Kickboard:** one per bay between the side and divider, set back 5cm for a toe recess;
the bottom rests on it and the sides and divider run to the floor.

### 3.3 Heights

Measured from the floor (the bottom of the sides). Both bays share every height from the
cabinet top up, so shelf lines run straight across a unit. The narrow bay's shelf at the
cabinet line is level with the wide bay's cabinet top; both are 18mm.


| Panel               | Wide bay                 | Narrow bay  |
| ------------------- | ------------------------ | ----------- |
| Kickboard           | 0–10                     | 0–10        |
| Bottom              | 10–11.8                  | 10–11.8     |
| Lower shelf         | cabinet shelf, 47.6–49.4 | 47.6–49.4   |
| Cabinet top / shelf | 85.2–87                  | 85.2–87     |
| Shelf               | 116.2–118                | 116.2–118   |
| Shelf               | 147.3–149.1              | 147.3–149.1 |
| Shelf               | 178.3–180.1              | 178.3–180.1 |
| Top                 | 209.3–213                | 209.3–213   |


The cabinet top is at 87cm, close to a built-in's usual 85–90cm. Compartments are ~29.2cm
clear above the cabinet top and ~35.8cm below it in the narrow bay. The wide bay's
cabinet shelf is 22cm deep against the back, leaving ~6.6cm at the front: 1.8cm for the
closed doors and the rest for the hinge cups.

### 3.4 Doors

Wide bay only. Inset: the pair sits inside the opening between the outer side, the
divider, the bottom and the cabinet top, faces flush with the frame's front, so the full
3.7cm frame shows all round. A 0.3cm gap all round and between the pair (`door_gap`),
from 12.1cm to 84.9cm. Each is 37.3 × 72.8 × 1.8cm, grain vertical, on 2 soft-close
inset concealed hinges with one knob; the hinges set the closed position, so no stop is
needed. Inset shows any out-of-square frame as a tapering gap: square the carcass before
hanging, and use the hinges' adjustment to even the gaps.

### 3.5 Backs

9mm moisture-resistant MDF, V-grooved at 100mm centres along the sheet's length, so the
grooves run vertically. One per unit, 106.3 × 209.3cm: between the outer sides, under the
top, from the floor behind the kickboards. Each is cut from its sheet so a groove sits
8.6cm in from the edge on the narrow bay's side: the narrow bay shows two grooves with
8.6cm strips at each side, the wide bay seven with a groove at its centre and 7.7cm
strips at each side, and one groove hides behind the divider. The 122cm sheet leaves
~14cm of slack, so the cut can always be placed; measure the sheet's grooves at pickup. Primed and given one coat of black satin flat,
before assembly. Screwed (no glue) through countersunk holes into the rear edges of the
divider, bottoms, cabinet top, cabinet shelf and every shelf, every 20cm; it keeps the
frame square and can come off later. Its edges are hidden by the frame.

### 3.6 Panel list

Per unit. Sides, divider and top are 3.7cm thick; everything else pine is 1.8cm.


| Part                | Frame             | Wide bay         | Narrow bay       |
| ------------------- | ----------------- | ---------------- | ---------------- |
| Sides               | 2 × 213 × 29.5    |                  |                  |
| Divider             | 1 × 209.3 × 28.6  |                  |                  |
| Top                 | 1 × 106.3 × 29.5  |                  |                  |
| Bottom              |                   | 1 × 75.4 × 28.6  | 1 × 27.2 × 28.6  |
| Cabinet top         |                   | 1 × 75.4 × 28.6  | –                |
| Shelves             |                   | 3 × 75.4 × 28.6  | 5 × 27.2 × 28.6  |
| Cabinet shelf       |                   | 1 × 75.4 × 22    | –                |
| Kickboard           |                   | 1 × 75.4 × 10    | 1 × 27.2 × 10    |
| Doors               |                   | 2 × 37.3 × 72.8  | –                |
| Back (9mm V-groove) | 1 × 106.3 × 209.3 |                  |                  |




## 4. Materials and cost

Expected figures with the defaults. Exact counts come from `build/materials.md`.

### 4.1 Sheets

- 37mm laminated (edge-glued) solid pine, 242 × 121.5cm, €123: 2 sheets, about 74% used
(one 29.5cm strip spare).
- 18mm laminated pine, €69.68: 2 sheets, about 79% used.
- 9mm V-groove moisture-resistant MDF, grooved on the long edge at 100mm centres, €57.50:
2 sheets, one back each, about 75% used.
- Sheets total €500.36, all from Strahan Timber
([strahanonlineshop.ie](https://www.strahanonlineshop.ie)).
- Measure the sheets and set the thickness settings to match; nominal thicknesses are
often a little under.
- Pine edges are solid wood, so no edge banding.
- Each unit weighs roughly 75kg assembled; build it in the room.



### 4.2 Cutting

About 63 cuts, counting a rip per strip, a crosscut per part and an extra rip per part
narrower than its strip, all done at home with a plunge saw: €0. Needs about 2.6m of
joined track for the 244cm rips and 213cm crosscuts, and rigid foam insulation under each
sheet.

⚠️ **Saw width:** the packing assumes a 3mm saw cut (`config.kerf`). Plunge saw blades
cut 2.2–2.8mm, so it has margin. Check the blade and set `config.kerf` if it's wider.

### 4.3 Hardware and finish

Rough placeholder prices, each a setting; replace with real ones.


| Item                  | Spec                                                         | Estimate  |
| --------------------- | ------------------------------------------------------------ | --------- |
| Hinges ×8             | [LOOTICH 110° soft-close inset, 8 pack](https://www.amazon.ie/dp/B07S52MPYH) (Amazon), rated 16–19mm doors | €18.58 |
| Knobs ×4              | one per door, already owned                                  | €0        |
| Wood screws ~12       | 4 × 60mm countersunk, for the 37mm top's pockets and 2 down into each divider; estimate | €7 |
| Short wood screws ~88 | 4 × 30mm countersunk, for 18mm panels, already owned         | €0        |
| Back screws ~120      | 4 × 30mm countersunk, through the back every 20cm, already owned | €0    |
| Corner braces ×24     | 40mm, 2 under each end of the cabinet's bottom, cabinet top and cabinet shelf, screws included; estimate | €27 |
| Washers ~96           | M4 flat, one under each pocket screw head, already owned     | €0        |
| Pocket plugs ~64      | [Shiwaki pine 9.5mm, 50 pack](https://www.amazon.ie/dp/B09P53GBG9), for open shelves, 2 packs | €15.98 |
| Wood glue             | 1L                                                           | €12       |
| Anti-tip brackets ×2  | homemade, one per unit                                       | €0        |
| Primer ×1             | MDF primer 750ml, one coat on the backs; estimate, not yet priced | €15  |
| Black paint ×1        | [GoodHome Liberty black satin 750ml](https://www.diy.ie/departments/goodhome-liberty-black-satin-interior-metal-wood-paint-750ml/5036581059460_BQ.prd) (B&Q), one coat over the primer | €20 |
| Varnish ×3            | [Ronseal Interior Antique Pine satin 750ml](https://tjomahony.ie/rn-int-varnish-antique-pine-satin-750ml-7536837.html), one coat | €65.73    |
| Roller kit            | [Axus Blonde natural wool mini, 101mm](https://tjomahony.ie/axus-blonde-100-natural-wool-mini-roller-kit-78axu-rkbln4.html) | €5.65 |
| Roller sleeves ×3     | [Axus Blonde 101mm, pack of 10](https://tjomahony.ie/axus-blonde-100-natural-wool-mini-sleeve-pack-of-10-4-101mm-78axu-rbln410.html), 1 pack | €9.72 |
| Brush                 | [Screwfix 173FM synthetic 3"](https://www.screwfix.ie/p/synthetic-paint-brush-3-/173fm) | €4.95     |
| Sanding sponges ×4    | [Bosch Expert 421VV](https://www.screwfix.ie/p/bosch-expert-superfine-fine-medium-grit-multi-material-hand-sanding-sponges-97mm-x-67mm-3-pack/421vv), superfine/fine/medium, 2 packs | €13.70    |
| **Subtotal**          |                                                              | **~€215** |


LOOTICH chosen: 4.4★ from 406 reviews, free delivery, with a drilling template; the
3-week wait before building covers delivery.

### 4.4 Total


|                     | Estimate                          |
| ------------------- | --------------------------------- |
| Sheets              | €500.36                           |
| Cutting             | €0, own plunge saw                |
| Hardware and finish | ~€215                             |
| Delivery            | €0, own pickup                    |
| **Total**           | **~€716**                         |




## 5. Construction

How it goes together. The generated `instructions.md` turns this into ordered steps with
real part names and measurements.

- **Cutting:** at home with a plunge saw, from the cutting list and sheet diagrams: rip
strips, then crosscut each. Sheets on rigid foam insulation, about 2.6m of joined track,
cut lines taped or scored against splintering. All sheets come from Strahan Timber: click
and collect in Rathcoole, which needs a vehicle that takes 244 × 122cm sheets. Paint from
B&Q.
- **Finishing:** sand and finish panels flat, before assembly, taping off glue areas
(panel ends and the shelf lines on the sides and divider). Laminated pine blotches under
stain, so use a clear water-based finish or hardwax oil, or a pre-stain conditioner if
staining. Test on an offcut first. Water-based varnish: raise the grain with a damp cloth
and sand 240 first; roll with the Axus Blonde wool mini roller, then tip off at once with
a near-dry wide synthetic brush, light strokes along the grain, end to end in one pass;
never rework areas that have started to set. Brush the edges, stir rather than shake.
One coat. Coat both faces equally so panels don't cup. Hardwax oil is wiped on thin and
buffed, not rolled. Backs: one coat of MDF primer, then one of black satin, brushed into
the grooves first, then rolled with a spare sleeve. Bare MDF soaks up paint, so a single
coat of black alone won't cover.
- **Joinery:** butt joints with glue and countersunk wood screws on M4 washers in pocket
holes: 4 × 30mm in the 18mm panels, so the tip can't break out through the side's outer
face, and 4 × 60mm in the 37mm top. Set the jig and bit collar to each panel's thickness.
Pocket screws were out of stock; the washer gives the tapered head a flat seat. Pockets
on each panel's hidden face; open-shelf pockets are plugged. Inside the wide bay's
cabinet, hidden by the doors, the bottom, cabinet top and cabinet shelf sit on 40mm corner
braces instead, 2 per end, set back so the doors and hinges clear them, screwed up into the panel
with screws of 15mm or less. The divider is fixed by 2
long screws down through the top (its top face is above eye level). Clamp each panel on
its line while driving; the screw nudges it away from the pocket face. No dados.
- **Assembly:** in the room the unit stands in, on the floor with the sides and divider
on their front edges, since every panel is flush at the front.
- **Backs:** square each frame, drop the back in between the sides under the top, and
screw it every 20cm into the rear edges of the divider and every horizontal panel. Pencil
the shelf lines on the back first. No glue, so nothing to tape off on the paint.
- **Install:** remove the skirting boards. Tilt each unit up with at least two people
(its corner sweeps ~215cm). Fix each unit's homemade anti-tip bracket through its top
panel into a stud wherever possible (find them with a stud finder), using spring or snap
toggles where there's no stud, never plain plugs. Wall fixings come from spares, so none
are bought.



## 6. Software



### 6.1 Architecture

A flat uv app (Python 3.12) with a settings module and three scripts in `src/`, and a
justfile. Root holds only
config, docs and generated output. Generated files go in `build/`; only its two text
outputs are committed, so every change's effect on the cut list, cost and instructions
shows in the diff.

```
bookshelf/
  .gitignore           # .venv/, build/* except materials.md and instructions.md
  .python-version      # 3.12
  AGENTS.md            # code style, quality control, spec alignment
  CLAUDE.md            # imports AGENTS.md
  README.md            # what it produces, how to change it, how it works
  justfile
  pyproject.toml
  uv.lock
  docs/
    spec.md
  src/                 # plain folder, not a package
    config.py          # adjustable settings: dimensions, layout, sheets, prices
    instructions.py    # instructions.md writer
    materials.py       # sheet packing, cost totals, materials.md, sheet diagrams
    model.py           # derived sizes, units, layout, checks, exports
  tests/
    test_materials.py  # packer self-check tests
  build/               # generated by `just build`, never edited
    bookshelf.step
    bookshelf.stl
    front.svg
    instructions.md    # committed
    materials.md       # committed
    sheets/
```

**Data flow:** `model.py` reads settings from `config.py`, builds the model, runs checks,
writes STEP/STL/SVG, then hands typed rows to the other two scripts:

- `Part` rows (label, unit, length, width, thickness, heights) and `Hardware` rows (item,
count, pack size, price per pack) to `materials.py`, with sheet size, kerf, edge trim
and prices;
- the layout, part rows, hardware rows and derived numbers (diagonals, hinge
positions) to `instructions.py`.

`Part` and `Hardware` are `NamedTuple`s defined in `materials.py`, its main consumer;
`model.py` and `instructions.py` import them from there.

**File layout:** each script opens with a short docstring (purpose, inputs, outputs, the
spec section it implements). `model.py` has banner comments for its sections, in the
order of [Flow](#64-model). The packer is a few small functions (pack strips, try
orderings, self-check), each with a one-line docstring.

**Why four files:** `config.py` is the one place to change the design or prices, with no
logic in it. `model.py` is the geometry and reads top to bottom. Sheet packing is a
self-contained algorithm that knows nothing about bookshelves, and the instructions are
mostly long step text; inlined, either would bury the model. Only `model.py` imports
`config`; `materials.py` and `instructions.py` take what they need as arguments and never
import Build123d. `model.py` imports them as siblings: running `uv run src/model.py` puts
`src/` on the import path, so no packaging is needed.

### 6.2 Setup and commands

- `uv init --app`, Python pinned to 3.12 (safe for OCP wheels on Apple Silicon); delete
the generated `main.py` and `README.md`, and create `src/`.
- `uv add build123d`; `uv add --dev ocp-vscode pytest` (viewer and tests only). pytest
finds `src/` through `pythonpath = ["src"]` in `pyproject.toml`.
- **Halt:** if the OCP/cadquery-ocp wheel won't install on this Python/arch, stop and
report the version that failed.

justfile recipes, alphabetical, each a one-liner over `uv run` (which syncs dependencies
itself, so there's no setup recipe):

- `build`: runs `src/model.py`, writing everything to `build/`, then renders
`sheets/all.png` with `rsvg-convert` (librsvg, `brew install librsvg`). ImageMagick's
built-in SVG renderer was tried and drops outlines and the grain arrow.
- `check`: runs `ruff format --check`, `ruff check`, basedpyright and `typos` through
`uvx`, so none are project dependencies, then `just --fmt --check --unstable` and
`uv run pytest`.
  - **Ruff:** default line length (88); rules `F`, `E`, `W`, `I`, `B`, `UP`, `SIM`,
  `C4`, `PTH`, `RUF`, `N` selected in `pyproject.toml`; `×` and `–` are allowed
  confusables, since the outputs use them.
  - **basedpyright:** "standard" mode, configured under `[tool.basedpyright]` in
  `pyproject.toml` so the editor and CLI agree. Strict would flood with errors from
  the untyped OCP layer, which may still need a few targeted ignores.
  - **typos:** spell-checks code and Markdown, including the spec and committed outputs
  people build from.
- `view`: runs `src/model.py --view`, which also builds and opens the OCP CAD Viewer.

**Editor:** the Ruff extension with format-on-save in Cursor, so files are formatted
before `just check` runs. Not committed; it's a personal setting.

### 6.3 Settings

`src/config.py` is a plain module of lowercase module-level variables, read as
`import config` then `config.kerf`. The module is the config object: no class or
instance. Values are in cm, one per line with a short comment. When a value was picked
for sheet yield or another constraint, the comment says so, e.g.
`depth = 29.5  # 4 strips plus saw cuts and edge trim`. Banner comments group them:

- **Dimensions:** unit width, narrow bay width, height, depth, 37mm and 18mm pine and
back thickness, kickboard, cabinet height, door gap, cabinet shelf depth, V-groove
spacing.
- **Layout:** `layout = ["narrow", "wide", "fireplace", "wide", "narrow"]` and
`fireplace_width = 160`. Bays between fireplaces form one unit, in order.
- **Sheets and cutting:** sheet size, the 37mm board's own size, `kerf = 0.3`, edge
trim.
- **Prices:** per sheet, per cut, delivery, and per hardware pack.
- **Viewer:** `hide_doors`, to see inside the cabinets; `pine_color` and `back_color`
for the viewer and STEP file.

Only things a person would change live here. Derived sizes (the wide bay's width, shelf
heights both bays share, door sizes) and hardware counts depend on the geometry,
so they're computed at the top of `model.py` and never repeated as literals further
down.

- **Units:** Build123d is mm by convention and STEP/STL readers assume mm, so values are
multiplied by Build123d's `CM` when building.
- **Types:** type hints on functions, checked by `just check`. No dataclass or validation
library; the only types are the `Part` and `Hardware` rows.
- **Names:** parts use the spec's words (side, divider, top, bottom, shelf, cabinet_top,
cabinet_shelf, kickboard, door, back), unabbreviated, so one name traces through the
code, labels, `materials.md` and `instructions.md`.



### 6.4 Model

- **One unit function:** `unit(bays)` returns one unit's labeled parts at its own
origin, for its bays left to right: outer sides, top and back, then each bay's bottom,
shelves and kickboard with a divider between bays. A wide bay adds the cabinet top,
cabinet shelf and doors; a narrow bay gets the lower shelves instead. It's the only
function in `model.py`.
- **Parts:** Build123d algebra mode (`Pos(...) * Box(...)`), not builder mode. Boxes use
`align=Align.MIN` on every axis so each position is the panel's front-left-bottom
corner. Every part sets `.label`.
- **Unit origin:** floor, front-left corner of the carcass. X width, Y depth, Z height.
Doors sit in front, at negative Y.
- **Layout:** origin at the left end of the left unit; the next unit starts
`config.fireplace_width` after it. Parts are labeled under their unit and bay, e.g.
`unit_1 / wide shelf_2`; frame parts have no bay (`unit_1 / divider_1`).
- **Assembly:** one labeled `Compound`, not fused, so each panel stays separate. Used for
viewing, checks and exports.
- **Flow:** plain script with no `main()`, top to bottom: derived sizes, `unit()`,
layout, checks, exports. Checks run before exports and exit with a clear
message on failure, so a bad model never reaches `build/`.
- **Viewing:** with `--view` only, `ocp_vscode` `show()` in the OCP CAD Viewer extension.
`config.hide_doors` hides the doors to see inside the cabinets.



### 6.5 Outputs

All overwrite `build/` on every run, and each path is printed.

`bookshelf.step` **/** `bookshelf.stl`**:** the full named, coloured assembly for other CAD tools,
and a mesh for quick previews (STL holds no colour).

`front.svg`**:** front elevation of both units with the fireplace gap. The assembly is
projected from a camera straight in front (`project_to_viewport`) and written with
`ExportSVG`; visible edges solid, hidden edges (e.g. cabinet shelves) dashed on their own
layer.

`materials.md`, written by `materials.py`:

- **Parts:** name, unit type, quantity across all units, length × width, thickness,
material. Identical panels grouped. Dimensions from each part's bounding box (smallest
is thickness, largest is length), rounded to 0.1cm.
- **Sheets to buy:** per material: its own sheet size, count, share of area used.
- **Hardware and finish:** counts derived from the parts and layout (hinges and knobs per
door, screws and washers per pocket, 2 pockets per panel end (plugs for the open
shelves), 2 corner braces per end of each cabinet panel, 2 long screws per divider, back screws per 20cm of rear edge plus one, brackets
per unit, finish and sanding by panel area), with packs to buy and cost. Panel area is
both faces of every pine part (~19m²). Varnish litres = area × coats ÷ coverage (11m²/L:
the label says 16, but bare pine soaks up the first coat), unrounded, then whole cans:
1.7L, 3 × 750ml. Sanding sponges = area ÷ 5m² per sponge, rounded up: 4, so 2 packs of 3.
Roller sleeves = area × coats ÷ 6m² per sleeve, rounded up, less the 1 assumed in the
kit: 3, so 1 pack of 10. Primer litres = front face of the backs (~4.5m²) ÷ 10m²/L: 0.5L,
so 1 × 750ml. Black paint litres = the same face × 1 coat ÷ 12m²/L (the label's 9m² per
750ml): 0.4L, so 1 × 750ml.
- **Cost:** sheets, cutting, hardware and finish, delivery, total. Placeholder prices are
labeled estimates; a price of 0 shows as €0.00 in the hardware table (already owned), as
own plunge saw for cutting and own pickup for delivery.
- **Saw width warning:** ⚠️ under the sheet count and the cost, stating the assumed
`config.kerf` and to confirm the saw width before cutting.

`sheets/*.svg`, written by `materials.py` from the same packing: each part's position,
label and size with a grain arrow; offcuts blank. `all.svg` stacks every sheet top to
bottom in one file. Plain SVG text, no drawing library.

`instructions.md`, written by `instructions.py` as a plain template with the model's
numbers filled in. Ordered steps, each listing the parts and hardware it uses:

1. **Cut:** the cutting list, per sheet: strips to rip and parts to crosscut from each,
  in order, with a link to the sheet's diagram. A part narrower than its strip gets an
  extra rip, listed with it. Plunge saw setup; check the blade width first. Where to
  place each back's cut against the sheet's grooves.
2. **Check and label:** count panels against the parts table, then pencil each part name
  (e.g. `unit_1 / wide shelf_2`) on an edge that will be hidden.
3. **Sand and finish** both faces and visible edges, taping off glue areas.
4. **Mark shelf lines:** a table per bay of each horizontal panel's top and underside
  from the floor (as in [Heights](#33-heights)). Mark each bay's outer side and the
   divider's matching face together, as mirror images. This is the core of the
   document: fixed shelves leave no room for error.
5. **Drill pocket holes:** on each panel's hidden face, at both ends, positions
  measured from the panel's front edge; none in the braced cabinet panels.
6. **Assemble each carcass** in its room, on its front edges: top between the sides with
  long screws down into the divider, then each bay's bottom, cabinet top and shelves,
  then the kickboards 5cm back from the front edge.
7. **Square and fix the back:** diagonals equal (~241.4cm), then drop the back in and
  screw it along the shelf and divider lines.
8. **Cabinet shelf, hinges and doors:** cabinet shelf height, hinge cup and plate
  positions (settings matching the hinge maker's template), knob position, adjusting the
   gaps.
9. **Install:** remove the skirting, tilt each unit up (two people, ~215cm sweep), fix the
  anti-tip brackets into studs or toggles.

Finish product instructions and wall cutouts are left out.

### 6.6 Packing

How `materials.py` turns part rows into sheets and a cutting list (written into
`instructions.md`).

- **Method:** pack the way a panel saw cuts: rip strips across the sheet, crosscut parts
from each strip, with `config.kerf` per cut inside each material's usable area. Each
part's length runs along the sheet's length (grain).
- **Offcuts:** a part goes into an existing strip's leftover length when it's no wider
than the strip; that's how narrow shelves land in wide shelf and door strips.
- **Shared sheets:** parts from all units share sheets, grouped by material, each with
its own sheet size.
- **Quality:** a single greedy pass can miss the best layout at this fill level, so the
packer tries several part orderings and keeps the one with the fewest sheets.
- **Expected:** 2 × 37mm pine, 2 × 18mm pine and 2 V-groove sheets:
  - 37mm 1: four side strips.
  - 37mm 2: a strip of both tops, two divider strips; one strip spare.
  - 18mm 1–2: the 4 doors in 37.3cm strips (with wide panels in their offcuts), the
  kickboards in a 10cm strip, and the shelves, bottoms, cabinet tops and cabinet shelves
  in 28.6cm strips.
  - V-groove 1–2: one back each.



## 7. Quality

- **Model checks** in `model.py`, before any export:
  - layout bounding box is 387.4 × 29.5 × 213 (unit widths plus `config.fireplace_width`, by
  depth, by height);
  - every unit is `config.unit_width` wide;
  - every bay's centre falls on the V-groove pattern (a groove or the middle between two),
  so the grooves are symmetric in each bay;
  - no two panels overlap, within a unit or between neighbors;
  - every panel fits the usable sheet with its length along the grain (sides and backs
  are the tightest).
- **Packer self-check:** every part placed exactly once, within the usable area, no
overlaps, a kerf between neighbors; otherwise the build fails. Wrong cutting lists are
the costliest bug here.
- **Packer tests** (`tests/test_materials.py`): prove the self-check rejects broken
layouts (overlapping parts, a missing part, no kerf between neighbors, a part off the
usable sheet), and that a part longer than any sheet fails with a clear message. The
only unit tests: geometry is covered by the model checks, text by the committed output
diff.
- **Check messages** show actual and expected values, e.g. "bounding box width 388.6,
expected 387.4", so a failure is clear without rerunning.
- **Every change:** `just check` (format, lint, types, spelling, tests) and `just build`
must pass.
- **Review:** one status item per commit, with the spec updated and the regenerated
`materials.md` and `instructions.md` included, plus a 2–3 line summary of which numbers
moved. Geometry changes also get a look at `front.svg` and the sheet diagrams.
- **Halt:** if the packer reports more than 2 × 37mm or 2 × 18mm pine sheets with the
defaults, improve the packer rather than accept it.



## 8. Decisions

Options considered and why they lost. Newest first within each group.

**Material:**

- 24mm pine frame, 18mm insides, 3.2mm hardboard backs glued and stapled (~€666): the
37mm frame looks chunkier and needs only 2 frame sheets once the bottoms and cabinet tops
move to 18mm; the V-groove back adds a panelled look. +€26 overall.
- 37mm bottom and cabinet top: heavier with no structural gain; 18mm on the kickboard,
with the screwed back, keeps the base square.
- 32mm frame: not stocked at Strahan (24, 28mm stair treads, 37mm).
- Laminated red deal stair treads for the frame (6 × 3.6m, 24.2mm €196.50 or 28mm
€241): crosscuts only, no rips, but 27cm deep, redder than the pine and possibly
nosed; the 37mm sheet (€246) is real pine at full depth.
- Pre-cut 37mm pine shelf boards (220 × 37 × 890mm): too short and narrow for the frame.
- 3.2mm hardboard backs painted black (€25.90 plus €40 paint): V-groove MDF (€115) looks
far better behind black, is stiffer, and is from the same shop as the pine.
- 12mm V-groove (€66.24 a sheet): heavier and dearer with no gain at this size.
- Glued backs: screws alone resist racking, mean no taping off the paint, and let the
back come off. Pocket holes in the back: 9mm is under the jig's ~12mm minimum.
- A rebated back (routed step in the frame's rear edges): shallower shelves get the same
result with no router.
- Two coats of black on the back: bare MDF soaks it up; primer plus one coat covers better
for less.
- All 24mm pine (4 sheets, ~€769): 24mm doors are past every affordable concealed
hinge's rating (Hafele, Eclipse 14–22mm; LOOTICH 16–19mm); only Hettich lists 24mm, at
~€75 for 8 from the UK. 18mm shelves, doors, cabinet shelves and kickboards keep stock
hinges and a lighter shelf look for +€41 (a 5th sheet, the third 24mm half spare).
- 18mm doors and hidden parts only: fixes the hinges too, but mixes thicknesses where
open shelves show; all shelves 18mm reads as a deliberate frame.
- Full overlay still shows ~6mm of each 24mm side beside the closed doors; 18mm sides
would hide it but lose the chunky frame.
- 18mm pine (€69.68/sheet) for everything: €115 cheaper and lighter, but a slimmer look.
- 24mm for only the sides and tops: costs more than all 24mm, because it breaks the sheet
layout and needs a third 24mm sheet.
- Inset 18mm back: needed a third 18mm sheet and fitting; a thin nailed-on back is simpler.
- Backs: 6mm birch (€77.49) is €23 more for strength the design doesn't need. Staples
over panel pins: as strong with glue, much faster.
- 4mm birch backs (€131.98 for 2): painted black hardboard (€25.90 plus €40 paint) saves
~€66 and suits the honey pine. Also weighed: 4mm poplar (€74.86, near pine under the
tinted varnish, plain grain); 12mm laminated pine (€110.70, exact match but solid wood
must be screwed, not glued, and adds 8mm depth); red deal tongue and groove (€95.94,
real pine but nailed, so little racking resistance); B&Q 5mm hardwood ply (pink tropical
face); EV pine ply (face dyed red); white-faced hardboard (paint grips its coating poorly).
- 18mm plywood frames (the original spec): switched to laminated pine, whose solid-wood
edges need no banding. MDF was ruled out because it sags under books.

**Dimensions:**

- 115.6cm units (77.3cm wide bay): fills the wall, but the back's grooves sat 0.95cm off
centre in the wide bay. 113.7cm makes both bays symmetric for 1.9cm less per unit; Strahan's
custom groove centres were the alternative.
- Cabinet top at 90cm (the usual built-in height): doors 79.6cm long no longer fit a
strip with six narrow shelves, costing a 5th pine sheet (+€98.40); 87cm keeps 4 sheets
with a 3mm or 4mm saw. 88cm fits only with a 3mm saw.
- Cabinet top at 76cm (desk height): replaced by 87cm for a taller, more built-in cabinet
at the same sheet count.
- 91.6cm wide units (88cm shelves): only two shelves per strip, costing a 5th pine and a
3rd birch sheet.
- 30cm narrow units: fits, but 26.4cm inside is tight for books; 32cm lets side offcuts
supply narrow shelves.
- 30cm-deep sides with 4 strips needed 121.9cm of a 122cm sheet; 29.5cm leaves margin for
edge trim.
- Keeping the 18mm-era widths after moving to 24mm shortened shelves by 1.2cm. Widening
each unit by 1.2cm (118cm sets) would restore 80cm and 28.4cm shelves at the same sheet
count, if the wall allows.

**Layout and features:**

- Antique black iron brackets under every shelf (4 each, ~64): a bold look and no shelf
pockets, but busy in the narrow bay and ~€65–190; on hold. Shelves keep pocket screws.
- Adjustable shelves on pins above the braced cabinet: fewer pockets and marked lines,
but visible pin holes and fewer fixing points for the back; not taken for now.
- Pocket screws inside the cabinet: corner braces are quicker, need no jig or plugs, and
the doors hide them.
- Full overlay doors (Hafele, €21.80 for 8): cheaper and forgiving of an out-of-square
frame, but hid most of the 37mm frame's edge and stood 1.8cm proud. Inset shows the full
frame and keeps the unit 29.5cm deep, for +€52 in hinges and a careful squaring step.
- Four separate units, bolted in two sets (8 connector bolts): one carcass per side with
a shared 37mm divider drops two sides, the bolts and a 4.8cm double line, and gives one
back per unit. Each unit is heavier (~75kg) and is built in its room.
- Blum 110° inset hinges (Screwfix 1964J, €73.80 for 8): local and a stronger brand,
but €55 more than LOOTICH's inset version, with 10× fewer reviews.
- LOOTICH overlay hinges (€17.22 for 8, rated 16–19mm) and Hettich Sensys (rated to 24mm, ~€75
for 8 from the UK): Hafele from Screwfix is in stock locally with far more reviews.

- One row of four bolted units: replaced by two sets either side of the fireplace.
- Shared sides between units: saves no sheet, loses movability. Superseded by one
carcass per side.
- Dropping the cabinet shelves: saves nothing, since they come from an otherwise spare
strip.
- Inset doors (with the 24mm frame): need an even gap all round and expose any
out-of-square frame; full overlay hid it. Reversed for the 37mm frame, see above.
- Push-to-open latches: don't work with soft-close hinges; soft-close with knobs chosen.
- Skirting notches: skirting is being removed instead.
- Hanging strip for anchoring: anti-tip brackets through the top panel instead.
- Bought anti-tip brackets (€16) and plasterboard toggles (€10): brackets are homemade
and wall fixings come from spares. Anchoring stays in the instructions.

**Software:**

- Single script: packing and instructions would bury the model.
- Three scripts at the repo root: cluttered root mixing code with config and docs; moved
to `src/`, with `bookshelf.py` renamed `model.py`.
- UPPER_CASE constants at the top of `model.py`: mixed settings with geometry, and the
casing was disliked; replaced by lowercase settings in `config.py`.
- Frozen dataclasses for settings (`Design`, `Cutting`, `Prices`): only worth it for
several configs at once or guarding against mutation; a plain module is simpler.
- A real package (`src/bookshelf/` with an entry point): needs a build backend,
`__init__.py` and `pyproject.toml` wiring for a one-off build script.
- A packing library (e.g. rectpack): doesn't give a panel-saw strip order for the
cutting list.
- No unit tests at all: nothing proved the packer's self-check rejects a bad layout, and
a broken self-check would let every build pass. Now pytest covers the packer only.
- Broader unit tests (geometry, instruction text): they'd repeat the model checks and the
committed output diff, which already run on the real design.
- Ignoring all of `build/`: output changes were invisible in review; the two text outputs
are now committed.
- Bare tuples or dicts between scripts: untyped and unclear in review; replaced by `Part`
and `Hardware` `NamedTuple`s. A separate types file was rejected; they live in
`materials.py`.
- basedpyright strict mode: too noisy with the untyped OCP layer; standard mode instead.
- Ruff `D` (docstring style) and full `PL` (pylint): noisy; `PL`'s magic-number rule only
catches comparisons. One docstring per file is enforced in review instead.
- pre-commit framework: another tool and config file; `just check` before each commit
covers it.
- Markdown formatter (prettier, mdformat): rewraps the spec's prose and adds diff noise.
- mypy: duplicates basedpyright.
- PNG front view: SVG needs no extra dependency and scales cleanly.
- Strahan cutting the sheets on their panel saw (~€75 at an assumed €1 per cut): a plunge
saw at home saves that, and the 3mm kerf setting already covers its blade.
- Confirmat screws: their heads show on every visible outer side; pocket screws hide
them on the shelves, at the cost of a jig and plugs for the open shelves.
- 8m²/L varnish coverage (4 cans): too cautious against the label's 16m²/L; 11m²/L
gives 3 cans, and a 4th can be bought if needed.
- Pocket hole jig in the hardware list at €0: already bought, so dropped from the list.
- Two coats of clear finish: one coat of water-based varnish saves time and about two cans;
shelf tops and doors get the least protection, so add a second coat there if they mark.



## 9. Status

Progress: ⬜ unblocked · 🛑 blocked · 🔄 in progress · ✅ done · ❓ undecided · ⏸️ paused · 🚫 not doing

- ✅ Design confirmed
- ✅ Setup and justfile ([6.2](#62-setup-and-commands))
- ✅ Settings and model ([6.3](#63-settings), [6.4](#64-model))
- ✅ Model checks ([7](#7-quality))
- ✅ STEP, STL and front view ([6.5](#65-outputs))
- ✅ Packing, packer tests and material spec ([6.6](#66-packing), [7](#7-quality), [6.5](#65-outputs))
- ✅ Sheet diagrams ([6.5](#65-outputs))
- ✅ Assembly instructions ([6.5](#65-outputs))
- ✅ Two units with a 37mm frame and V-groove backs ([3](#3-furniture-design))
- ✅ Corner braces inside the cabinet ([5](#5-construction))
- ⬜ Real prices: saw width, hardware, primer, long screws, corner braces ([4](#4-materials-and-cost))
- ✅ Inset doors ([3.4](#34-doors))
- ✅ Symmetric V-grooves: 113.7cm units ([3.2](#32-frame-and-bays))

