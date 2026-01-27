"""Tool palette for selecting and placing wardrobe components."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QGroupBox, QGridLayout, QSizePolicy
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QDrag, QPixmap, QPainter, QColor

from ...models.enums import ComponentType


class ComponentButton(QPushButton):
    """Button representing a wardrobe component that can be dragged."""

    component_selected = Signal(ComponentType)

    def __init__(self, component_type: ComponentType, label: str, parent=None):
        super().__init__(label, parent)
        self.component_type = component_type
        self.setMinimumHeight(50)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet("""
            QPushButton {
                background-color: #E8E8E8;
                border: 2px solid #999;
                border-radius: 5px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #D0D0D0;
                border-color: #666;
            }
            QPushButton:pressed {
                background-color: #C0C0C0;
            }
        """)

        self.clicked.connect(self._on_clicked)

    def _on_clicked(self):
        self.component_selected.emit(self.component_type)

    def mouseMoveEvent(self, event):
        """Start drag operation when mouse moves with button pressed."""
        if event.buttons() & Qt.LeftButton:
            drag = QDrag(self)
            mime_data = drag.mimeData()
            mime_data.setText(self.component_type.name)

            # Create drag pixmap
            pixmap = QPixmap(100, 50)
            pixmap.fill(QColor("#D4A574"))
            painter = QPainter(pixmap)
            painter.setPen(QColor("#333"))
            painter.drawText(pixmap.rect(), Qt.AlignCenter, self.text())
            painter.end()

            drag.setPixmap(pixmap)
            drag.exec(Qt.CopyAction)


class ToolPalette(QWidget):
    """Panel containing component selection buttons."""

    component_selected = Signal(ComponentType)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        # Title
        title = QLabel("Components")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)

        # Storage components group
        storage_group = QGroupBox("Storage")
        storage_layout = QGridLayout(storage_group)

        drawer_btn = ComponentButton(ComponentType.DRAWER_UNIT, "Drawers")
        drawer_btn.component_selected.connect(self.component_selected)
        storage_layout.addWidget(drawer_btn, 0, 0)

        shelf_btn = ComponentButton(ComponentType.SHELF, "Shelf")
        shelf_btn.component_selected.connect(self.component_selected)
        storage_layout.addWidget(shelf_btn, 0, 1)

        overhead_btn = ComponentButton(ComponentType.OVERHEAD, "Overhead")
        overhead_btn.component_selected.connect(self.component_selected)
        storage_layout.addWidget(overhead_btn, 1, 0)

        layout.addWidget(storage_group)

        # Hanging components group
        hanging_group = QGroupBox("Hanging")
        hanging_layout = QGridLayout(hanging_group)

        hanging_btn = ComponentButton(ComponentType.HANGING_SPACE, "Hanging\nSpace")
        hanging_btn.component_selected.connect(self.component_selected)
        hanging_layout.addWidget(hanging_btn, 0, 0)

        layout.addWidget(hanging_group)

        # Structure components group
        structure_group = QGroupBox("Structure")
        structure_layout = QGridLayout(structure_group)

        divider_btn = ComponentButton(ComponentType.DIVIDER, "Divider")
        divider_btn.component_selected.connect(self.component_selected)
        structure_layout.addWidget(divider_btn, 0, 0)

        layout.addWidget(structure_group)

        # Spacer
        layout.addStretch()

        # Instructions
        instructions = QLabel("Click a component to place it,\nor drag onto the canvas.")
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(instructions)
