build:
    uv run src/model.py
    rsvg-convert -b white -z 2 build/sheets/all.svg -o build/sheets/all.png

check:
    uvx ruff format --check
    uvx ruff check
    uvx basedpyright
    uvx typos
    just --fmt --check --unstable
    uv run pytest

view:
    @#code --install-extension bernhard-42.ocp-cad-viewer
    uv run src/model.py --view
