"""Graphics item for shelves."""
from PySide6.QtCore import QRectF
from PySide6.QtGui import QPen, QBrush, QColor, QPainter

from .base_item import BaseWardrobeItem
from ...models.shelf import Shelf


class ShelfItem(BaseWardrobeItem):
    """Visual representation of a shelf."""

    def __init__(self, component: Shelf, parent=None):
        super().__init__(component, parent)
        self._fill_color = QColor("#D4A574")  # Wood color
        self.setBrush(self._fill_color)

    def paint(self, painter: QPainter, option, widget=None):
        super().paint(painter, option, widget)

        shelf: Shelf = self.component
        rect = self.rect()

        # Draw edge banding line
        edge_pen = QPen(QColor("#8B6914"), 2)
        painter.setPen(edge_pen)
        painter.drawLine(int(rect.left()), int(rect.bottom()),
                        int(rect.right()), int(rect.bottom()))
