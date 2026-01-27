"""Graphics view for the wardrobe canvas."""
from PySide6.QtWidgets import QGraphicsView
from PySide6.QtCore import Qt, Signal, QRectF
from PySide6.QtGui import QPainter

from .canvas_scene import CanvasScene


class CanvasView(QGraphicsView):
    """The viewport for viewing and interacting with the canvas."""

    zoom_changed = Signal(float)

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
