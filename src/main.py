"""Main entry point for the wardrobe planner application."""
import sys
from PySide6.QtWidgets import QApplication
from src.views.main_window import MainWindow


def main():
    """Main entry point for the wardrobe planner application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Wardrobe Planner")
    app.setOrganizationName("Jammos Wardrobes")

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
