"""Streamlit UI for Jammo's Wardrobe Planner."""
import io
import json
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st

from src.models.enums import ComponentType, UnitSystem
from src.models.component import Component, Dimensions, Position
from src.models.drawer import DrawerUnit
from src.models.hanging import HangingSpace
from src.models.shelf import Shelf
from src.models.overhead import Overhead
from src.models.project import WardrobeProject, WardrobeFrame, ProjectMetadata
from src.services.file_service import FileService
from src.services.component_library import get_library
from src.utils.config import (
    APP_NAME,
    VERSION,
    DEFAULT_COLORS,
    MIN_FRAME_WIDTH,
    MAX_FRAME_WIDTH,
    MIN_FRAME_HEIGHT,
    MAX_FRAME_HEIGHT,
    MIN_FRAME_DEPTH,
    MAX_FRAME_DEPTH,
)
from src.utils.units import format_dimension, mm_to_inches, mm_to_cm


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

COMPONENT_COLORS = {
    ComponentType.DRAWER_UNIT: "#E8D5B7",
    ComponentType.HANGING_SPACE: "#F5F0E6",
    ComponentType.SHELF: "#D4A574",
    ComponentType.OVERHEAD: "#D4C4B0",
    ComponentType.DIVIDER: "#BC8F8F",
}


def _get_project() -> WardrobeProject:
    """Return the current project from session state, creating one if needed."""
    if "project" not in st.session_state:
        st.session_state["project"] = FileService.create_new_project()
    return st.session_state["project"]


def _set_project(project: WardrobeProject) -> None:
    st.session_state["project"] = project
    # Clear selection when project changes
    st.session_state.pop("selected_id", None)


def _use_metric() -> bool:
    return _get_project().unit_system == UnitSystem.METRIC


def _fmt(mm: float) -> str:
    return format_dimension(mm, _use_metric())


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def _draw_component_details(ax, comp, scale, origin_y):
    """Draw type-specific interior details for a component."""
    x = comp.position.x * scale
    w = comp.dimensions.width * scale
    h = comp.dimensions.height * scale
    # Y is from bottom of frame
    y = (origin_y + comp.position.y) * scale

    if isinstance(comp, DrawerUnit):
        # Draw individual drawer divisions
        if comp.drawer_count > 1:
            drawer_h = h / comp.drawer_count
            for i in range(1, comp.drawer_count):
                dy = y + i * drawer_h
                ax.plot([x, x + w], [dy, dy], color="#8B7355", linewidth=0.8)
            # Draw small handle marks on each drawer
            for i in range(comp.drawer_count):
                cy = y + i * drawer_h + drawer_h / 2
                if comp.handle_style == "bar":
                    bar_w = w * 0.3
                    bx = x + (w - bar_w) / 2
                    ax.plot([bx, bx + bar_w], [cy, cy], color="#666", linewidth=1.5)
                elif comp.handle_style == "knob":
                    ax.plot(x + w / 2, cy, "o", color="#666", markersize=3)

    elif isinstance(comp, HangingSpace):
        # Draw rail(s)
        rail_y = y + comp.rail_height * scale
        if rail_y > y + h:
            rail_y = y + h * 0.9
        ax.plot([x + w * 0.05, x + w * 0.95], [rail_y, rail_y],
                color="#A0A0A0", linewidth=2.5, solid_capstyle="round")
        # Rail supports
        ax.plot([x + w * 0.05, x + w * 0.05], [rail_y, rail_y + h * 0.03],
                color="#A0A0A0", linewidth=1.5)
        ax.plot([x + w * 0.95, x + w * 0.95], [rail_y, rail_y + h * 0.03],
                color="#A0A0A0", linewidth=1.5)
        if comp.rail_type == "double":
            rail2_y = y + h * 0.45
            ax.plot([x + w * 0.05, x + w * 0.95], [rail2_y, rail2_y],
                    color="#A0A0A0", linewidth=2.5, solid_capstyle="round")

    elif isinstance(comp, Shelf):
        # Draw edge banding line along bottom
        ax.plot([x, x + w], [y, y], color="#8B7355", linewidth=1.2)

    elif isinstance(comp, Overhead):
        # Draw door divisions
        if comp.door_count > 1:
            door_w = w / comp.door_count
            for i in range(1, comp.door_count):
                dx = x + i * door_w
                ax.plot([dx, dx], [y, y + h], color="#8B7355", linewidth=0.8)
        # Door handles
        for i in range(comp.door_count):
            door_w = w / comp.door_count
            hx = x + i * door_w + door_w / 2
            hy = y + h / 2
            ax.plot(hx, hy, "o", color="#666", markersize=2.5)
        # Internal shelf (dashed)
        if comp.has_shelf:
            shelf_y = y + h * 0.5
            ax.plot([x + 2, x + w - 2], [shelf_y, shelf_y],
                    color="#999", linewidth=0.7, linestyle="--")


def render_wardrobe(project: WardrobeProject, selected_id: str = None):
    """Render the wardrobe layout as a matplotlib figure."""
    frame = project.frame
    # Scale so the figure is a reasonable pixel size
    fig_w = 8
    scale = fig_w / (frame.width + 200)  # 200mm margin
    fig_h = (frame.height + 200) * scale
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    # Background
    ax.set_facecolor("#F5F5F5")

    # Draw frame outline
    frame_rect = patches.FancyBboxPatch(
        (0, 0),
        frame.width * scale,
        frame.height * scale,
        boxstyle="round,pad=0",
        linewidth=2,
        edgecolor="#333333",
        facecolor="#FFFFFF",
    )
    ax.add_patch(frame_rect)

    # Draw panel thickness indicators
    pt = frame.panel_thickness * scale
    # Left panel
    ax.add_patch(patches.Rectangle((0, 0), pt, frame.height * scale,
                                   facecolor="#DEB887", edgecolor="#8B7355",
                                   linewidth=0.5, alpha=0.5))
    # Right panel
    ax.add_patch(patches.Rectangle(
        ((frame.width - frame.panel_thickness) * scale, 0),
        pt, frame.height * scale,
        facecolor="#DEB887", edgecolor="#8B7355", linewidth=0.5, alpha=0.5))
    # Top
    ax.add_patch(patches.Rectangle(
        (0, (frame.height - frame.top_clearance) * scale),
        frame.width * scale, frame.top_clearance * scale,
        facecolor="#DEB887", edgecolor="#8B7355", linewidth=0.5, alpha=0.3))
    # Base
    ax.add_patch(patches.Rectangle(
        (0, 0), frame.width * scale, frame.base_height * scale,
        facecolor="#DEB887", edgecolor="#8B7355", linewidth=0.5, alpha=0.3))

    # Draw components
    for comp in project.components:
        color = COMPONENT_COLORS.get(comp.component_type, "#CCCCCC")
        edge = "#0078D7" if comp.id == selected_id else "#555555"
        lw = 2.5 if comp.id == selected_id else 1.0

        x = comp.position.x * scale
        y = comp.position.y * scale
        w = comp.dimensions.width * scale
        h = comp.dimensions.height * scale

        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.005",
            linewidth=lw,
            edgecolor=edge,
            facecolor=color,
            alpha=0.85,
        )
        ax.add_patch(rect)

        # Component label
        label = comp.label or comp.name
        fontsize = max(5, min(8, w * 12))
        ax.text(
            x + w / 2,
            y + h / 2,
            label,
            ha="center",
            va="center",
            fontsize=fontsize,
            fontweight="bold" if comp.id == selected_id else "normal",
            color="#333",
            clip_on=True,
        )

        # Draw type-specific details
        _draw_component_details(ax, comp, scale, 0)

    # Dimension annotations
    fw = frame.width * scale
    fh = frame.height * scale
    # Width annotation (top)
    ax.annotate(
        "", xy=(fw, fh + 15 * scale), xytext=(0, fh + 15 * scale),
        arrowprops=dict(arrowstyle="<->", color="#666", lw=1),
    )
    ax.text(fw / 2, fh + 22 * scale, _fmt(frame.width),
            ha="center", va="bottom", fontsize=7, color="#666")
    # Height annotation (right)
    ax.annotate(
        "", xy=(fw + 15 * scale, fh), xytext=(fw + 15 * scale, 0),
        arrowprops=dict(arrowstyle="<->", color="#666", lw=1),
    )
    ax.text(fw + 22 * scale, fh / 2, _fmt(frame.height),
            ha="left", va="center", fontsize=7, color="#666", rotation=90)

    ax.set_xlim(-20 * scale, (frame.width + 100) * scale)
    ax.set_ylim(-20 * scale, (frame.height + 100) * scale)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout()
    return fig


def export_png(project: WardrobeProject, width_px: int = 2000) -> bytes:
    """Render the wardrobe to a PNG byte string."""
    fig = render_wardrobe(project)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight",
                facecolor="#F5F5F5")
    plt.close(fig)
    buf.seek(0)
    return buf.read()


def export_pdf(project: WardrobeProject) -> bytes:
    """Render the wardrobe to a PDF byte string."""
    fig = render_wardrobe(project)
    buf = io.BytesIO()
    fig.savefig(buf, format="pdf", bbox_inches="tight", facecolor="#F5F5F5")
    plt.close(fig)
    buf.seek(0)
    return buf.read()


# ---------------------------------------------------------------------------
# Sidebar sections
# ---------------------------------------------------------------------------

def sidebar_project_management():
    """Project management: new, save (download), load (upload)."""
    st.sidebar.header("Project")
    project = _get_project()

    col1, col2 = st.sidebar.columns(2)
    if col1.button("New Project", use_container_width=True):
        _set_project(FileService.create_new_project())
        st.rerun()

    # Download project (.wdp JSON)
    proj_json = json.dumps(project.to_dict(), indent=2, ensure_ascii=False)
    col2.download_button(
        "Save (.wdp)",
        data=proj_json,
        file_name=f"{project.metadata.project_name}.wdp",
        mime="application/json",
        use_container_width=True,
    )

    # Upload / load
    uploaded = st.sidebar.file_uploader("Load project (.wdp)", type=["wdp", "json"])
    if uploaded is not None:
        try:
            data = json.loads(uploaded.read().decode("utf-8"))
            loaded = WardrobeProject.from_dict(data)
            _set_project(loaded)
            st.sidebar.success("Project loaded!")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Failed to load: {e}")


def sidebar_metadata():
    """Edit project metadata."""
    project = _get_project()
    meta = project.metadata

    with st.sidebar.expander("Project Info", expanded=False):
        new_name = st.text_input("Project Name", value=meta.project_name,
                                 key="meta_name")
        new_client = st.text_input("Client Name", value=meta.client_name,
                                   key="meta_client")
        new_phone = st.text_input("Client Phone", value=meta.client_phone,
                                  key="meta_phone")
        new_notes = st.text_area("Notes", value=meta.notes, key="meta_notes",
                                 height=80)

        if (new_name != meta.project_name or new_client != meta.client_name
                or new_phone != meta.client_phone or new_notes != meta.notes):
            meta.project_name = new_name
            meta.client_name = new_client
            meta.client_phone = new_phone
            meta.notes = new_notes
            meta.modified_date = datetime.now().isoformat()


def sidebar_frame_settings():
    """Frame dimension configuration."""
    project = _get_project()
    frame = project.frame

    with st.sidebar.expander("Frame Settings", expanded=False):
        new_w = st.number_input("Width (mm)", min_value=MIN_FRAME_WIDTH,
                                max_value=MAX_FRAME_WIDTH, value=frame.width,
                                step=50.0, key="frame_w")
        new_h = st.number_input("Height (mm)", min_value=MIN_FRAME_HEIGHT,
                                max_value=MAX_FRAME_HEIGHT, value=frame.height,
                                step=50.0, key="frame_h")
        new_d = st.number_input("Depth (mm)", min_value=MIN_FRAME_DEPTH,
                                max_value=MAX_FRAME_DEPTH, value=frame.depth,
                                step=50.0, key="frame_d")
        new_pt = st.number_input("Panel Thickness (mm)", min_value=10.0,
                                 max_value=50.0, value=frame.panel_thickness,
                                 step=1.0, key="frame_pt")
        new_base = st.number_input("Base Height (mm)", min_value=0.0,
                                   max_value=300.0, value=frame.base_height,
                                   step=10.0, key="frame_base")
        new_tc = st.number_input("Top Clearance (mm)", min_value=0.0,
                                 max_value=200.0, value=frame.top_clearance,
                                 step=10.0, key="frame_tc")

        frame.width = new_w
        frame.height = new_h
        frame.depth = new_d
        frame.panel_thickness = new_pt
        frame.base_height = new_base
        frame.top_clearance = new_tc

        st.caption(
            f"Internal: {_fmt(frame.internal_width)} W x "
            f"{_fmt(frame.internal_height)} H"
        )


def sidebar_unit_system():
    """Toggle between metric and imperial."""
    project = _get_project()
    options = ["Metric (mm)", "Imperial (inches)"]
    current = 0 if project.unit_system == UnitSystem.METRIC else 1
    choice = st.sidebar.radio("Units", options, index=current, key="unit_sys",
                              horizontal=True)
    new_sys = UnitSystem.METRIC if choice == options[0] else UnitSystem.IMPERIAL
    if new_sys != project.unit_system:
        project.unit_system = new_sys


def sidebar_component_library():
    """Add components from the template library."""
    st.sidebar.header("Add Component")
    library = get_library()
    project = _get_project()
    frame = project.frame

    categories = {
        "Drawer Units": ComponentType.DRAWER_UNIT,
        "Hanging Spaces": ComponentType.HANGING_SPACE,
        "Shelves": ComponentType.SHELF,
        "Overheads": ComponentType.OVERHEAD,
    }

    for cat_name, comp_type in categories.items():
        templates = library.get_templates_by_type(comp_type)
        if not templates:
            continue
        with st.sidebar.expander(cat_name, expanded=False):
            for tmpl in templates:
                desc = (f"{tmpl.description}  \n"
                        f"{_fmt(tmpl.width)} x {_fmt(tmpl.height)} x {_fmt(tmpl.depth)}")
                if st.button(tmpl.name, key=f"tmpl_{tmpl.name}",
                             help=desc, use_container_width=True):
                    comp = tmpl.create_component()
                    # Place inside the frame internal area
                    comp.position.x = frame.panel_thickness
                    comp.position.y = frame.base_height
                    project.add_component(comp)
                    st.session_state["selected_id"] = comp.id
                    st.rerun()


def sidebar_export():
    """Export wardrobe design to PNG or PDF."""
    project = _get_project()
    st.sidebar.header("Export")
    col1, col2 = st.sidebar.columns(2)

    png_data = export_png(project)
    col1.download_button(
        "Download PNG",
        data=png_data,
        file_name=f"{project.metadata.project_name}.png",
        mime="image/png",
        use_container_width=True,
    )

    pdf_data = export_pdf(project)
    col2.download_button(
        "Download PDF",
        data=pdf_data,
        file_name=f"{project.metadata.project_name}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )


# ---------------------------------------------------------------------------
# Main area – property editor
# ---------------------------------------------------------------------------

def component_property_editor():
    """Show property editor for the selected component."""
    project = _get_project()
    selected_id = st.session_state.get("selected_id")
    if not selected_id:
        return

    comp = project.get_component(selected_id)
    if comp is None:
        st.session_state.pop("selected_id", None)
        return

    st.subheader(f"Edit: {comp.name}")

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Delete Component", type="primary"):
            project.remove_component(comp.id)
            st.session_state.pop("selected_id", None)
            st.rerun()

    with col1:
        comp.name = st.text_input("Name", value=comp.name, key="prop_name")
        comp.label = st.text_input("Label", value=comp.label or "",
                                   key="prop_label") or None

    # Dimensions
    st.markdown("**Dimensions**")
    dc1, dc2, dc3 = st.columns(3)
    comp.dimensions.width = dc1.number_input(
        "Width (mm)", min_value=50.0, max_value=5000.0,
        value=comp.dimensions.width, step=10.0, key="prop_w")
    comp.dimensions.height = dc2.number_input(
        "Height (mm)", min_value=1.0, max_value=5000.0,
        value=comp.dimensions.height, step=10.0, key="prop_h")
    comp.dimensions.depth = dc3.number_input(
        "Depth (mm)", min_value=50.0, max_value=1000.0,
        value=comp.dimensions.depth, step=10.0, key="prop_d")

    # Position
    st.markdown("**Position**")
    pc1, pc2 = st.columns(2)
    comp.position.x = pc1.number_input(
        "X (mm)", min_value=0.0, max_value=5000.0,
        value=comp.position.x, step=10.0, key="prop_x")
    comp.position.y = pc2.number_input(
        "Y (mm)", min_value=0.0, max_value=5000.0,
        value=comp.position.y, step=10.0, key="prop_y")

    # Type-specific properties
    if isinstance(comp, DrawerUnit):
        st.markdown("**Drawer Options**")
        tc1, tc2 = st.columns(2)
        comp.drawer_count = int(tc1.number_input(
            "Drawer Count", min_value=1, max_value=10,
            value=comp.drawer_count, step=1, key="prop_dc"))
        comp.handle_style = tc2.selectbox(
            "Handle Style",
            options=["bar", "knob", "recessed", "none"],
            index=["bar", "knob", "recessed", "none"].index(comp.handle_style),
            key="prop_hs",
        )

    elif isinstance(comp, HangingSpace):
        st.markdown("**Hanging Options**")
        tc1, tc2 = st.columns(2)
        comp.rail_type = tc1.selectbox(
            "Rail Type", options=["single", "double"],
            index=["single", "double"].index(comp.rail_type),
            key="prop_rt",
        )
        comp.clothing_type = tc2.selectbox(
            "Clothing Type",
            options=["full_length", "half_length", "shirts"],
            index=["full_length", "half_length", "shirts"].index(
                comp.clothing_type),
            key="prop_ct",
        )

    elif isinstance(comp, Shelf):
        st.markdown("**Shelf Options**")
        tc1, tc2 = st.columns(2)
        comp.adjustable = tc1.checkbox("Adjustable", value=comp.adjustable,
                                       key="prop_adj")
        comp.load_capacity = tc2.number_input(
            "Load Capacity (kg)", min_value=1.0, max_value=200.0,
            value=comp.load_capacity, step=5.0, key="prop_lc")

    elif isinstance(comp, Overhead):
        st.markdown("**Overhead Options**")
        tc1, tc2, tc3 = st.columns(3)
        comp.door_type = tc1.selectbox(
            "Door Type", options=["hinged", "lift_up", "sliding"],
            index=["hinged", "lift_up", "sliding"].index(comp.door_type),
            key="prop_dt",
        )
        comp.door_count = int(tc2.number_input(
            "Door Count", min_value=1, max_value=4,
            value=comp.door_count, step=1, key="prop_drc"))
        comp.has_shelf = tc3.checkbox("Has Shelf", value=comp.has_shelf,
                                      key="prop_hs2")

    comp.locked = st.checkbox("Locked", value=comp.locked, key="prop_locked")
    comp.notes = st.text_area("Notes", value=comp.notes or "",
                              key="prop_notes", height=60) or None


# ---------------------------------------------------------------------------
# Main area – component list
# ---------------------------------------------------------------------------

def component_list():
    """Display a list of components with selection."""
    project = _get_project()
    selected_id = st.session_state.get("selected_id")

    if not project.components:
        st.info("No components yet. Use the sidebar to add components from the library.")
        return

    st.subheader("Components")
    for comp in project.components:
        type_label = comp.component_type.name.replace("_", " ").title()
        is_selected = comp.id == selected_id
        label = f"{'>> ' if is_selected else ''}{comp.name} ({type_label}) " \
                f"- {_fmt(comp.dimensions.width)} x {_fmt(comp.dimensions.height)}"

        if st.button(label, key=f"sel_{comp.id}", use_container_width=True):
            if is_selected:
                st.session_state.pop("selected_id", None)
            else:
                st.session_state["selected_id"] = comp.id
            st.rerun()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    st.set_page_config(
        page_title=f"{APP_NAME} v{VERSION}",
        page_icon="🗄",
        layout="wide",
    )

    st.title(f"{APP_NAME}")
    st.caption(f"v{VERSION} — Design and plan wardrobe layouts")

    # --- Sidebar ---
    sidebar_project_management()
    sidebar_metadata()
    sidebar_unit_system()
    sidebar_frame_settings()
    sidebar_component_library()
    sidebar_export()

    # --- Main area ---
    project = _get_project()

    # Canvas
    fig = render_wardrobe(project, st.session_state.get("selected_id"))
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # Component list + property editor
    col_list, col_props = st.columns([1, 2])
    with col_list:
        component_list()
    with col_props:
        component_property_editor()


if __name__ == "__main__":
    main()
