"""Settings as one namespace, so tests and callers can override single values.

Inputs: design.py and catalog.py, plus optional overrides by name.
Outputs: a Settings namespace read as settings.name.
Implements spec 6.3 (Settings).
"""

from types import ModuleType, SimpleNamespace

from bookshelf.settings import catalog, design

Settings = SimpleNamespace


def values(module: ModuleType) -> dict[str, object]:
    """A settings module's public values."""
    return {k: v for k, v in vars(module).items() if not k.startswith("_")}


def load(**overrides: object) -> Settings:
    """The settings files' values with any named overrides applied."""
    found = {**values(design), **values(catalog)}
    unknown = sorted(set(overrides) - set(found))
    if unknown:
        raise ValueError(f"unknown settings {unknown}, expected names in settings/")
    return Settings(**{**found, **overrides})
