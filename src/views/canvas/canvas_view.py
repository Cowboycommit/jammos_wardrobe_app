"""Graphics view for the wardrobe canvas."""
from PySide6.QtWidgets import QGraphicsView
from PySide6.QtCore import Qt, Signal, QRectF, QPointF
from PySide6.QtGui import QPainter

from .canvas_scene import CanvasScene
from ...models.enums import ComponentType

# Default preview sizes for each component type (width, height in mm)
_COMPONENT_PREVIEW_SIZES = {
    ComponentType.DRAWER_UNIT: (600, 800),
    ComponentType.HANGING_SPACE: (800, 1800),
    ComponentType.SHELF: (800, 18),
    ComponentType.OVERHEAD: (800, 400),
    ComponentType.DIVIDER: (18, 2400),
}


class CanvasView(QGraphicsView):
    """The viewport for viewing and interacting with the canvas."""

    zoom_changed = Signal(float)
    component_dropped = Signal(ComponentType, float, float)  # type, x, y

    def __init__(self, parent=None):
        super().__init__(parent)

        self._zoom_level = 1.0
        self._min_zoom = 0.1
        self._max_zoom = 5.0

        # Set up scene
        self._scene = CanvasScene()
        self.setScene(self._scene)

        # View settings
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setAcceptDrops(True)

        # Flip Y axis so origin is at bottom-left
        self.scale(1, -1)

    @property
    def canvas_scene(self) -> CanvasScene:
        """Get the canvas scene."""
        return self._scene

    def wheelEvent(self, event):
        """Handle mouse wheel for zooming."""
        factor = 1.15
        if event.angleDelta().y() > 0:
            self.zoom_in(factor)
        else:
            self.zoom_out(factor)

    def zoom_in(self, factor=1.25):
        """Zoom in on the canvas."""
        new_zoom = self._zoom_level * factor
        if new_zoom <= self._max_zoom:
            self.scale(factor, factor)
            self._zoom_level = new_zoom
            self.zoom_changed.emit(self._zoom_level)

    def zoom_out(self, factor=1.25):
        """Zoom out from the canvas."""
        new_zoom = self._zoom_level / factor
        if new_zoom >= self._min_zoom:
            self.scale(1/factor, 1/factor)
            self._zoom_level = new_zoom
            self.zoom_changed.emit(self._zoom_level)

    def fit_to_frame(self):
        """Fit the wardrobe frame in view."""
        frame_rect = QRectF(
            0, 0,
            self._scene.frame_width,
            self._scene.frame_height
        )
        self.fitInView(frame_rect, Qt.KeepAspectRatio)
        # Update zoom level
        self._zoom_level = self.transform().m11()
        self.zoom_changed.emit(self._zoom_level)

    def reset_zoom(self):
        """Reset to 1:1 zoom."""
        self.resetTransform()
        self.scale(1, -1)  # Maintain Y-flip
        self._zoom_level = 1.0
        self.zoom_changed.emit(self._zoom_level)

    def get_zoom_level(self) -> float:
        """Get current zoom level."""
        return self._zoom_level

    def set_grid_visible(self, visible: bool):
        """Show or hide the grid."""
        self._scene.set_grid_visible(visible)

    def set_snap_enabled(self, enabled: bool):
        """Enable or disable snap to grid."""
        self._scene.set_snap_enabled(enabled)

    def _parse_component_type(self, mime_text: str):
        """Parse component type from drag mime data."""
        try:
            return ComponentType[mime_text]
        except (KeyError, ValueError):
            return None

    def dragEnterEvent(self, event):
        """Accept drag if it carries a component type."""
        mime = event.mimeData()
        if mime and mime.hasText() and self._parse_component_type(mime.text()):
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        """Show snap preview as drag moves over the canvas."""
        mime = event.mimeData()
        if not mime or not mime.hasText():
            super().dragMoveEvent(event)
            return

        comp_type = self._parse_component_type(mime.text())
        if comp_type is None:
            super().dragMoveEvent(event)
            return

        event.acceptProposedAction()

        # Map viewport position to scene coordinates
        scene_pos = self.mapToScene(event.position().toPoint())
        w, h = _COMPONENT_PREVIEW_SIZES.get(comp_type, (600, 400))
        self._scene.show_drop_preview(scene_pos, w, h)

    def dragLeaveEvent(self, event):
        """Hide preview when drag leaves the canvas."""
        self._scene.hide_drop_preview()
        super().dragLeaveEvent(event)

    def dropEvent(self, event):
        """Handle component drop - emit signal with type and snapped position."""
        mime = event.mimeData()
        if not mime or not mime.hasText():
            super().dropEvent(event)
            return

        comp_type = self._parse_component_type(mime.text())
        if comp_type is None:
            super().dropEvent(event)
            return

        self._scene.hide_drop_preview()

        # Map to scene coordinates and snap
        scene_pos = self.mapToScene(event.position().toPoint())
        snapped = self._scene.snap_position(scene_pos)

        event.acceptProposedAction()
        self.component_dropped.emit(comp_type, snapped.x(), snapped.y())
