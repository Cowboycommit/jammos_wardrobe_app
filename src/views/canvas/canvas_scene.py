"""Graphics scene for the wardrobe canvas."""
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import Qt, Signal, QPointF
from PySide6.QtGui import QPen, QBrush, QColor


class CanvasScene(QGraphicsScene):
    """
    The graphics scene holding all wardrobe components.

    Coordinate System:
    - Origin (0,0) is at bottom-left of wardrobe frame
    - Y increases upward
    - Units are millimeters
    """

    component_added = Signal(object)
    component_removed = Signal(str)
    component_moved = Signal(str, float, float)
    selection_changed = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Wardrobe frame dimensions
        self.frame_width = 2400.0
        self.frame_height = 2400.0

        # Drop preview indicator
        self._drop_preview = None

        # Set scene rect with margin
        margin = 200
        self.setSceneRect(
            -margin, -margin,
            self.frame_width + 2 * margin,
            self.frame_height + 2 * margin
        )

        self.setBackgroundBrush(QBrush(QColor("#F5F5F5")))
        self._draw_frame()

    def _draw_frame(self):
        """Draw the wardrobe frame outline."""
        frame_pen = QPen(QColor("#333333"), 3)
        frame_brush = QBrush(QColor("#FFFFFF"))

        self.frame_rect = self.addRect(
            0, 0, self.frame_width, self.frame_height,
            frame_pen, frame_brush
        )
        self.frame_rect.setZValue(-100)

    def set_frame_size(self, width: float, height: float):
        """Update the wardrobe frame size."""
        self.frame_width = width
        self.frame_height = height

        margin = 200
        self.setSceneRect(
            -margin, -margin,
            width + 2 * margin,
            height + 2 * margin
        )

        self.frame_rect.setRect(0, 0, width, height)
        self.update()

    def show_drop_preview(self, pos: QPointF, width: float, height: float):
        """Show a preview rectangle where a dropped component will land."""
        if self._drop_preview is None:
            preview_pen = QPen(QColor("#0066CC"), 2, Qt.DashLine)
            preview_brush = QBrush(QColor(0, 102, 204, 40))
            self._drop_preview = self.addRect(
                pos.x(), pos.y(), width, height,
                preview_pen, preview_brush
            )
            self._drop_preview.setZValue(1000)
        else:
            self._drop_preview.setRect(
                pos.x(), pos.y(), width, height
            )

    def hide_drop_preview(self):
        """Remove the drop preview rectangle."""
        if self._drop_preview is not None:
            self.removeItem(self._drop_preview)
            self._drop_preview = None
