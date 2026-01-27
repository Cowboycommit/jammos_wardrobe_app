"""Project model for wardrobe planning application."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid

from .enums import ComponentType, UnitSystem
from .component import Component, Dimensions, Position


@dataclass
class WardrobeFrame:
    """The outer frame/carcass of the wardrobe."""
    width: float = 2400.0       # Total width in mm
    height: float = 2400.0      # Total height in mm
    depth: float = 600.0        # Total depth in mm
    panel_thickness: float = 18.0
    top_clearance: float = 50.0
    base_height: float = 100.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "width": self.width,
            "height": self.height,
            "depth": self.depth,
            "panel_thickness": self.panel_thickness,
            "top_clearance": self.top_clearance,
            "base_height": self.base_height,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WardrobeFrame":
        return cls(**data)

    @property
    def internal_width(self) -> float:
        """Internal width after accounting for side panels."""
        return self.width - 2 * self.panel_thickness

    @property
    def internal_height(self) -> float:
        """Internal height after accounting for top/bottom."""
        return self.height - self.top_clearance - self.base_height


@dataclass
class ProjectMetadata:
    """Project metadata and client information."""
    project_name: str = "Untitled Wardrobe"
    client_name: str = ""
    client_address: str = ""
    client_phone: str = ""
    notes: str = ""
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())
    modified_date: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_name": self.project_name,
            "client_name": self.client_name,
            "client_address": self.client_address,
            "client_phone": self.client_phone,
            "notes": self.notes,
            "created_date": self.created_date,
            "modified_date": self.modified_date,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProjectMetadata":
        return cls(**data)


@dataclass
class WardrobeProject:
    """Complete wardrobe project containing frame and all components."""
    version: str = "1.0"
    metadata: ProjectMetadata = field(default_factory=ProjectMetadata)
    unit_system: UnitSystem = UnitSystem.METRIC
    frame: WardrobeFrame = field(default_factory=WardrobeFrame)
    components: List[Component] = field(default_factory=list)
    zoom_level: float = 1.0
    scroll_position: tuple = (0, 0)

    def add_component(self, component: Component) -> None:
        self.components.append(component)
        self.metadata.modified_date = datetime.now().isoformat()

    def remove_component(self, component_id: str) -> Optional[Component]:
        for i, comp in enumerate(self.components):
            if comp.id == component_id:
                removed = self.components.pop(i)
                self.metadata.modified_date = datetime.now().isoformat()
                return removed
        return None

    def get_component(self, component_id: str) -> Optional[Component]:
        for comp in self.components:
            if comp.id == component_id:
                return comp
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "metadata": self.metadata.to_dict(),
            "unit_system": self.unit_system.name,
            "frame": self.frame.to_dict(),
            "components": [c.to_dict() for c in self.components],
            "view_state": {
                "zoom_level": self.zoom_level,
                "scroll_position": list(self.scroll_position),
            }
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WardrobeProject":
        # Import here to avoid circular imports
        from .drawer import DrawerUnit
        from .hanging import HangingSpace
        from .shelf import Shelf
        from .overhead import Overhead

        type_map = {
            "DRAWER_UNIT": DrawerUnit,
            "HANGING_SPACE": HangingSpace,
            "SHELF": Shelf,
            "OVERHEAD": Overhead,
        }

        components = []
        for comp_data in data.get("components", []):
            comp_type = comp_data.get("component_type", "SHELF")
            comp_class = type_map.get(comp_type, Component)
            components.append(comp_class.from_dict(comp_data))

        view_state = data.get("view_state", {})

        return cls(
            version=data.get("version", "1.0"),
            metadata=ProjectMetadata.from_dict(data.get("metadata", {})),
            unit_system=UnitSystem[data.get("unit_system", "METRIC")],
            frame=WardrobeFrame.from_dict(data.get("frame", {})),
            components=components,
            zoom_level=view_state.get("zoom_level", 1.0),
            scroll_position=tuple(view_state.get("scroll_position", [0, 0])),
        )
