"""Graphics item for drawer units."""
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPen, QColor, QPainter

from .base_item import BaseWardrobeItem
from ...models.drawer import DrawerUnit


class DrawerItem(BaseWardrobeItem):
    """Visual representation of a drawer unit."""

    def __init__(self, component: DrawerUnit, parent=None):
        super().__init__(component, parent)
        self._fill_color = QColor("#E8D5B7")  # Light wood color
        self.setBrush(self._fill_color)

    def paint(self, painter: QPainter, option, widget=None):
        super().paint(painter, option, widget)

        # Draw individual drawers
        rect = self.rect()
        drawer_unit: DrawerUnit = self.component
        offset = self._get_depth_offset()

        drawer_pen = QPen(QColor("#8B7355"), 1)
        painter.setPen(drawer_pen)

        y = rect.bottom()
        for i, height in enumerate(drawer_unit.drawer_heights):
            y -= height
            # Drawer line on front face
            painter.drawLine(int(rect.left()), int(y), int(rect.right()), int(y))

            # Handle
            handle_y = y + height / 2
            handle_width = 40 if drawer_unit.handle_style == "bar" else 10
            handle_x = rect.center().x() - handle_width / 2

            painter.drawRect(QRectF(handle_x, handle_y - 3, handle_width, 6))

        # Extend drawer lines onto the 3D right face
        if offset > 0:
            perspective_pen = QPen(QColor("#6B5335"), 1)
            painter.setPen(perspective_pen)

            y = rect.bottom()
            for height in drawer_unit.drawer_heights:
                y -= height
                # Line from front-right edge to projected point at 45 degrees
                painter.drawLine(
                    int(rect.right()), int(y),
                    int(rect.right() + offset), int(y + offset)
                )
