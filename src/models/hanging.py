from dataclasses import dataclass
from typing import Any, Dict, Optional
from uuid import uuid4

from .component import Component, Dimensions, Position
from .enums import ComponentType


@dataclass
class HangingSpace(Component):
    """A hanging space component for clothing storage."""
    rail_height: float = 1700.0  # Height of the rail from the bottom in mm
    rail_type: str = "single"  # "single", "double"
    clothing_type: str = "full_length"  # "full_length", "half_length", "shirts"

    @classmethod
    def create(
        cls,
        name: str,
        width: float = 800.0,
        height: float = 1800.0,
        depth: float = 580.0,
        x: float = 0.0,
        y: float = 0.0,
        rail_height: float = 1700.0,
        rail_type: str = "single",
        clothing_type: str = "full_length",
        id: Optional[str] = None,
        color: Optional[str] = None,
        label: Optional[str] = None,
        notes: Optional[str] = None,
        locked: bool = False,
    ) -> "HangingSpace":
        """Factory method to create a HangingSpace instance."""
        return cls(
            id=id or str(uuid4()),
            component_type=ComponentType.HANGING_SPACE,
            name=name,
            dimensions=Dimensions(width, height, depth),
            position=Position(x, y),
            color=color,
            label=label,
            notes=notes,
            locked=locked,
            rail_height=rail_height,
            rail_type=rail_type,
            clothing_type=clothing_type,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert hanging space to dictionary for JSON serialization."""
        data = super().to_dict()
        data.update({
            "rail_height": self.rail_height,
            "rail_type": self.rail_type,
            "clothing_type": self.clothing_type,
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HangingSpace":
        """Create HangingSpace instance from dictionary."""
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
            rail_height=data.get("rail_height", 1700.0),
            rail_type=data.get("rail_type", "single"),
            clothing_type=data.get("clothing_type", "full_length"),
        )
