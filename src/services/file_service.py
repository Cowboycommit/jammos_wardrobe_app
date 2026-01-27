"""File service for saving and loading wardrobe projects."""
import json
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime

from ..models.project import WardrobeProject


class FileService:
    """Handles saving and loading wardrobe project files."""

    FILE_EXTENSION = ".wdp"
    SUPPORTED_VERSIONS = ["1.0"]

    @staticmethod
    def save_project(project: WardrobeProject, file_path: Path) -> Tuple[bool, str]:
        """
        Save project to file.

        Returns: Tuple of (success: bool, message: str)
        """
        try:
            # Ensure correct extension
            if file_path.suffix.lower() != FileService.FILE_EXTENSION:
                file_path = file_path.with_suffix(FileService.FILE_EXTENSION)

            # Update modified date
            project.metadata.modified_date = datetime.now().isoformat()

            # Create backup if file exists
            if file_path.exists():
                backup_path = file_path.with_suffix(f"{FileService.FILE_EXTENSION}.bak")
                backup_path.write_bytes(file_path.read_bytes())

            # Serialize and write
            data = project.to_dict()
            json_str = json.dumps(data, indent=2, ensure_ascii=False)

            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(json_str, encoding="utf-8")

            return True, f"Project saved to {file_path}"

        except PermissionError:
            return False, f"Permission denied: Cannot write to {file_path}"
        except Exception as e:
            return False, f"Failed to save project: {str(e)}"

    @staticmethod
    def load_project(file_path: Path) -> Tuple[Optional[WardrobeProject], str]:
        """
        Load project from file.

        Returns: Tuple of (project or None, message: str)
        """
        try:
            if not file_path.exists():
                return None, f"File not found: {file_path}"

            json_str = file_path.read_text(encoding="utf-8")
            data = json.loads(json_str)

            # Version check
            version = data.get("version", "unknown")
            if version not in FileService.SUPPORTED_VERSIONS:
                return None, f"Unsupported file version: {version}"

            project = WardrobeProject.from_dict(data)

            return project, f"Project loaded from {file_path}"

        except json.JSONDecodeError as e:
            return None, f"Invalid file format: {str(e)}"
        except KeyError as e:
            return None, f"Missing required field: {str(e)}"
        except Exception as e:
            return None, f"Failed to load project: {str(e)}"

    @staticmethod
    def create_new_project() -> WardrobeProject:
        """Create a new empty project with defaults."""
        return WardrobeProject()

    @staticmethod
    def get_file_filter() -> str:
        """Get file dialog filter string."""
        return f"Wardrobe Design Files (*{FileService.FILE_EXTENSION});;All Files (*)"
