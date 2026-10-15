# Bookshelf

Plans for four built-in-style bookshelves in laminated pine: two sets either side of a
fireplace, each a narrow open unit next to a wide unit with a 2-door cabinet below.
Everything needed to buy, cut and assemble them is generated from one parametric model.

## The design

With help from Gemini:
![Bookshelf front elevation](docs/target-design-by-gemini.png)

- **Layout:** narrow, wide | 160cm fireplace | wide, narrow. 391.2cm overall.
- **Size:** 213cm tall, 29.5cm-deep shelves, recessed 10cm kickboard.
- **Wide units (83.6cm):** 4 open compartments over a cabinet with an inside shelf and
  two soft-close doors. Cabinet top at 87cm.
- **Narrow units (32cm):** 6 open compartments, lined up with the wide units' shelves.
- **Materials:** 24mm laminated pine panels, 4mm birch plywood backs glued and stapled.
- **Cost:** about €800 before delivery: 4 pine and 2 birch sheets (€525.58), about €75
  of cutting and about €200 of hardware and finish. Prices are estimates until quoted.

## What it produces

3d models, cutting diagrams, parts list, and assembly instructions.

![Bookshelf 3D model](docs/3d-render.webp)

Run `just build`; everything lands in `build/`:

| File | What it's for |
| --- | --- |
| [`materials.md`](build/materials.md) | Parts list, sheets to buy, hardware and cost |
| [`instructions.md`](build/instructions.md) | Step-by-step build: cutting list per sheet, shelf marking heights, screw positions, squaring diagonals, hinges, install |
| `sheets/*.svg` | One cutting diagram per sheet, with part labels, sizes and grain direction |
| `sheets/all.svg`, `all.png` | Every sheet stacked in one image, handy to print for cutting day |
| `front.svg` | Front elevation of both sets |
| `bookshelf.step` | Full 3D model with named, coloured panels for CAD tools (FreeCAD, Fusion, Onshape) |
| `bookshelf.stl` | 3D mesh for quick previews or a scale print |

Only `materials.md` and `instructions.md` are committed; regenerate the rest with
`just build`.

## Changing the design

Every size, price and setting is in [`src/config.py`](src/config.py): unit widths,
heights, cabinet height, saw width, sheet prices and so on. Change a value, run
`just build`, and the cutting list, cost and instructions all follow. Most sizes were
picked so everything fits on 4 pine sheets; the build reports the sheet count, so a
change that needs a 5th sheet is obvious.

Before cutting, check your saw blade's width and set `kerf` to match.

## How it's made

- **AI Assisted App Spec:** [`docs/spec.md`](docs/spec.md) records the full design, why each choice was
  made, and the options that were rejected, and how to build the app.
- **Requirements:** [uv](https://docs.astral.sh/uv/), [just](https://just.systems/) and
  librsvg (`brew install librsvg`) for the PNG. uv installs Python 3.12 and the
  dependencies on first run.
- **Commands:** `just build` generates everything; `just check` runs formatting, lint,
  type checks, spelling and tests; `just view` opens the model in the
  [OCP CAD Viewer](https://marketplace.visualstudio.com/items?itemName=bernhard-42.ocp-cad-viewer)
  VS Code extension (open its viewer first).
- **How it works:** [`src/model.py`](src/model.py) builds each panel as a box in
  [Build123d](https://github.com/gumyr/build123d), checks the model (overall size, no
  overlapping panels, every panel fits a sheet along the grain) and exports the 3D files
  and front view. [`src/materials.py`](src/materials.py) packs the panels onto sheets
  the way a panel saw cuts (rip strips, then crosscut), keeping the grain along each
  part's length; it tries many orderings, keeps the fewest sheets and verifies the
  result before writing the cutting list and diagrams.
  [`src/instructions.py`](src/instructions.py) fills in the assembly steps with the
  model's numbers.

## How this app was made

1. Start with image gen: Gemini posting and image of current space and ask it to remove what's currently there. Then ask it for ideas, more ideas, tell it which I like and why, more ideas, …. This took like 1.5 hours of back and forth with Gemini.

2. Refine goals, approaches, constraints, make a fancy plan generator app with Claude Code. 

Starting Prompt:
```txt
goal: help me create an app spec to to make 4 natural wood, quality, simple bookshelves based on 2 designs

Design 1: a 2.5’ wide, 7ft tall, 12” deep, 2 doors lower, 4 compartments above

Design 2: 1ft wide, 7ft tall, 12” deep, 6 compartments

Outputs:

- generate models using the most suitable, ai friendly OSS cad lib
- build instructions
- materials list
- cut guides 
```

...chat for like 4 hours to refining.

And then, only then, did I tell it to actually implement the app
