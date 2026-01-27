"""Graphics item for overhead cabinets."""
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPen, QColor, QPainter

from .base_item import BaseWardrobeItem
from ...models.overhead import Overhead


class OverheadItem(BaseWardrobeItem):
    """Visual representation of an overhead cabinet."""

    def __init__(self, component: Overhead, parent=None):
        super().__init__(component, parent)
        self._fill_color = QColor("#D4C4B0")  # Light wood
        self.setBrush(self._fill_color)

    def paint(self, painter: QPainter, option, widget=None):
        super().paint(painter, option, widget)

        overhead: Overhead = self.component
        rect = self.rect()

        door_pen = QPen(QColor("#8B7355"), 2)
        painter.setPen(door_pen)

        # Draw door divisions
        door_width = rect.width() / overhead.door_count
        for i in range(1, overhead.door_count):
            x = rect.left() + i * door_width
            painter.drawLine(int(x), int(rect.top()), int(x), int(rect.bottom()))

        # Draw handles on each door
        handle_y = rect.center().y()
        for i in range(overhead.door_count):
            door_center_x = rect.left() + (i + 0.5) * door_width
            handle_x = door_center_x - 5
            painter.drawRect(QRectF(handle_x, handle_y - 15, 10, 30))

        # Draw internal shelf line if present
        if overhead.has_shelf:
            shelf_y = rect.center().y()
            dash_pen = QPen(QColor("#999999"), 1)
            dash_pen.setStyle(Qt.DashLine)
            painter.setPen(dash_pen)
            painter.drawLine(int(rect.left() + 5), int(shelf_y),
                            int(rect.right() - 5), int(shelf_y))
