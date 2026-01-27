from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from uuid import uuid4

from .enums import ComponentType


@dataclass
class Dimensions:
    """Dimensions of a component in millimeters."""
    width: float
    height: float
    depth: float

    def to_dict(self) -> Dict[str, float]:
        """Convert dimensions to dictionary for JSON serialization."""
        return {
            "width": self.width,
            "height": self.height,
            "depth": self.depth,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "Dimensions":
        """Create Dimensions instance from dictionary."""
        return cls(
            width=data["width"],
            height=data["height"],
            depth=data["depth"],
        )


@dataclass
class Position:
    """Position of a component within the wardrobe (in millimeters)."""
    x: float
    y: float

    def to_dict(self) -> Dict[str, float]:
        """Convert position to dictionary for JSON serialization."""
        return {
            "x": self.x,
            "y": self.y,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "Position":
        """Create Position instance from dictionary."""
        return cls(
            x=data["x"],
            y=data["y"],
        )


@dataclass
class Component:
    """Base class for all wardrobe components."""
    component_type: ComponentType
    name: str
    dimensions: Dimensions
    position: Position
    id: str = field(default_factory=lambda: str(uuid4()))
    color: Optional[str] = None
    label: Optional[str] = None
    notes: Optional[str] = None
    locked: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert component to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "component_type": self.component_type.name,
            "name": self.name,
            "dimensions": self.dimensions.to_dict(),
            "position": self.position.to_dict(),
            "color": self.color,
            "label": self.label,
            "notes": self.notes,
            "locked": self.locked,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Component":
        """Create Component instance from dictionary."""
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
        )
