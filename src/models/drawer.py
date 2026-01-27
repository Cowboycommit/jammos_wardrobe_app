from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from uuid import uuid4

from .component import Component, Dimensions, Position
from .enums import ComponentType


@dataclass
class DrawerUnit(Component):
    """A drawer unit component containing multiple drawers."""
    drawer_count: int = 3
    drawer_heights: List[float] = field(default_factory=list)
    handle_style: str = "bar"  # "bar", "knob", "recessed", "none"

    def __post_init__(self):
        """Initialize drawer heights if not provided."""
        if not self.drawer_heights and self.drawer_count > 0:
            # Calculate equal heights for each drawer based on unit height
            drawer_height = self.dimensions.height / self.drawer_count
            self.drawer_heights = [drawer_height] * self.drawer_count

    @classmethod
    def create(
        cls,
        name: str,
        width: float = 600,
        height: float = 800,
        depth: float = 500,
        x: float = 0,
        y: float = 0,
        drawer_count: int = 3,
        drawer_heights: Optional[List[float]] = None,
        handle_style: str = "bar",
        id: Optional[str] = None,
        color: Optional[str] = None,
        label: Optional[str] = None,
        notes: Optional[str] = None,
        locked: bool = False,
    ) -> "DrawerUnit":
        """Factory method to create a DrawerUnit instance."""
        return cls(
            id=id or str(uuid4()),
            component_type=ComponentType.DRAWER_UNIT,
            name=name,
            dimensions=Dimensions(width, height, depth),
            position=Position(x, y),
            color=color,
            label=label,
            notes=notes,
            locked=locked,
            drawer_count=drawer_count,
            drawer_heights=drawer_heights or [],
            handle_style=handle_style,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert drawer unit to dictionary for JSON serialization."""
        data = super().to_dict()
        data.update({
            "drawer_count": self.drawer_count,
            "drawer_heights": self.drawer_heights,
            "handle_style": self.handle_style,
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DrawerUnit":
        """Create DrawerUnit instance from dictionary."""
        return cls(
            id=data["id"],
            component_type=ComponentType[data["component_type"]],
            name=data["name"],
            dimensions=Dimensions.from_dict(data["dimensions"]),
            position=Position.from_dict(data["position"]),
            color=data.get("color"),
            label=data.get("label"),
            notes=data.get("notes"),
            locked=data.get("locked", False),
            drawer_count=data.get("drawer_count", 3),
            drawer_heights=data.get("drawer_heights", []),
            handle_style=data.get("handle_style", "bar"),
        )
