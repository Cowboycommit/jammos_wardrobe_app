"""Component library with pre-built wardrobe component templates."""
from dataclasses import dataclass
from typing import Dict, List, Any

from ..models.enums import ComponentType
from ..models.component import Dimensions
from ..models.drawer import DrawerUnit
from ..models.hanging import HangingSpace
from ..models.shelf import Shelf
from ..models.overhead import Overhead


@dataclass
class ComponentTemplate:
    """A reusable template for creating components."""
    name: str
    description: str
    component_type: ComponentType
    width: float
    height: float
    depth: float
    properties: Dict[str, Any]

    def create_component(self):
        """Create a new component instance from this template."""
        if self.component_type == ComponentType.DRAWER_UNIT:
            return DrawerUnit.create(
                name=self.name,
                width=self.width,
                height=self.height,
                depth=self.depth,
                **self.properties
            )
        elif self.component_type == ComponentType.HANGING_SPACE:
            return HangingSpace.create(
                name=self.name,
                width=self.width,
                height=self.height,
                depth=self.depth,
                **self.properties
            )
        elif self.component_type == ComponentType.SHELF:
            return Shelf.create(
                name=self.name,
                width=self.width,
                height=self.height,
                depth=self.depth,
                **self.properties
            )
        elif self.component_type == ComponentType.OVERHEAD:
            return Overhead.create(
                name=self.name,
                width=self.width,
                height=self.height,
                depth=self.depth,
                **self.properties
            )
        else:
            raise ValueError(f"Unknown component type: {self.component_type}")


class ComponentLibrary:
    """Manages the library of component templates."""

    def __init__(self):
        self._templates: Dict[str, ComponentTemplate] = {}
        self._load_builtin_templates()

    def _load_builtin_templates(self):
        """Load built-in component templates."""

        # === DRAWER UNITS ===
        self.add_template(ComponentTemplate(
            name="4-Drawer Unit",
            description="Standard 4-drawer unit with bar handles",
            component_type=ComponentType.DRAWER_UNIT,
            width=600, height=800, depth=500,
            properties={"drawer_count": 4, "handle_style": "bar"}
        ))

        self.add_template(ComponentTemplate(
            name="3-Drawer Unit (Deep)",
            description="3-drawer unit with deeper drawers",
            component_type=ComponentType.DRAWER_UNIT,
            width=600, height=750, depth=500,
            properties={"drawer_count": 3, "handle_style": "bar"}
        ))

        self.add_template(ComponentTemplate(
            name="5-Drawer Unit (Narrow)",
            description="Narrow 5-drawer unit for accessories",
            component_type=ComponentType.DRAWER_UNIT,
            width=450, height=750, depth=500,
            properties={"drawer_count": 5, "handle_style": "knob"}
        ))

        # === HANGING SPACES ===
        self.add_template(ComponentTemplate(
            name="Full-Length Hanging",
            description="Full-length hanging for coats and dresses",
            component_type=ComponentType.HANGING_SPACE,
            width=800, height=1800, depth=580,
            properties={"rail_type": "single", "clothing_type": "full_length"}
        ))

        self.add_template(ComponentTemplate(
            name="Double Hanging",
            description="Two rails for shirts and pants",
            component_type=ComponentType.HANGING_SPACE,
            width=800, height=1800, depth=580,
            properties={"rail_type": "double", "clothing_type": "half_length"}
        ))

        self.add_template(ComponentTemplate(
            name="Shirt Hanging",
            description="Single rail for shirts",
            component_type=ComponentType.HANGING_SPACE,
            width=600, height=1000, depth=580,
            properties={"rail_type": "single", "clothing_type": "shirts"}
        ))

        # === SHELVES ===
        self.add_template(ComponentTemplate(
            name="Standard Shelf",
            description="Standard adjustable shelf",
            component_type=ComponentType.SHELF,
            width=800, height=18, depth=500,
            properties={"adjustable": True, "shelf_thickness": 18.0}
        ))

        self.add_template(ComponentTemplate(
            name="Wide Shelf",
            description="Wide shelf for folded items",
            component_type=ComponentType.SHELF,
            width=1200, height=18, depth=500,
            properties={"adjustable": True, "shelf_thickness": 18.0}
        ))

        # === OVERHEADS ===
        self.add_template(ComponentTemplate(
            name="Overhead Cabinet (2 Door)",
            description="Two-door overhead storage cabinet",
            component_type=ComponentType.OVERHEAD,
            width=800, height=400, depth=580,
            properties={"door_type": "hinged", "door_count": 2, "has_shelf": True}
        ))

        self.add_template(ComponentTemplate(
            name="Lift-Up Overhead",
            description="Overhead with lift-up door",
            component_type=ComponentType.OVERHEAD,
            width=600, height=350, depth=580,
            properties={"door_type": "lift_up", "door_count": 1, "has_shelf": False}
        ))

        self.add_template(ComponentTemplate(
            name="Wide Overhead (3 Door)",
            description="Three-door overhead cabinet",
            component_type=ComponentType.OVERHEAD,
            width=1200, height=400, depth=580,
            properties={"door_type": "hinged", "door_count": 3, "has_shelf": True}
        ))

    def add_template(self, template: ComponentTemplate):
        """Add a template to the library."""
        self._templates[template.name] = template

    def get_template(self, name: str) -> ComponentTemplate:
        """Get a template by name."""
        return self._templates.get(name)

    def get_templates_by_type(self, component_type: ComponentType) -> List[ComponentTemplate]:
        """Get all templates of a specific type."""
        return [t for t in self._templates.values() if t.component_type == component_type]

    def get_all_templates(self) -> List[ComponentTemplate]:
        """Get all templates."""
        return list(self._templates.values())

    def get_template_names(self) -> List[str]:
        """Get all template names."""
        return list(self._templates.keys())


# Global instance
_library = None

def get_library() -> ComponentLibrary:
    """Get the global component library instance."""
    global _library
    if _library is None:
        _library = ComponentLibrary()
    return _library
