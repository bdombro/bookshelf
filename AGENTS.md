# AGENTS.md

Parametric model of four laminated pine bookshelves (Build123d, uv). Generates STEP/STL, a front view, a material spec with cost, sheet cutting diagrams and assembly instructions.

## Spec

- docs/spec.md is the source of truth: design, materials, cost, software
- It describes the current state; when anything pivots, update the section it belongs to in the same change, plus the at-a-glance summary and any repeated numbers
- Log the replaced option and why under its Decisions section; never delete silently
- Keep its Status list current as work lands
- After a build, compare spec figures (sheet counts, cost, panel sizes, heights) with build/materials.md and build/instructions.md; fix whichever is wrong

## Commands

- just build: model, checks, all outputs to build/
- just check: ruff format check, ruff lint, basedpyright (standard mode), typos via uvx; just --fmt --check; uv run pytest
- Tool settings (ruff rules, basedpyright) live in pyproject.toml; fix lint findings rather than adding ignores, except targeted OCP typing ignores
- just view: build and open in OCP CAD Viewer
- uv only: uv add / uv add --dev; never pip; commit uv.lock

## Code structure

- Code lives in src/ (plain folder, not a package), packer tests in tests/test_materials.py; root holds only config, docs and build/
- Four files only: src/config.py (settings), src/model.py (model), src/materials.py (packing, cost, spec, diagrams), src/instructions.py (instructions.md); new files need a strong reason
- config.py holds only values a person would change, no logic; only model.py imports it
- materials.py and instructions.py never import build123d or config; they take Part and Hardware rows (NamedTuples defined in materials.py) and settings as arguments from model.py
- model.py reads top to bottom: derived sizes, unit(), layout, checks, exports; no main()
- unit(width, cabinet) is the only function in model.py
- Each script opens with a short docstring: purpose, inputs, outputs, spec section it implements
- model.py has a banner comment per section, in the order above
- The packer is a few small functions (pack strips, try orderings, self-check), each with a one-line docstring

## Code style

- Settings: lowercase module-level variables in config.py, in cm with a short comment, read as config.name; multiply by CM when building
- No UPPER_CASE names; derived sizes in model.py are lowercase too
- When a value was picked for sheet yield or another constraint, its comment says so (e.g. `# 3 shelves per 243cm strip`)
- Part names use the spec's words, unabbreviated (side, shelf, cabinet_top, kickboard), and match across code, labels, materials.md and instructions.md
- Formatting and lint belong to ruff; don't hand-format or debate style
- No magic numbers outside config.py; derive from settings
- Build123d algebra mode, Box with align=Align.MIN, every part labeled
- Type hints on functions; inference elsewhere
- Comments: terse what, never mechanics or change history
- Inline by default; extract only when reused or self-contained
- New settings or list entries go below existing ones in their group; new objects alphabetical

## Quality control

- Run just check and just build after every code change; both must pass
- Model checks in model.py cover geometry: bounding box, no overlaps, every panel fits a sheet along the grain; extend them rather than adding geometry unit tests
- The packer verifies its own result: every part placed once, within the usable sheet, no overlaps, kerf respected
- Unit tests cover the packer only: the self-check must reject each kind of broken layout; add a test when the self-check gains a rule
- Check failures print actual vs expected values
- Never edit build/; regenerate it. build/materials.md and build/instructions.md are committed so output changes show in review; regenerate them before every commit
- One spec Status item per commit; end each change with a 2–3 line summary of which numbers moved (sheets, cost, sizes, heights)
- After a geometry change, look at build/front.svg and build/sheets/
- Call out any change that raises sheet count or cost before continuing; more than 4 pine sheets with the defaults means fix the packer

## Real-world constraints

- Grain: every pine part's length runs along the sheet's 244cm length
- Kerf and edge trim are settings; the saw width warning stays in materials.md
- Never drop anchoring, anti-tip brackets or set bolts from instructions or hardware
- Prices are placeholders until replaced with quotes; label estimates as estimates
