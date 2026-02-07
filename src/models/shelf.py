from dataclasses import dataclass
from typing import Any, Dict, Optional
from uuid import uuid4

from .component import Component, Dimensions, Position
from .enums import ComponentType


@dataclass
class Shelf(Component):
    """A shelf component for storage."""
    adjustable: bool = True
    shelf_thickness: float = 18.0  # Thickness in mm
    load_capacity: float = 30.0  # Load capacity in kg

    @classmethod
    def create(
        cls,
        name: str,
        width: float = 800.0,
        height: float = 18.0,
        depth: float = 500.0,
        x: float = 0.0,
        y: float = 0.0,
        adjustable: bool = True,
        shelf_thickness: float = 18.0,
        load_capacity: float = 30.0,
        id: Optional[str] = None,
        color: Optional[str] = None,
        label: Optional[str] = None,
        notes: Optional[str] = None,
        locked: bool = False,
    ) -> "Shelf":
        """Factory method to create a Shelf instance."""
        return cls(
            id=id or str(uuid4()),
            component_type=ComponentType.SHELF,
            name=name,
            dimensions=Dimensions(width, height, depth),
            position=Position(x, y),
            color=color,
            label=label,
            notes=notes,
            locked=locked,
            adjustable=adjustable,
            shelf_thickness=shelf_thickness,
            load_capacity=load_capacity,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert shelf to dictionary for JSON serialization."""
        data = super().to_dict()
        data.update({
            "adjustable": self.adjustable,
            "shelf_thickness": self.shelf_thickness,
            "load_capacity": self.load_capacity,
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Shelf":
        """Create Shelf instance from dictionary."""
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
            adjustable=data.get("adjustable", True),
            shelf_thickness=data.get("shelf_thickness", 18.0),
            load_capacity=data.get("load_capacity", 30.0),
        )
