from dataclasses import dataclass
from typing import Any, Dict, Optional
from uuid import uuid4

from .component import Component, Dimensions, Position
from .enums import ComponentType


@dataclass
class Overhead(Component):
    """An overhead storage component with doors."""
    door_type: str = "hinged"  # "hinged", "lift_up", "sliding"
    door_count: int = 2
    has_shelf: bool = True

    @classmethod
    def create(
        cls,
        name: str,
        width: float = 800,
        height: float = 400,
        depth: float = 580,
        x: float = 0,
        y: float = 0,
        door_type: str = "hinged",
        door_count: int = 2,
        has_shelf: bool = True,
        id: Optional[str] = None,
        color: Optional[str] = None,
        label: Optional[str] = None,
        notes: Optional[str] = None,
        locked: bool = False,
    ) -> "Overhead":
        """Factory method to create an Overhead instance."""
        return cls(
            id=id or str(uuid4()),
            component_type=ComponentType.OVERHEAD,
            name=name,
            dimensions=Dimensions(width, height, depth),
            position=Position(x, y),
            color=color,
            label=label,
            notes=notes,
            locked=locked,
            door_type=door_type,
            door_count=door_count,
            has_shelf=has_shelf,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert overhead to dictionary for JSON serialization."""
        data = super().to_dict()
        data.update({
            "door_type": self.door_type,
            "door_count": self.door_count,
            "has_shelf": self.has_shelf,
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Overhead":
        """Create Overhead instance from dictionary."""
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
            door_type=data.get("door_type", "hinged"),
            door_count=data.get("door_count", 2),
            has_shelf=data.get("has_shelf", True),
        )
