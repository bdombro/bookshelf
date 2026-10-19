# AGENTS.md

Parametric model of two laminated pine bookshelves (Build123d, uv). Generates STEP/STL, a front view, a material spec with cost, sheet cutting diagrams and assembly instructions.

## Spec

- docs/spec.md is the source of truth and a requirements spec: what to build, the rules the design follows and why, what the software must produce
- It describes the current state; when anything pivots, update the section it belongs to in the same change; state each fact once
- No generated figures or product details: part sizes, heights, sheet counts, sheet use, cut counts, product names, prices, links, totals live in build/ and config.py. The spec says what an item must be; a setting's value may appear with the reason it was picked
- No research notes: supplier stock checks, "X doesn't sell Y", dated lookups, review counts. Report those in chat
- Coding conventions and process live here, not in the spec
- Log a replaced option under its Decisions group in one line, option then why it lost; merge superseded chains; never delete silently
- Keep its Status list current as work lands
- After a build, check the spec's rules still match the model and outputs; fix whichever is wrong

## Commands

- just build: model, checks, all outputs to build/
- just check: ruff format check, ruff lint, basedpyright (standard mode), typos via uvx; just --fmt --check; uv run pytest
- Tool settings (ruff rules, basedpyright) live in pyproject.toml; fix lint findings rather than adding ignores, except targeted OCP typing ignores
- just view: build and open in OCP CAD Viewer
- uv only: uv add / uv add --dev; never pip; commit uv.lock

## Code structure

- Code lives in src/bookshelf/, tests in tests/; root holds only config, docs and build/
- As many files and folders as keep the code well organized; each module has one clear job and a short docstring
- Settings modules hold only values a person would change, no logic; functions take settings as arguments instead of importing them
- Packing and text-output code never import build123d or read the settings modules; they take Part and Hardware rows (NamedTuples) and settings as arguments
- Instruction prose lives in outputs/templates/instructions.md.j2; Python only computes the values it prints
- Each module opens with a short docstring: purpose, inputs, outputs, spec section it implements
- The packer is a few small functions (pack strips, try orderings, self-check), each with a one-line docstring

## Code style

- Settings: lowercase module-level variables in src/bookshelf/settings/, in cm with a short comment, read as settings.name; multiply by CM when building
- No UPPER_CASE names; derived sizes are lowercase too
- When a value was picked for sheet yield or another constraint, its comment says so (e.g. `# 3 shelves per 243cm strip`)
- Part names use the spec's words, unabbreviated (side, divider, shelf, cabinet_top, kickboard), and match across code, labels, materials.md and instructions.md
- Formatting and lint belong to ruff; don't hand-format or debate style
- No magic numbers outside settings/; derive from settings. Drawing-only constants (SVG scale, the gap between units) stay where they're used
- One tuple per sheet or product in settings/catalog.py, (…, price, link), splatted into its row; never split one item across several settings
- Build123d algebra mode, Box with align=Align.MIN, every part labeled
- Type hints on functions; inference elsewhere
- Comments: terse what, never mechanics or change history
- Inline by default; extract only when reused or self-contained
- New settings or list entries go below existing ones in their group; new objects alphabetical

## Quality control

- Run just check and just build after every code change; both must pass
- Model checks in model/checks.py cover geometry: bounding box, no overlaps, every panel fits a sheet along the grain; extend them, and add a test in tests/test_checks.py that fails on settings breaking the new check
- A spec requirement the build can verify becomes a check, its limit a setting; prefer that over a rule here
- The packer verifies its own result: every part placed once, within the usable sheet, no overlaps, kerf respected
- Packer tests: the self-check must reject each kind of broken layout; add a test when the self-check gains a rule
- Check tests override single settings with settings.load(name=value); never copy source to try a setting
- Check failures print actual vs expected values
- Never edit build/; regenerate it. build/materials.md and build/instructions.md are committed so output changes show in review; regenerate them before every commit
- One spec Status item per commit; end each change with a 2–3 line summary of which numbers moved (sheets, cost, sizes, heights)
- After a geometry change, look at build/front.svg and build/sheets/
- Call out any change that raises cost before continuing. If the build fails the sheet limit, improve the packer first; raise max_sheets only when the user accepts the cost

## Real-world constraints

- Grain: every pine part's length runs along the sheet's 244cm length
- Kerf and edge trim are settings; the saw width warning stays in materials.md
- Never drop anchoring or anti-tip brackets from instructions or hardware
- Prices are placeholders until replaced with quotes; label estimates as estimates
