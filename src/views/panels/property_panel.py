"""Property panel for editing selected component properties."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox,
    QGroupBox, QFormLayout, QPushButton, QCheckBox
)
from PySide6.QtCore import Signal

from ...models.component import Component
from ...models.drawer import DrawerUnit
from ...models.hanging import HangingSpace
from ...models.shelf import Shelf
from ...models.overhead import Overhead


class PropertyPanel(QWidget):
    """Panel for viewing and editing component properties."""

    property_changed = Signal()
    delete_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_component = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Title
        self.title_label = QLabel("Properties")
        self.title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(self.title_label)

        # No selection message
        self.no_selection = QLabel("No component selected")
        self.no_selection.setStyleSheet("color: #666;")
        layout.addWidget(self.no_selection)

        # Properties container
        self.props_widget = QWidget()
        props_layout = QVBoxLayout(self.props_widget)
        props_layout.setContentsMargins(0, 0, 0, 0)

        # Basic properties group
        basic_group = QGroupBox("Dimensions")
        basic_form = QFormLayout(basic_group)

        self.name_edit = QLineEdit()
        self.name_edit.textChanged.connect(self._on_property_changed)
        basic_form.addRow("Name:", self.name_edit)

        self.width_spin = QDoubleSpinBox()
        self.width_spin.setRange(50, 5000)
        self.width_spin.setSuffix(" mm")
        self.width_spin.valueChanged.connect(self._on_property_changed)
        basic_form.addRow("Width:", self.width_spin)

        self.height_spin = QDoubleSpinBox()
        self.height_spin.setRange(50, 5000)
        self.height_spin.setSuffix(" mm")
        self.height_spin.valueChanged.connect(self._on_property_changed)
        basic_form.addRow("Height:", self.height_spin)

        self.depth_spin = QDoubleSpinBox()
        self.depth_spin.setRange(50, 1000)
        self.depth_spin.setSuffix(" mm")
        self.depth_spin.valueChanged.connect(self._on_property_changed)
        basic_form.addRow("Depth:", self.depth_spin)

        props_layout.addWidget(basic_group)

        # Position group
        pos_group = QGroupBox("Position")
        pos_form = QFormLayout(pos_group)

        self.x_spin = QDoubleSpinBox()
        self.x_spin.setRange(0, 5000)
        self.x_spin.setSuffix(" mm")
        self.x_spin.valueChanged.connect(self._on_property_changed)
        pos_form.addRow("X:", self.x_spin)

        self.y_spin = QDoubleSpinBox()
        self.y_spin.setRange(0, 5000)
        self.y_spin.setSuffix(" mm")
        self.y_spin.valueChanged.connect(self._on_property_changed)
        pos_form.addRow("Y:", self.y_spin)

        props_layout.addWidget(pos_group)

        # Type-specific properties (will be populated dynamically)
        self.specific_group = QGroupBox("Component Settings")
        self.specific_layout = QFormLayout(self.specific_group)
        props_layout.addWidget(self.specific_group)

        # Label
        label_group = QGroupBox("Display")
        label_form = QFormLayout(label_group)

        self.label_edit = QLineEdit()
        self.label_edit.textChanged.connect(self._on_property_changed)
        label_form.addRow("Label:", self.label_edit)

        self.locked_check = QCheckBox("Locked")
        self.locked_check.stateChanged.connect(self._on_property_changed)
        label_form.addRow("", self.locked_check)

        props_layout.addWidget(label_group)

        # Delete button
        self.delete_btn = QPushButton("Delete Component")
        self.delete_btn.setStyleSheet("background-color: #ffcccc;")
        self.delete_btn.clicked.connect(self.delete_requested)
        props_layout.addWidget(self.delete_btn)

        props_layout.addStretch()

        layout.addWidget(self.props_widget)
        self.props_widget.hide()

    def set_component(self, component: Component):
        """Set the component to edit."""
        self._current_component = component

        if component is None:
            self.no_selection.show()
            self.props_widget.hide()
            return

        self.no_selection.hide()
        self.props_widget.show()

        # Block signals during update
        self._block_signals(True)

        self.name_edit.setText(component.name)
        self.width_spin.setValue(component.dimensions.width)
        self.height_spin.setValue(component.dimensions.height)
        self.depth_spin.setValue(component.dimensions.depth)
        self.x_spin.setValue(component.position.x)
        self.y_spin.setValue(component.position.y)
        self.label_edit.setText(component.label)
        self.locked_check.setChecked(component.locked)

        self._update_specific_properties(component)

        self._block_signals(False)

    def _update_specific_properties(self, component):
        """Update type-specific property fields."""
        # Clear existing specific widgets
        while self.specific_layout.count():
            item = self.specific_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if isinstance(component, DrawerUnit):
            self.specific_group.setTitle("Drawer Settings")
            count_spin = QSpinBox()
            count_spin.setRange(1, 10)
            count_spin.setValue(component.drawer_count)
            self.specific_layout.addRow("Drawers:", count_spin)

        elif isinstance(component, HangingSpace):
            self.specific_group.setTitle("Hanging Settings")
            rail_combo = QComboBox()
            rail_combo.addItems(["single", "double"])
            rail_combo.setCurrentText(component.rail_type)
            self.specific_layout.addRow("Rail Type:", rail_combo)

        elif isinstance(component, Overhead):
            self.specific_group.setTitle("Overhead Settings")
            door_spin = QSpinBox()
            door_spin.setRange(1, 4)
            door_spin.setValue(component.door_count)
            self.specific_layout.addRow("Doors:", door_spin)

        self.specific_group.setVisible(self.specific_layout.count() > 0)

    def _block_signals(self, block: bool):
        """Block/unblock signals from all input widgets."""
        for widget in [self.name_edit, self.width_spin, self.height_spin,
                      self.depth_spin, self.x_spin, self.y_spin,
                      self.label_edit, self.locked_check]:
            widget.blockSignals(block)

    def _on_property_changed(self):
        """Handle property value changes."""
        if self._current_component is None:
            return

        self._current_component.name = self.name_edit.text()
        self._current_component.dimensions.width = self.width_spin.value()
        self._current_component.dimensions.height = self.height_spin.value()
        self._current_component.dimensions.depth = self.depth_spin.value()
        self._current_component.position.x = self.x_spin.value()
        self._current_component.position.y = self.y_spin.value()
        self._current_component.label = self.label_edit.text()
        self._current_component.locked = self.locked_check.isChecked()

        self.property_changed.emit()

    def clear(self):
        """Clear the panel."""
        self.set_component(None)
