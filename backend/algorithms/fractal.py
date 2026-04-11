# fractal.py
# The Mandelbrot set is one of the most famous fractals in mathematics.
# For every pixel (x, y) on the canvas, we treat it as a complex number C.
# We then repeatedly apply the formula: Z = Z² + C
# If Z stays small (doesn't "escape" to infinity), the point is IN the set.
# If Z grows large quickly, it's OUTSIDE — and the number of steps before
# it escaped becomes the color. This creates the infinitely detailed boundary.

import numpy as np
from PIL import Image
import io
import base64


def generate_fractal(
    width: int = 800,
    height: int = 800,
    seed: int = 42,            # Seed is accepted for API consistency (not used here — fractals are deterministic)
    colors: list = None,       # Color palette — applied as a gradient across escape times
    max_iter: int = 100,       # More iterations = more detail but slower
    zoom: float = 1.0,         # Zoom level — higher zoom = more detail at a specific spot
    offset_x: float = -0.5,   # Pan the view horizontally
    offset_y: float = 0.0,    # Pan the view vertically
) -> str:
    if colors is None:
        colors = ["#0D0221", "#FF6B6B", "#4ECDC4", "#FFE66D", "#FFFFFF"]

    def hex_to_rgb(hex_color: str):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    rgb_colors = [hex_to_rgb(c) for c in colors]

    # Build a grid of complex numbers — one per pixel.
    # np.linspace gives us evenly spaced values between two numbers.
    # The zoom and offset let us look at different parts of the fractal.
    x = np.linspace(-2.0 / zoom + offset_x, 1.0 / zoom + offset_x, width)
    y = np.linspace(-1.5 / zoom + offset_y, 1.5 / zoom + offset_y, height)

    # np.newaxis adds a dimension so we can combine x and y into a 2D grid.
    # C is a 2D array of complex numbers — one for each pixel.
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    # Z starts at 0 for every pixel.
    Z = np.zeros_like(C)

    # M stores the "escape iteration" for each pixel (0 means it never escaped).
    M = np.zeros(C.shape, dtype=int)

    # mask tracks which pixels are still being iterated (haven't escaped yet).
    mask = np.ones(C.shape, dtype=bool)

    # Run the Mandelbrot iteration up to max_iter times.
    for i in range(max_iter):
        # Only update pixels that haven't escaped yet (mask == True).
        Z[mask] = Z[mask] ** 2 + C[mask]

        # Find pixels where |Z| > 2 — these have escaped.
        escaped = mask & (np.abs(Z) > 2)

        # Record which iteration this pixel escaped on.
        M[escaped] = i

        # Remove escaped pixels from future iterations.
        mask[escaped] = False

    # Now paint each pixel.
    # We divide the iteration range into bands and interpolate between colors.
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    num_colors = len(rgb_colors)

    for idx in range(1, num_colors):
        # Each color band covers an equal slice of the iteration range.
        lo = int((idx - 1) / num_colors * max_iter)
        hi = int(idx / num_colors * max_iter)
        band = (M >= lo) & (M < hi)

        c1 = np.array(rgb_colors[idx - 1])
        c2 = np.array(rgb_colors[idx % num_colors])

        # t is a value between 0 and 1 — how far into this band are we?
        # We use it to blend (interpolate) between the two colors smoothly.
        t = ((M[band] - lo) / max(hi - lo, 1))[:, np.newaxis]
        img_array[band] = (c1 * (1 - t) + c2 * t).astype(np.uint8)

    # Pixels still in the set (never escaped) get the darkest color.
    img_array[mask] = rgb_colors[0]

    img = Image.fromarray(img_array, "RGB")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")
