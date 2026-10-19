"""Number formatting shared by the model and the outputs.

Inputs: numbers. Outputs: strings.
Implements spec 6.5 (Outputs).
"""


def money(value: float) -> str:
    """Euro amount, or unknown for an unpriced 0."""
    return f"€{value:,.2f}" if value else "unknown"


def size(value: float) -> str:
    """A cm figure to 0.1cm, without a trailing .0."""
    return f"{value:.1f}".removesuffix(".0")
