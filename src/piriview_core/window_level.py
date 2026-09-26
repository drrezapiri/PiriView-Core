"""Window and level utilities for PiriView Core."""

import numpy as np


def apply_window_level(
    pixel_array: np.ndarray,
    window_center: float,
    window_width: float,
) -> np.ndarray:
    """Convert image values to an 8-bit grayscale image."""

    if window_width <= 0:
        raise ValueError("Window width must be greater than zero")

    lower = window_center - window_width / 2.0
    upper = window_center + window_width / 2.0

    clipped = np.clip(
        pixel_array.astype(np.float32),
        lower,
        upper,
    )

    normalized = (
        (clipped - lower)
        / (upper - lower)
        * 255.0
    )

    return normalized.astype(np.uint8)
    