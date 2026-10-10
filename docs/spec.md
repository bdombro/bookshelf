# Bookshelf spec

A spec for a application that generates plans for making 4 bookshelves from 2 designs.

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

A parametric 3D model of four laminated pine bookshelves in Build123d, managed with uv.
One build turns the model into everything needed to buy, cut and assemble them.

**At a glance:**

- Four units in two sets either side of a 160cm fireplace wall: narrow, wide | fireplace
| wide, narrow. 391.2cm overall.
- Every unit is 213cm tall with 29.5cm-deep shelves and a recessed 10cm kickboard. The
carcass is 29.9cm deep with the back, 32.3cm at the cabinet doors.
- Wide ×2: 83.6cm wide. 4 open compartments over a 2-door cabinet with an inside shelf.
- Narrow ×2: 32cm wide. 6 open compartments, lined up with the wide units' shelves.
- 24mm laminated pine for every panel except the backs, which are 4mm birch plywood,
glued and stapled.
- Estimated cost ~€790 before delivery: 4 pine and 2 birch sheets €525.58, cutting by
Strahan Timber (cutmylist.ie) ~€64, hardware and finish ~€200.

**Outputs** (all in `build/`, detailed in [Outputs](#65-outputs)):

- `bookshelf.step` and `bookshelf.stl`: the assembled layout for other tools.
- `front.svg`: front elevation of both sets.
- `materials.md`: parts, sheets, cutting list, hardware and cost.
- `sheets/*.svg`: one cutting diagram per sheet.
- `instructions.md`: step-by-step assembly with a shelf marking guide.



## 2. Requirements and constraints

- **Room:** a 160cm fireplace wall with one set on each side. Each set's 115.6cm fits
(confirmed by the owner). Plasterboard wall; skirting boards come off before install.
No records or oversized books, so ~30cm compartments are enough. The fireplace's
clearance is fine.
- **Sheets:** standard Irish 244 × 122cm. Usable area is 243 × 121cm after 0.5cm is
trimmed off each edge for squaring.
- **Grain:** laminated pine's strips run along the sheet's 244cm length. Every pine part
keeps its length along them: sides and doors vertical, shelves the long way.
- **Saw width:** `config.kerf` setting, 0.3cm for now. The cutter's saw may be ~0.4cm; the
4-sheet layout fits either way.
- **Flexible sizes:** exact dimensions can change whenever that makes building, cutting
or buying simpler. Most sizes below were picked for sheet yield.
- **Not modeled:** hardware, wall cutouts for sockets or switches (cut by hand during
install), finish.



## 3. Furniture design



### 3.1 Layout

A left set (narrow, wide) and a mirrored right set (wide, narrow), with the wide units
next to the fireplace wall. Each set is 115.6cm; the layout is 2 × 115.6 + 160 = 391.2cm.
The two units in a set are bolted together through their touching sides, which make a
4.8cm double line.

### 3.2 Unit types

All pine is 24mm, for a chunkier, built-in look.

- **Wide (83.6cm):** shelves are 83.6 − 2 × 2.4 = 78.8cm, so three fit end to end on a
243cm strip. 4 open compartments over a 2-door cabinet with one inside shelf.
- **Narrow (32cm):** shelves are 27.2cm. A 213cm side leaves ~29.7cm of its strip, so
every side's offcut yields one narrow shelf: 8 of the 14 narrow shelves come free.
6 open compartments, no doors.
- **Depth:** sides and shelves are 29.5cm, so four strips plus saw cuts and edge trim fit
across a sheet. The back adds 0.4cm (29.9cm) and the doors 2.4cm more (32.3cm). Sides
are one depth top to bottom.
- **Shelves:** all fixed. A 78.8cm span of 24mm pine won't visibly sag under books.
- **Kickboard:** between the sides, set back 5cm for a toe recess; the bottom panel rests
on it and the sides run to the floor.



### 3.3 Heights

Measured from the floor (the bottom of the sides). Both unit types share every height
from the cabinet top up, so shelf lines run straight across a set.


| Panel               | Wide                     | Narrow      |
| ------------------- | ------------------------ | ----------- |
| Kickboard           | 0–10                     | 0–10        |
| Bottom              | 10–12.4                  | 10–12.4     |
| Lower shelf         | cabinet shelf, 41.8–44.2 | 41.8–44.2   |
| Cabinet top / shelf | 73.6–76                  | 73.6–76     |
| Shelf               | 107.9–110.3              | 107.9–110.3 |
| Shelf               | 142.1–144.5              | 142.1–144.5 |
| Shelf               | 176.4–178.8              | 176.4–178.8 |
| Top                 | 210.6–213                | 210.6–213   |


Compartments are ~31.9cm clear above the cabinet top and ~29.4cm below it in the narrow
units. The wide unit's cabinet shelf is 25cm deep against the back, leaving ~4.5cm at the
front for hinges.

### 3.4 Doors

Wide units only. Full overlay: outer edges flush with the outside of the sides, a 0.4cm
gap between the pair, from 10.2cm to 75.8cm, covering the front edges of the sides,
bottom and cabinet top. Each is 41.6 × 65.6 × 2.4cm, grain vertical, on 2 soft-close
concealed hinges with one knob.

### 3.5 Backs

4mm birch plywood cut to each unit's outside size (83.6 × 213 and 32 × 213), running to
the floor behind the kickboard. Glued and stapled to the rear edges of the sides, top,
bottom and every shelf; it keeps the frame square.

### 3.6 Panel list

Per unit. All pine parts are 2.4cm thick.


| Part             | Wide (83.6cm)   | Narrow (32cm)   |
| ---------------- | --------------- | --------------- |
| Sides            | 2 × 213 × 29.5  | 2 × 213 × 29.5  |
| Top, bottom      | 2 × 78.8 × 29.5 | 2 × 27.2 × 29.5 |
| Cabinet top      | 1 × 78.8 × 29.5 | –               |
| Shelves          | 3 × 78.8 × 29.5 | 5 × 27.2 × 29.5 |
| Cabinet shelf    | 1 × 78.8 × 25   | –               |
| Kickboard        | 1 × 78.8 × 10   | 1 × 27.2 × 10   |
| Doors            | 2 × 41.6 × 65.6 | –               |
| Back (4mm birch) | 1 × 83.6 × 213  | 1 × 32 × 213    |




## 4. Materials and cost

Expected figures with the defaults. Exact counts come from `build/materials.md`.

### 4.1 Sheets

- 24mm laminated (edge-glued) solid pine, €98.40: 4 sheets, about 90% used.
- 4mm BB/BB birch plywood, €65.99: 2 sheets, one set's two backs on each.
- Sheets total €525.58.
- Measure the sheets and set the thickness settings to match; nominal thicknesses are
often a little under.
- Pine edges are solid wood, so no edge banding.
- 24mm makes each unit about a third heavier than 18mm; a wide unit is a two-person lift.



### 4.2 Cutting

About 64 cuts (≈58 pine, 6 birch). Strahan doesn't publish a price, so the estimate
assumes €1 per cut: ~€64. Replace it with their quote.

⚠️ **Saw width before ordering precut:** the packing assumes a 3mm saw cut (`config.kerf`).
Industrial panel saws like Strahan's often cut ~4mm. The 4-sheet layout still fits at
4mm, but confirm their saw width and set `config.kerf` before submitting the list.

### 4.3 Hardware and finish

Rough placeholder prices, each a setting; replace with real ones.


| Item                  | Spec                                                         | Estimate  |
| --------------------- | ------------------------------------------------------------ | --------- |
| Hinges ×8             | soft-close 35mm concealed full overlay, rated for 24mm doors | €40       |
| Knobs ×4              | one per door                                                 | €12       |
| Confirmat screws ~190 | 7 × 60mm for 24mm panels, 2 boxes of 100                     | €24       |
| Stepped drill bit     | matching the confirmats                                      | €10       |
| Staples               | narrow crown, 16–19mm legs                                   | €8        |
| Wood glue             | 1L                                                           | €12       |
| Connector bolts ×8    | for the joint in each set                                    | €8        |
| Anti-tip brackets ×4  | one per unit                                                 | €16       |
| Plasterboard toggles  | spring or snap, for fixings that miss a stud                 | €10       |
| Clear finish          | ~4L, both faces of every panel, two coats                    | €60       |
| **Subtotal**          |                                                              | **~€200** |


Most concealed hinges cover 16–26mm doors; check before buying.

### 4.4 Total


|                     | Estimate                          |
| ------------------- | --------------------------------- |
| Sheets              | €525.58                           |
| Cutting             | ~€64                              |
| Hardware and finish | ~€200                             |
| Delivery            | unknown (0 for click and collect) |
| **Total**           | **~€790 before delivery**         |




## 5. Construction

How it goes together. The generated `instructions.md` turns this into ordered steps with
real part names and measurements.

- **Cutting:** Strahan Timber cuts the sheets through
[cutmylist.ie](https://www.cutmylist.ie/) on their panel saw, from the cutting list and
sheet diagrams. They only cut boards bought from their stock and quote from a
submitted cutting list. Delivery is Dublin only, or click and collect in Rathcoole. If
their sheet count differs from ours, theirs wins.
- **Finishing:** sand and finish panels flat, before assembly, taping off glue areas.
Laminated pine blotches under stain, so use a clear water-based finish or hardwax oil,
or a pre-stain conditioner if staining. Test on an offcut first.
- **Joinery:** butt joints with glue and confirmat screws; no clamps or dados.
- **Backs:** square each frame, then glue and staple every 10–15cm. Keep each staple's
crown along the 24mm edge, not across it, so a leg can't split out through a face.
Pencil the shelf lines on the back first. Glue is safe because every glued edge runs
along the pine's grain.
- **Install:** remove the skirting boards. Bolt each set's two units together, then fix
each unit's anti-tip bracket through its top panel into a stud wherever possible (find
them with a stud finder), using spring or snap toggles where there's no stud, never
plain plugs. A 32cm-wide, 213cm-tall unit tips very easily.



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
- the layout, part rows, hardware rows and derived numbers (diagonals, hinge and bolt
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

- `build`: runs `src/model.py`, writing everything to `build/`.
- `check`: runs `ruff format --check`, `ruff check`, basedpyright and `typos` through
`uvx`, so none are project dependencies, then `just --fmt --check --unstable` and
`uv run pytest`.
  - **Ruff:** default line length (88); rules `F`, `E`, `W`, `I`, `B`, `UP`, `SIM`,
  `C4`, `PTH`, `RUF`, `N` selected in `pyproject.toml`.
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
`wide_width = 83.6  # 3 shelves per 243cm strip`. Banner comments group them:

- **Dimensions:** unit widths, height, shelf depth, pine and back thickness, kickboard,
cabinet height, door gaps, cabinet shelf depth.
- **Layout:** `layout = ["narrow", "wide", "fireplace", "wide", "narrow"]` and
`fireplace_width = 160`. Unit counts and the bolted joints (neighbors not split by the
fireplace) come from it.
- **Sheets and cutting:** sheet size, `kerf = 0.3`, edge trim.
- **Prices:** per sheet, per cut, delivery, and per hardware pack.
- **Viewer:** `hide_doors`, to see inside the cabinets.

Only things a person would change live here. Derived sizes (shelf lengths, the shelf
heights both unit types share, door sizes) and hardware counts depend on the geometry,
so they're computed at the top of `model.py` and never repeated as literals further
down.

- **Units:** Build123d is mm by convention and STEP/STL readers assume mm, so values are
multiplied by Build123d's `CM` when building.
- **Types:** type hints on functions, checked by `just check`. No dataclass or validation
library; the only types are the `Part` and `Hardware` rows.
- **Names:** parts use the spec's words (side, top, bottom, shelf, cabinet_top,
cabinet_shelf, kickboard, door, back), unabbreviated, so one name traces through the
code, labels, `materials.md` and `instructions.md`.



### 6.4 Model

- **One unit function:** `unit(width, cabinet)` returns one unit's labeled parts at its
own origin. It's the only function in `model.py`; the cabinet flag adds the doors
and cabinet shelf, or the narrow unit's lower shelf instead.
- **Parts:** Build123d algebra mode (`Pos(...) * Box(...)`), not builder mode. Boxes use
`align=Align.MIN` on every axis so each position is the panel's front-left-bottom
corner. Every part sets `.label`.
- **Unit origin:** floor, front-left corner of the carcass. X width, Y depth, Z height.
Doors sit in front, at negative Y.
- **Layout:** origin at the left end of the left set. Within a set each unit starts where
the previous one ends; the right set starts `config.fireplace_width` later, mirrored
(wide, then narrow). Parts are labeled under their unit, e.g. `wide_1 / shelf_2`.
- **Assembly:** one labeled `Compound`, not fused, so each panel stays separate. Used for
viewing, checks and exports.
- **Flow:** plain script with no `main()`, top to bottom: derived sizes, `unit()`,
layout, checks, exports. Checks run before exports and exit with a clear
message on failure, so a bad model never reaches `build/`.
- **Viewing:** with `--view` only, `ocp_vscode` `show()` in the OCP CAD Viewer extension.
`config.hide_doors` hides the doors to see inside the cabinets.



### 6.5 Outputs

All overwrite `build/` on every run, and each path is printed.

`bookshelf.step` **/** `bookshelf.stl`**:** the full named assembly for other CAD tools, and a
mesh for quick previews.

`front.svg`**:** front elevation of both sets with the fireplace gap. The assembly is
projected from a camera straight in front (`project_to_viewport`) and written with
`ExportSVG`; visible edges solid, hidden edges (e.g. cabinet shelves) dashed on their own
layer.

`materials.md`, written by `materials.py`:

- **Parts:** name, unit type, quantity across all units, length × width, thickness,
material. Identical panels grouped. Dimensions from each part's bounding box (smallest
is thickness, largest is length), rounded to 0.1cm.
- **Sheets to buy:** per material: sheet size, count, share of area used.
- **Cutting list:** per sheet, strips to rip and parts to crosscut from each, in panel saw
order. A part narrower than its strip gets an extra rip, listed with it.
- **Hardware and finish:** counts derived from the parts and layout (hinges and knobs per
door, confirmats per butt joint, staples per back, bolts per set joint, brackets per
unit, finish by panel area), with packs to buy and cost.
- **Cost:** sheets, cutting, hardware and finish, delivery, total. Placeholder prices are
labeled estimates; a price of 0 shows as unknown.
- **Saw width warning:** ⚠️ under the sheet count and the cost, stating the assumed
`config.kerf` and to confirm the cutter's saw width before ordering precut.

`sheets/*.svg`, written by `materials.py` from the same packing: each part's position,
label and size with a grain arrow; offcuts blank. Plain SVG text, no drawing library.

`instructions.md`, written by `instructions.py` as a plain template with the model's
numbers filled in. Ordered steps, each listing the parts and hardware it uses:

1. **Order:** submit the cutting list and diagrams; confirm the saw width first.
2. **Check and label:** count panels against the parts table, then pencil each part name
  (e.g. `wide_1 / shelf_2`) on an edge that will be hidden.
3. **Sand and finish** both faces and visible edges, taping off glue areas.
4. **Mark shelf lines:** a table per unit type of each horizontal panel's top and
  underside from the bottom of the side (as in [Heights](#33-heights)). Mark each pair
   of sides together, as mirror images, on their inner faces. This is the core of the
   document: fixed shelves leave no room for error.
5. **Drill for confirmats:** hole positions through each side into each panel end,
  measured from the front edge.
6. **Assemble each carcass** on its back: sides with top and bottom, then cabinet top and
  shelves, then the kickboard 5cm back from the front edge.
7. **Square and fix the back:** diagonals equal to the expected value per unit type
  (~228.8cm wide, ~215.4cm narrow), then glue and staple along the shelf lines.
8. **Cabinet shelf, hinges and doors:** cabinet shelf height, hinge cup and plate
  positions (settings matching the hinge maker's template), knob position, adjusting the
   gaps.
9. **Install:** remove the skirting, stand each unit up (two people), bolt each set at the
  given bolt positions, fix the anti-tip brackets into studs or toggles.

Finish product instructions and wall cutouts are left out.

### 6.6 Packing

How `materials.py` turns part rows into sheets and a cutting list.

- **Method:** pack the way a panel saw cuts: rip strips across the sheet, crosscut parts
from each strip, with `config.kerf` per cut inside the usable 243 × 121cm. Each part's length
runs along the sheet's length (grain).
- **Offcuts:** a part goes into an existing strip's leftover length when it's no wider
than the strip; that's how narrow shelves land in side and door offcuts.
- **Shared sheets:** parts from all units share sheets, grouped by material.
- **Quality:** a single greedy pass can miss the best layout at this fill level, so the
packer tries several part orderings and keeps the one with the fewest sheets.
- **Expected:** 4 pine and 2 birch sheets. A hand layout that achieves it:
  - Pine 1–2: four side strips each; each side's offcut is a narrow shelf.
  - Pine 3: four strips of three wide shelf-sized panels (12).
  - Pine 4: two 41.6cm door strips (2 doors and 3 narrow shelves each), a 10cm strip with
  all 4 kickboards, and a 25cm strip with both cabinet shelves.
  - Birch 1–2: one wide and one narrow back side by side.



## 7. Quality

- **Model checks** in `model.py`, before any export:
  - layout bounding box is 391.2 × 32.3 × 213 (unit widths plus `config.fireplace_width`, by
  depth + back + door, by height);
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
- **Check messages** show actual and expected values, e.g. "bounding box width 392.4,
expected 391.2", so a failure is clear without rerunning.
- **Every change:** `just check` (format, lint, types, spelling, tests) and `just build`
must pass.
- **Review:** one status item per commit, with the spec updated and the regenerated
`materials.md` and `instructions.md` included, plus a 2–3 line summary of which numbers
moved. Geometry changes also get a look at `front.svg` and the sheet diagrams.
- **Halt:** if the packer reports more than 4 pine sheets with the defaults, improve the
packer rather than accept it; the hand layout proves 4 fit.



## 8. Decisions

Options considered and why they lost. Newest first within each group.

**Material:**

- 18mm pine (€69.68/sheet): €115 cheaper and lighter, but a slimmer look; 24mm chosen.
- 24mm for only the sides and tops: costs more than all 24mm, because it breaks the sheet
layout and needs a third 24mm sheet.
- Inset 18mm back: needed a third 18mm sheet and fitting; a thin nailed-on back is simpler.
- Backs: 6mm birch (€77.49) is €23 more for strength the design doesn't need; 6mm poplar
(€55.35) and 4mm poplar (€37.43) are cheaper but show a plainer, sometimes streaky face
through the open shelves. Staples over panel pins: as strong with glue, much faster.
- 18mm plywood frames (the original spec): switched to laminated pine, whose solid-wood
edges need no banding. MDF was ruled out because it sags under books.

**Dimensions:**

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

- One row of four bolted units: replaced by two sets either side of the fireplace.
- Shared sides between units: saves no sheet, loses movability.
- Dropping the cabinet shelves: saves nothing, since they come from an otherwise spare
strip.
- Inset doors: need an even gap all round and expose any out-of-square frame; full
overlay hides it.
- Push-to-open latches: don't work with soft-close hinges; soft-close with knobs chosen.
- Skirting notches: skirting is being removed instead.
- Hanging strip for anchoring: anti-tip brackets through the top panel instead.

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



## 9. Status

Progress: ⬜ unblocked · 🛑 blocked · 🔄 in progress · ✅ done · ❓ undecided · ⏸️ paused · 🚫 not doing

- ✅ Design confirmed
- ⬜ Setup and justfile ([6.2](#62-setup-and-commands))
- ⬜ Settings and model ([6.3](#63-settings), [6.4](#64-model))
- ⬜ Model checks ([7](#7-quality))
- ⬜ STEP, STL and front view ([6.5](#65-outputs))
- ⬜ Packing, packer tests and material spec ([6.6](#66-packing), [7](#7-quality), [6.5](#65-outputs))
- ⬜ Sheet diagrams ([6.5](#65-outputs))
- ⬜ Assembly instructions ([6.5](#65-outputs))
- ⬜ Real prices: cutting quote, saw width, hardware, delivery ([4](#4-materials-and-cost))

