"""Application configuration constants for the Wardrobe Planner."""

# Application metadata
APP_NAME = "Wardrobe Planner"
VERSION = "1.0.0"
FILE_EXTENSION = ".wdp"

# Default frame dimensions (in millimeters)
DEFAULT_FRAME_WIDTH = 4800.0
DEFAULT_FRAME_HEIGHT = 2400.0
DEFAULT_FRAME_DEPTH = 600.0

# Default panel thickness (in millimeters)
DEFAULT_PANEL_THICKNESS = 18.0

# Default colors for different component types (hex color codes)
DEFAULT_COLORS = {
    "frame": "#8B4513",           # Saddle brown for frame
    "panel": "#DEB887",           # Burlywood for panels
    "shelf": "#D2B48C",           # Tan for shelves
    "divider": "#BC8F8F",         # Rosy brown for dividers
    "drawer": "#F4A460",          # Sandy brown for drawers
    "door": "#CD853F",            # Peru for doors
    "rail": "#A0A0A0",            # Gray for hanging rails
    "background": "#FFFFFF",      # White background
    "selection": "#0078D7",       # Blue for selection highlight
    "hover": "#ADD8E6",           # Light blue for hover state
}

# Minimum and maximum dimension constraints (in millimeters)
MIN_FRAME_WIDTH = 300.0
MAX_FRAME_WIDTH = 6000.0
MIN_FRAME_HEIGHT = 300.0
MAX_FRAME_HEIGHT = 3000.0
MIN_FRAME_DEPTH = 200.0
MAX_FRAME_DEPTH = 1000.0

# UI settings
DEFAULT_ZOOM_LEVEL = 1.0
MIN_ZOOM_LEVEL = 0.1
MAX_ZOOM_LEVEL = 5.0
ZOOM_STEP = 0.1

# Undo/Redo settings
MAX_UNDO_HISTORY = 50
