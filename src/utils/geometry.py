"""Geometric calculation utilities for wardrobe planning."""

from typing import Tuple


def point_in_rect(
    x: float, y: float, rect_x: float, rect_y: float, rect_w: float, rect_h: float
) -> bool:
    """
    Check if a point (x, y) is inside a rectangle.

    Args:
        x: Point x coordinate
        y: Point y coordinate
        rect_x: Rectangle left edge x coordinate
        rect_y: Rectangle top edge y coordinate
        rect_w: Rectangle width
        rect_h: Rectangle height

    Returns:
        True if point is inside rectangle, False otherwise
    """
    return rect_x <= x <= rect_x + rect_w and rect_y <= y <= rect_y + rect_h


def rects_intersect(
    rect1: Tuple[float, float, float, float], rect2: Tuple[float, float, float, float]
) -> bool:
    """
    Check if two rectangles intersect.

    Args:
        rect1: First rectangle as (x, y, width, height)
        rect2: Second rectangle as (x, y, width, height)

    Returns:
        True if rectangles intersect, False otherwise
    """
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    # Check for no overlap conditions
    if x1 + w1 <= x2 or x2 + w2 <= x1:
        return False
    if y1 + h1 <= y2 or y2 + h2 <= y1:
        return False

    return True


def snap_to_grid(value: float, grid_size: float) -> float:
    """
    Snap a value to the nearest grid point.

    Args:
        value: The value to snap
        grid_size: The grid spacing

    Returns:
        The value snapped to the nearest grid point
    """
    if grid_size <= 0:
        return value
    return round(value / grid_size) * grid_size


def calculate_scale_to_fit(
    content_w: float,
    content_h: float,
    container_w: float,
    container_h: float,
    margin: float = 0.0,
) -> float:
    """
    Calculate the scale factor to fit content within a container while preserving aspect ratio.

    Args:
        content_w: Width of the content to fit
        content_h: Height of the content to fit
        container_w: Width of the container
        container_h: Height of the container
        margin: Optional margin to leave around the content

    Returns:
        Scale factor to apply to content dimensions
    """
    if content_w <= 0 or content_h <= 0:
        return 1.0

    available_w = container_w - 2 * margin
    available_h = container_h - 2 * margin

    if available_w <= 0 or available_h <= 0:
        return 1.0

    scale_x = available_w / content_w
    scale_y = available_h / content_h

    # Return the smaller scale to ensure content fits in both dimensions
    return min(scale_x, scale_y)


def rect_contains_rect(
    outer: Tuple[float, float, float, float], inner: Tuple[float, float, float, float]
) -> bool:
    """
    Check if the outer rectangle fully contains the inner rectangle.

    Args:
        outer: Outer rectangle as (x, y, width, height)
        inner: Inner rectangle as (x, y, width, height)

    Returns:
        True if outer fully contains inner, False otherwise
    """
    ox, oy, ow, oh = outer
    ix, iy, iw, ih = inner

    return (
        ox <= ix
        and oy <= iy
        and ox + ow >= ix + iw
        and oy + oh >= iy + ih
    )


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Clamp a value to be within a specified range.

    Args:
        value: The value to clamp
        min_val: Minimum allowed value
        max_val: Maximum allowed value

    Returns:
        The clamped value
    """
    return max(min_val, min(max_val, value))
