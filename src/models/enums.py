from enum import Enum, auto


class ComponentType(Enum):
    """Types of wardrobe components."""
    FRAME = auto()
    DRAWER_UNIT = auto()
    HANGING_SPACE = auto()
    SHELF = auto()
    OVERHEAD = auto()
    DIVIDER = auto()


class UnitSystem(Enum):
    """Measurement unit systems."""
    METRIC = auto()   # Millimeters
    IMPERIAL = auto()  # Inches
