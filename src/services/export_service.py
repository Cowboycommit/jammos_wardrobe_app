"""Export service for wardrobe plans to PDF and PNG."""
from pathlib import Path
from typing import Tuple

from PySide6.QtCore import QRectF, QMarginsF, Qt
from PySide6.QtGui import QPainter, QPageLayout, QPageSize, QImage, QColor
from PySide6.QtPrintSupport import QPrinter
from PySide6.QtWidgets import QGraphicsScene


class ExportService:
    """Handles exporting wardrobe plans to various formats."""

    @staticmethod
    def export_to_pdf(
        scene: QGraphicsScene,
        file_path: Path,
        title: str = "",
        frame_width: float = 4800,
        frame_height: float = 2400
    ) -> Tuple[bool, str]:
        """
        Export the scene to a PDF file.

        Args:
            scene: The graphics scene to export
            file_path: Destination PDF path
            title: Optional title to add to the page
            frame_width: Wardrobe frame width in mm
            frame_height: Wardrobe frame height in mm

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            if file_path.suffix.lower() != ".pdf":
                file_path = file_path.with_suffix(".pdf")

            # Configure printer for PDF output
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(str(file_path))

            # Determine orientation based on aspect ratio
            if frame_width > frame_height:
                orientation = QPageLayout.Landscape
            else:
                orientation = QPageLayout.Portrait

            # Set page layout
            layout = QPageLayout(
                QPageSize(QPageSize.A4),
                orientation,
                QMarginsF(15, 20, 15, 15),
                QPageLayout.Millimeter
            )
            printer.setPageLayout(layout)

            # Create painter and render
            painter = QPainter()
            if not painter.begin(printer):
                return False, "Failed to initialize PDF writer"

            try:
                # Get page dimensions
                page_rect = printer.pageRect(QPrinter.DevicePixel)

                # Reserve space for title if provided
                content_rect = page_rect
                if title:
                    title_height = 60
                    painter.setFont(painter.font())
                    painter.drawText(
                        int(page_rect.x()), int(page_rect.y()),
                        int(page_rect.width()), title_height,
                        Qt.AlignCenter, title
                    )
                    content_rect.setTop(page_rect.top() + title_height)

                # Source rect (wardrobe frame with small margin)
                margin = 50
                source_rect = QRectF(
                    -margin, -margin,
                    frame_width + 2 * margin,
                    frame_height + 2 * margin
                )

                # Render scene to PDF
                scene.render(painter, content_rect, source_rect, Qt.KeepAspectRatio)

            finally:
                painter.end()

            return True, f"PDF exported to {file_path}"

        except Exception as e:
            return False, f"Failed to export PDF: {str(e)}"

    @staticmethod
    def export_to_png(
        scene: QGraphicsScene,
        file_path: Path,
        width: int = 2000,
        frame_width: float = 4800,
        frame_height: float = 2400
    ) -> Tuple[bool, str]:
        """
        Export the scene to a PNG image.

        Args:
            scene: The graphics scene to export
            file_path: Destination PNG path
            width: Image width in pixels
            frame_width: Wardrobe frame width in mm
            frame_height: Wardrobe frame height in mm

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            if file_path.suffix.lower() != ".png":
                file_path = file_path.with_suffix(".png")

            # Calculate dimensions maintaining aspect ratio
            aspect_ratio = frame_height / frame_width
            height = int(width * aspect_ratio)

            # Create image
            image = QImage(width, height, QImage.Format_ARGB32)
            image.fill(QColor("#FFFFFF"))

            # Source rect
            margin = 50
            source_rect = QRectF(
                -margin, -margin,
                frame_width + 2 * margin,
                frame_height + 2 * margin
            )

            # Render scene to image
            painter = QPainter(image)
            painter.setRenderHint(QPainter.Antialiasing)
            scene.render(painter, QRectF(0, 0, width, height), source_rect)
            painter.end()

            # Save image
            if not image.save(str(file_path)):
                return False, f"Failed to save image to {file_path}"

            return True, f"PNG exported to {file_path}"

        except Exception as e:
            return False, f"Failed to export PNG: {str(e)}"
