"""Main application window for the wardrobe planner."""
from PySide6.QtWidgets import (
    QMainWindow, QDockWidget, QToolBar, QStatusBar,
    QFileDialog, QMessageBox, QWidget, QVBoxLayout
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QKeySequence

from ..models.project import WardrobeProject
from ..services.file_service import FileService
from ..views.canvas import CanvasView
from ..views.panels.tool_palette import ToolPalette
from ..views.panels.property_panel import PropertyPanel
from ..models.enums import ComponentType
from ..models.drawer import DrawerUnit
from ..models.hanging import HangingSpace
from ..models.shelf import Shelf
from ..models.overhead import Overhead
from ..views.items import DrawerItem, HangingItem, ShelfItem, OverheadItem


class MainWindow(QMainWindow):
    """Main application window."""

    project_changed = Signal()

    def __init__(self):
        super().__init__()
        self.project = FileService.create_new_project()
        self.current_file = None
        self.is_modified = False

        self._setup_ui()
        self._setup_menus()
        self._setup_toolbars()
        self._setup_statusbar()
        self._update_title()
        self._connect_signals()

    def _setup_ui(self):
        """Set up the main UI layout."""
        self.setWindowTitle("Wardrobe Planner")
        self.setMinimumSize(1200, 800)

        # Central widget - canvas view
        self.canvas_view = CanvasView()
        self.setCentralWidget(self.canvas_view)

        # Tool palette dock (left side)
        self.tool_dock = QDockWidget("Components", self)
        self.tool_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.tool_palette = ToolPalette()
        self.tool_dock.setWidget(self.tool_palette)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.tool_dock)

        # Property panel dock (right side)
        self.property_dock = QDockWidget("Properties", self)
        self.property_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.property_panel = PropertyPanel()
        self.property_dock.setWidget(self.property_panel)
        self.addDockWidget(Qt.RightDockWidgetArea, self.property_dock)

    def _setup_menus(self):
        """Set up application menus."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")
        file_menu.addAction(self._create_action("&New", "Ctrl+N", self.new_project))
        file_menu.addAction(self._create_action("&Open...", "Ctrl+O", self.open_project))
        file_menu.addAction(self._create_action("&Save", "Ctrl+S", self.save_project))
        file_menu.addAction(self._create_action("Save &As...", "Ctrl+Shift+S", self.save_project_as))
        file_menu.addSeparator()
        file_menu.addAction(self._create_action("&Export to PDF...", "Ctrl+E", self.export_pdf))
        file_menu.addAction(self._create_action("&Print...", "Ctrl+P", self.print_project))
        file_menu.addSeparator()
        file_menu.addAction(self._create_action("E&xit", "Alt+F4", self.close))

        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        edit_menu.addAction(self._create_action("&Undo", "Ctrl+Z", self.undo))
        edit_menu.addAction(self._create_action("&Redo", "Ctrl+Y", self.redo))
        edit_menu.addSeparator()
        edit_menu.addAction(self._create_action("&Delete", "Delete", self.delete_selected))
        edit_menu.addAction(self._create_action("Select &All", "Ctrl+A", self.select_all))

        # View menu
        view_menu = menubar.addMenu("&View")
        view_menu.addAction(self._create_action("Zoom &In", "Ctrl++", self.zoom_in))
        view_menu.addAction(self._create_action("Zoom &Out", "Ctrl+-", self.zoom_out))
        view_menu.addAction(self._create_action("&Fit to Window", "Ctrl+0", self.fit_to_window))
        # Help menu
        help_menu = menubar.addMenu("&Help")
        help_menu.addAction(self._create_action("&About", "", self.show_about))

    def _setup_toolbars(self):
        """Set up toolbars."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        toolbar.addAction(self._create_action("New", "", self.new_project))
        toolbar.addAction(self._create_action("Open", "", self.open_project))
        toolbar.addAction(self._create_action("Save", "", self.save_project))
        toolbar.addSeparator()
        toolbar.addAction(self._create_action("Undo", "", self.undo))
        toolbar.addAction(self._create_action("Redo", "", self.redo))
        toolbar.addSeparator()
        toolbar.addAction(self._create_action("Zoom In", "", self.zoom_in))
        toolbar.addAction(self._create_action("Zoom Out", "", self.zoom_out))
        toolbar.addAction(self._create_action("Fit", "", self.fit_to_window))

    def _setup_statusbar(self):
        """Set up status bar."""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Ready")

    def _connect_signals(self):
        """Connect signals between components."""
        self.tool_palette.component_selected.connect(self._on_component_selected)
        self.property_panel.property_changed.connect(self._on_property_changed)
        self.property_panel.delete_requested.connect(self.delete_selected)
        self.canvas_view.canvas_scene.selectionChanged.connect(self._on_selection_changed)
        self.canvas_view.component_dropped.connect(self._on_component_dropped)

    def _create_action(self, text, shortcut, slot, checkable=False):
        """Helper to create menu/toolbar actions."""
        action = QAction(text, self)
        if shortcut:
            action.setShortcut(QKeySequence(shortcut))
        action.triggered.connect(slot)
        action.setCheckable(checkable)
        return action

    def _update_title(self):
        """Update window title based on current file."""
        title = "Wardrobe Planner"
        if self.current_file:
            title = f"{self.current_file.name} - {title}"
        else:
            title = f"Untitled - {title}"
        if self.is_modified:
            title = f"*{title}"
        self.setWindowTitle(title)

    def _mark_modified(self):
        """Mark project as modified."""
        self.is_modified = True
        self._update_title()

    def _confirm_discard(self) -> bool:
        """Ask user to confirm discarding unsaved changes."""
        if not self.is_modified:
            return True

        reply = QMessageBox.question(
            self, "Unsaved Changes",
            "You have unsaved changes. Do you want to discard them?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        return reply == QMessageBox.Yes

    def _create_component_and_item(self, component_type: ComponentType):
        """Create a component model and its corresponding graphics item."""
        if component_type == ComponentType.DRAWER_UNIT:
            component = DrawerUnit.create(name="New Drawers", width=600, height=800, depth=500)
            item = DrawerItem(component)
        elif component_type == ComponentType.HANGING_SPACE:
            component = HangingSpace.create(name="Hanging Space", width=800, height=1800, depth=580)
            item = HangingItem(component)
        elif component_type == ComponentType.SHELF:
            component = Shelf.create(name="Shelf", width=800, height=18, depth=500)
            item = ShelfItem(component)
        elif component_type == ComponentType.OVERHEAD:
            component = Overhead.create(name="Overhead", width=800, height=400, depth=580)
            item = OverheadItem(component)
        else:
            return None, None
        return component, item

    def _add_component_at(self, component_type: ComponentType, x: float, y: float):
        """Create and place a component at the given position."""
        component, item = self._create_component_and_item(component_type)
        if component is None:
            self.statusbar.showMessage(f"Component type {component_type} not yet implemented")
            return

        component.position.x = x
        component.position.y = y
        item.setPos(x, y)

        scene = self.canvas_view.canvas_scene
        scene.addItem(item)
        self.project.add_component(component)

        self._mark_modified()
        self.statusbar.showMessage(f"Added {component.name}")

    def _on_component_selected(self, component_type: ComponentType):
        """Handle component selection from palette (click) - add to canvas center."""
        # Place at the center of the currently visible area
        viewport_center = self.canvas_view.viewport().rect().center()
        scene_center = self.canvas_view.mapToScene(viewport_center)
        self._add_component_at(component_type, scene_center.x(), scene_center.y())

    def _on_component_dropped(self, component_type: ComponentType, x: float, y: float):
        """Handle component dropped onto canvas from palette."""
        self._add_component_at(component_type, x, y)

    def _on_property_changed(self):
        """Handle property changes from panel."""
        # Sync visual items with model
        for item in self.canvas_view.canvas_scene.items():
            if hasattr(item, 'sync_from_model'):
                item.sync_from_model()
        self._mark_modified()

    def _on_selection_changed(self):
        """Handle selection changes in canvas."""
        selected = self.canvas_view.canvas_scene.selectedItems()
        if selected and hasattr(selected[0], 'component'):
            self.property_panel.set_component(selected[0].component)
        else:
            self.property_panel.set_component(None)

    # File operations
    def new_project(self):
        if not self._confirm_discard():
            return
        self.project = FileService.create_new_project()
        self.current_file = None
        self.is_modified = False
        self._update_title()
        self.project_changed.emit()
        self.statusbar.showMessage("New project created")

    def open_project(self):
        if not self._confirm_discard():
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Project", "",
            FileService.get_file_filter()
        )
        if file_path:
            from pathlib import Path
            project, message = FileService.load_project(Path(file_path))
            if project:
                self.project = project
                self.current_file = Path(file_path)
                self.is_modified = False
                self._update_title()
                self.project_changed.emit()
            self.statusbar.showMessage(message)

    def save_project(self):
        if self.current_file:
            success, message = FileService.save_project(self.project, self.current_file)
            if success:
                self.is_modified = False
                self._update_title()
            self.statusbar.showMessage(message)
        else:
            self.save_project_as()

    def save_project_as(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Project", "",
            FileService.get_file_filter()
        )
        if file_path:
            from pathlib import Path
            self.current_file = Path(file_path)
            success, message = FileService.save_project(self.project, self.current_file)
            if success:
                self.is_modified = False
                self._update_title()
            self.statusbar.showMessage(message)

    def export_pdf(self):
        """Export plan to PDF."""
        from PySide6.QtWidgets import QFileDialog
        from ..services.export_service import ExportService

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export to PDF", "",
            "PDF Files (*.pdf);;All Files (*)"
        )
        if file_path:
            from pathlib import Path
            scene = self.canvas_view.canvas_scene
            success, message = ExportService.export_to_pdf(
                scene, Path(file_path),
                title=self.project.metadata.project_name,
                frame_width=scene.frame_width,
                frame_height=scene.frame_height
            )
            self.statusbar.showMessage(message)

    def print_project(self):
        """Print the plan."""
        from ..services.print_service import PrintService

        scene = self.canvas_view.canvas_scene
        if PrintService.print_with_preview(
            scene, self,
            frame_width=scene.frame_width,
            frame_height=scene.frame_height
        ):
            self.statusbar.showMessage("Print job sent")
        else:
            self.statusbar.showMessage("Print cancelled")

    def undo(self):
        self.statusbar.showMessage("Undo - Not yet implemented")

    def redo(self):
        self.statusbar.showMessage("Redo - Not yet implemented")

    def delete_selected(self):
        selected = self.canvas_view.canvas_scene.selectedItems()
        for item in selected:
            if hasattr(item, 'component'):
                self.project.remove_component(item.component.id)
            self.canvas_view.canvas_scene.removeItem(item)
        self.property_panel.clear()
        self._mark_modified()
        self.statusbar.showMessage(f"Deleted {len(selected)} item(s)")

    def select_all(self):
        self.statusbar.showMessage("Select All - Not yet implemented")

    def zoom_in(self):
        self.canvas_view.zoom_in()

    def zoom_out(self):
        self.canvas_view.zoom_out()

    def fit_to_window(self):
        self.canvas_view.fit_to_frame()

    def show_about(self):
        QMessageBox.about(self, "About Wardrobe Planner",
            "Wardrobe Planner v1.0\n\n"
            "A simple tool for designing wardrobe layouts.\n\n"
            "Created for Jammo's Wardrobes"
        )

    def closeEvent(self, event):
        if self._confirm_discard():
            event.accept()
        else:
            event.ignore()
