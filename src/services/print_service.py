"""Print service for wardrobe plans."""
from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPainter
from PySide6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PySide6.QtWidgets import QGraphicsScene, QWidget


class PrintService:
    """Handles printing wardrobe plans."""

    @staticmethod
    def print_with_preview(
        scene: QGraphicsScene,
        parent: QWidget = None,
        frame_width: float = 4800,
        frame_height: float = 2400
    ) -> bool:
        """
        Show print preview dialog and print if confirmed.

        Args:
            scene: The graphics scene to print
            parent: Parent widget for dialog
            frame_width: Wardrobe frame width in mm
            frame_height: Wardrobe frame height in mm

        Returns:
            True if printed, False if cancelled
        """
        printer = QPrinter(QPrinter.HighResolution)

        preview_dialog = QPrintPreviewDialog(printer, parent)
        preview_dialog.setWindowTitle("Print Preview - Wardrobe Plan")

        def render_preview(p):
            PrintService._render_to_printer(scene, p, frame_width, frame_height)

        preview_dialog.paintRequested.connect(render_preview)

        result = preview_dialog.exec()
        return result == QPrintPreviewDialog.Accepted

    @staticmethod
    def print_direct(
        scene: QGraphicsScene,
        parent: QWidget = None,
        frame_width: float = 4800,
        frame_height: float = 2400
    ) -> bool:
        """
        Show print dialog and print if confirmed.

        Args:
            scene: The graphics scene to print
            parent: Parent widget for dialog
            frame_width: Wardrobe frame width in mm
            frame_height: Wardrobe frame height in mm

        Returns:
            True if printed, False if cancelled
        """
        printer = QPrinter(QPrinter.HighResolution)

        print_dialog = QPrintDialog(printer, parent)
        print_dialog.setWindowTitle("Print Wardrobe Plan")

        if print_dialog.exec() == QPrintDialog.Accepted:
            PrintService._render_to_printer(scene, printer, frame_width, frame_height)
            return True

        return False

    @staticmethod
    def _render_to_printer(
        scene: QGraphicsScene,
        printer: QPrinter,
        frame_width: float,
        frame_height: float
    ):
        """Render scene to the given printer."""
        painter = QPainter()
        painter.begin(printer)

        # Source rect (wardrobe frame with margin)
        margin = 50
        source_rect = QRectF(
            -margin, -margin,
            frame_width + 2 * margin,
            frame_height + 2 * margin
        )

        # Target rect (printer page)
        page_rect = printer.pageRect(QPrinter.DevicePixel)

        # Render maintaining aspect ratio
        scene.render(painter, page_rect, source_rect, Qt.KeepAspectRatio)

        painter.end()
