"""Utility modules for the Wardrobe Planner application."""

from .units import (
    MM_PER_INCH,
    MM_PER_CM,
    mm_to_inches,
    inches_to_mm,
    mm_to_cm,
    cm_to_mm,
    format_dimension,
    parse_dimension,
)

from .geometry import (
    point_in_rect,
    rects_intersect,
    snap_to_grid,
    calculate_scale_to_fit,
    rect_contains_rect,
    clamp,
)

from .config import (
    APP_NAME,
    VERSION,
    FILE_EXTENSION,
    DEFAULT_GRID_SIZE,
    DEFAULT_FRAME_WIDTH,
    DEFAULT_FRAME_HEIGHT,
    DEFAULT_FRAME_DEPTH,
    DEFAULT_PANEL_THICKNESS,
    DEFAULT_COLORS,
    MIN_FRAME_WIDTH,
    MAX_FRAME_WIDTH,
    MIN_FRAME_HEIGHT,
    MAX_FRAME_HEIGHT,
    MIN_FRAME_DEPTH,
    MAX_FRAME_DEPTH,
    DEFAULT_ZOOM_LEVEL,
    MIN_ZOOM_LEVEL,
    MAX_ZOOM_LEVEL,
    ZOOM_STEP,
    SNAP_TOLERANCE,
    MAX_UNDO_HISTORY,
)

__all__ = [
    # Unit conversion
    "MM_PER_INCH",
    "MM_PER_CM",
    "mm_to_inches",
    "inches_to_mm",
    "mm_to_cm",
    "cm_to_mm",
    "format_dimension",
    "parse_dimension",
    # Geometry
    "point_in_rect",
    "rects_intersect",
    "snap_to_grid",
    "calculate_scale_to_fit",
    "rect_contains_rect",
    "clamp",
    # Config - App metadata
    "APP_NAME",
    "VERSION",
    "FILE_EXTENSION",
    # Config - Defaults
    "DEFAULT_GRID_SIZE",
    "DEFAULT_FRAME_WIDTH",
    "DEFAULT_FRAME_HEIGHT",
    "DEFAULT_FRAME_DEPTH",
    "DEFAULT_PANEL_THICKNESS",
    "DEFAULT_COLORS",
    # Config - Constraints
    "MIN_FRAME_WIDTH",
    "MAX_FRAME_WIDTH",
    "MIN_FRAME_HEIGHT",
    "MAX_FRAME_HEIGHT",
    "MIN_FRAME_DEPTH",
    "MAX_FRAME_DEPTH",
    # Config - UI settings
    "DEFAULT_ZOOM_LEVEL",
    "MIN_ZOOM_LEVEL",
    "MAX_ZOOM_LEVEL",
    "ZOOM_STEP",
    "SNAP_TOLERANCE",
    "MAX_UNDO_HISTORY",
]
