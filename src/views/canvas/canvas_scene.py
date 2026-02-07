"""Graphics scene for the wardrobe canvas."""
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import Qt, Signal, QPointF
from PySide6.QtGui import QPen, QBrush, QColor, QPolygonF


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
        self.frame_depth = 600.0

        # Drop preview indicator
        self._drop_preview = None

        # 3D perspective items for the frame
        self._frame_top_face = None
        self._frame_right_face = None

        # Set scene rect with margin
        margin = 200
        self.setSceneRect(
            -margin, -margin,
            self.frame_width + 2 * margin,
            self.frame_height + 2 * margin
        )

        self.setBackgroundBrush(QBrush(QColor("#F5F5F5")))
        self._draw_frame()

    def _get_frame_depth_offset(self):
        """Calculate the 3D perspective depth offset for the frame."""
        return min(self.frame_depth * 0.12, 80)

    def _draw_frame(self):
        """Draw the wardrobe frame outline with 3D perspective."""
        frame_pen = QPen(QColor("#333333"), 3)
        frame_brush = QBrush(QColor("#FFFFFF"))

        self.frame_rect = self.addRect(
            0, 0, self.frame_width, self.frame_height,
            frame_pen, frame_brush
        )
        self.frame_rect.setZValue(-100)

        self._draw_frame_3d()

    def _draw_frame_3d(self):
        """Draw 3D perspective faces on the wardrobe frame."""
        offset = self._get_frame_depth_offset()
        if offset <= 0:
            return

        w = self.frame_width
        h = self.frame_height
        perspective_pen = QPen(QColor("#333333"), 2)

        # Top face (lighter gray)
        # In scene coords with Y-flip: y=h is the visual top
        top_face = QPolygonF([
            QPointF(0, h),              # visual top-left
            QPointF(w, h),              # visual top-right
            QPointF(w + offset, h + offset),   # projected top-right
            QPointF(offset, h + offset),       # projected top-left
        ])
        self._frame_top_face = self.addPolygon(
            top_face, perspective_pen, QBrush(QColor("#E8E8E8"))
        )
        self._frame_top_face.setZValue(-99)

        # Right face (darker gray)
        right_face = QPolygonF([
            QPointF(w, h),              # visual top-right
            QPointF(w, 0),              # visual bottom-right
            QPointF(w + offset, offset),       # projected bottom-right
            QPointF(w + offset, h + offset),   # projected top-right
        ])
        self._frame_right_face = self.addPolygon(
            right_face, perspective_pen, QBrush(QColor("#D0D0D0"))
        )
        self._frame_right_face.setZValue(-99)

    def _remove_frame_3d(self):
        """Remove existing 3D perspective items from the frame."""
        if self._frame_top_face is not None:
            self.removeItem(self._frame_top_face)
            self._frame_top_face = None
        if self._frame_right_face is not None:
            self.removeItem(self._frame_right_face)
            self._frame_right_face = None

    def set_frame_size(self, width: float, height: float, depth: float = None):
        """Update the wardrobe frame size."""
        self.frame_width = width
        self.frame_height = height
        if depth is not None:
            self.frame_depth = depth

        margin = 200
        self.setSceneRect(
            -margin, -margin,
            width + 2 * margin,
            height + 2 * margin
        )

        self.frame_rect.setRect(0, 0, width, height)

        # Redraw 3D perspective for new dimensions
        self._remove_frame_3d()
        self._draw_frame_3d()

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
