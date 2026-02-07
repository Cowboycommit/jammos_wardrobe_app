"""Base graphics item for wardrobe components."""
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsItem, QStyleOptionGraphicsItem
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPen, QBrush, QColor, QPainter, QFont

from ...models.component import Component


class BaseWardrobeItem(QGraphicsRectItem):
    """Base class for all wardrobe component graphics items."""

    def __init__(self, component: Component, parent=None):
        super().__init__(parent)

        self.component = component
        self._resize_handle_size = 10
        self._is_dragging = False

        # Set position and size from model
        self.setRect(0, 0, component.dimensions.width, component.dimensions.height)
        self.setPos(component.position.x, component.position.y)

        # Item flags
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, not component.locked)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)

        # Appearance
        self._default_pen = QPen(QColor("#333333"), 2)
        self._selected_pen = QPen(QColor("#0066CC"), 3)
        self._drag_pen = QPen(QColor("#0066CC"), 2, Qt.DashLine)
        self._fill_color = QColor(component.color)

        self.setPen(self._default_pen)
        self.setBrush(QBrush(self._fill_color))

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget=None):
        """Custom painting with selection highlight and labels."""
        # Draw base rectangle
        if self._is_dragging:
            painter.setPen(self._drag_pen)
            drag_fill = QColor(self._fill_color)
            drag_fill.setAlpha(180)
            painter.setBrush(QBrush(drag_fill))
        elif self.isSelected():
            painter.setPen(self._selected_pen)
            painter.setBrush(self.brush())
        else:
            painter.setPen(self._default_pen)
            painter.setBrush(self.brush())

        painter.drawRect(self.rect())

        # Draw label (flip for readability since Y is inverted)
        self._draw_label(painter)

        # Draw resize handles if selected
        if self.isSelected():
            self._draw_resize_handles(painter)

    def _draw_label(self, painter: QPainter):
        """Draw component label."""
        label = self.component.label or self.component.name
        if not label:
            return

        painter.save()
        painter.scale(1, -1)  # Flip for readable text

        font = QFont("Arial", 10)
        painter.setFont(font)
        painter.setPen(QColor("#333333"))

        rect = self.rect()
        text_rect = QRectF(rect.x(), -rect.y() - rect.height(), rect.width(), rect.height())
        painter.drawText(text_rect, Qt.AlignCenter, label)
        painter.restore()

    def _draw_resize_handles(self, painter: QPainter):
        """Draw resize handles at corners."""
        handle_color = QColor("#0066CC")
        painter.setBrush(QBrush(handle_color))
        painter.setPen(Qt.NoPen)

        rect = self.rect()
        hs = self._resize_handle_size

        handles = [
            QRectF(rect.right() - hs, rect.top(), hs, hs),
            QRectF(rect.right() - hs, rect.bottom() - hs, hs, hs),
            QRectF(rect.left(), rect.bottom() - hs, hs, hs),
            QRectF(rect.left(), rect.top(), hs, hs),
        ]

        for handle in handles:
            painter.drawRect(handle)

    def mousePressEvent(self, event):
        """Track drag start."""
        if event.button() == Qt.LeftButton and not self.component.locked:
            self._is_dragging = True
            self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Track drag end."""
        if event.button() == Qt.LeftButton:
            self._is_dragging = False
            self.update()
        super().mouseReleaseEvent(event)

    def itemChange(self, change, value):
        """Handle item position changes."""
        if change == QGraphicsItem.ItemPositionHasChanged:
            self.component.position.x = value.x()
            self.component.position.y = value.y()
        return super().itemChange(change, value)

    def sync_from_model(self):
        """Update visual from model data."""
        self.setRect(0, 0, self.component.dimensions.width, self.component.dimensions.height)
        self.setPos(self.component.position.x, self.component.position.y)
        self._fill_color = QColor(self.component.color)
        self.setBrush(QBrush(self._fill_color))
        self.update()

    def sync_to_model(self):
        """Update model from visual state."""
        rect = self.rect()
        pos = self.pos()
        self.component.dimensions.width = rect.width()
        self.component.dimensions.height = rect.height()
        self.component.position.x = pos.x()
        self.component.position.y = pos.y()
