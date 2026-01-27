"""Graphics item for hanging spaces."""
from PySide6.QtCore import QRectF
from PySide6.QtGui import QPen, QColor, QPainter

from .base_item import BaseWardrobeItem
from ...models.hanging import HangingSpace


class HangingItem(BaseWardrobeItem):
    """Visual representation of hanging space."""

    def __init__(self, component: HangingSpace, parent=None):
        super().__init__(component, parent)
        self._fill_color = QColor("#F5F0E6")  # Light cream
        self.setBrush(self._fill_color)

    def paint(self, painter: QPainter, option, widget=None):
        super().paint(painter, option, widget)

        rect = self.rect()
        hanging: HangingSpace = self.component

        # Draw rail(s)
        rail_pen = QPen(QColor("#666666"), 3)
        painter.setPen(rail_pen)

        rail_y = rect.bottom() - hanging.rail_height + rect.top()
        if rail_y < rect.top():
            rail_y = rect.top() + 50

        margin = 20
        painter.drawLine(int(rect.left() + margin), int(rail_y),
                        int(rect.right() - margin), int(rail_y))

        # Draw rail supports
        painter.drawLine(int(rect.left() + margin), int(rail_y),
                        int(rect.left() + margin), int(rect.top()))
        painter.drawLine(int(rect.right() - margin), int(rail_y),
                        int(rect.right() - margin), int(rect.top()))

        # Second rail for double
        if hanging.rail_type == "double":
            rail_y2 = rail_y - 450  # Second rail below
            if rail_y2 > rect.bottom():
                rail_y2 = rect.bottom() - 50
            painter.drawLine(int(rect.left() + margin), int(rail_y2),
                            int(rect.right() - margin), int(rail_y2))
