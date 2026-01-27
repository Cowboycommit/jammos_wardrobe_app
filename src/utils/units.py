"""Unit conversion utilities for wardrobe measurements."""

MM_PER_INCH = 25.4
MM_PER_CM = 10.0

def mm_to_inches(mm: float) -> float:
    """Convert millimeters to inches."""
    return mm / MM_PER_INCH

def inches_to_mm(inches: float) -> float:
    """Convert inches to millimeters."""
    return inches * MM_PER_INCH

def mm_to_cm(mm: float) -> float:
    """Convert millimeters to centimeters."""
    return mm / MM_PER_CM

def cm_to_mm(cm: float) -> float:
    """Convert centimeters to millimeters."""
    return cm * MM_PER_CM

def format_dimension(mm: float, use_metric: bool = True, precision: int = 1) -> str:
    """Format dimension for display with unit suffix."""
    if use_metric:
        return f"{mm:.{precision}f} mm"
    else:
        inches = mm_to_inches(mm)
        return f"{inches:.{precision}f}\""

def parse_dimension(value_str: str) -> tuple[float, bool]:
    """
    Parse a dimension string to millimeters.
    Accepts: "500", "500mm", "50cm", "20\"", "20in"
    Returns: (value_in_mm, success)
    """
    value_str = value_str.strip().lower()
    try:
        if value_str.endswith("mm"):
            return float(value_str[:-2]), True
        elif value_str.endswith("cm"):
            return cm_to_mm(float(value_str[:-2])), True
        elif value_str.endswith('"') or value_str.endswith("in"):
            suffix_len = 1 if value_str.endswith('"') else 2
            return inches_to_mm(float(value_str[:-suffix_len])), True
        else:
            return float(value_str), True
    except ValueError:
        return 0.0, False
