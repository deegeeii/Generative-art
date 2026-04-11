# geometric.py
# This algorithm draws layered geometric shapes — circles, triangles, and rectangles —
# at random positions, sizes, and transparencies.
# Overlapping transparent shapes create depth and a painterly feel.

import numpy as np
from PIL import Image, ImageDraw
import io
import base64
import math


def generate_geometric(
    width: int = 800,
    height: int = 800,
    seed: int = 42,
    colors: list = None,
    num_shapes: int = 60,           # Total number of shapes to draw
    shape_type: str = "mixed",      # "circles", "triangles", "rectangles", or "mixed"
) -> str:
    rng = np.random.default_rng(seed)

    if colors is None:
        colors = ["#2C3E50", "#E74C3C", "#3498DB", "#2ECC71", "#F39C12"]

    def hex_to_rgb(hex_color: str):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    rgb_colors = [hex_to_rgb(c) for c in colors]

    # Use the first color as the background
    bg_color = rgb_colors[0]
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img, "RGBA")

    for _ in range(num_shapes):
        # Pick a random color (skip index 0 — that's the background)
        color = rgb_colors[rng.integers(1, len(rgb_colors))]
        alpha = rng.integers(40, 140)    # Semi-transparent so shapes layer nicely
        cx = rng.integers(0, width)      # Center X
        cy = rng.integers(0, height)     # Center Y
        size = rng.integers(20, 180)     # Rough size of the shape

        # Decide which shape to draw
        if shape_type == "mixed":
            pick = rng.choice(["circles", "triangles", "rectangles"])
        else:
            pick = shape_type

        if pick == "circles":
            # draw.ellipse takes a bounding box: top-left corner and bottom-right corner.
            draw.ellipse(
                [(cx - size, cy - size), (cx + size, cy + size)],
                outline=(*color, alpha),
                width=rng.integers(1, 4),
            )

        elif pick == "triangles":
            # A triangle needs 3 points.
            # We calculate them evenly spaced around a circle using trigonometry.
            # angle rotates the whole triangle randomly.
            angle = rng.uniform(0, math.pi * 2)
            pts = [
                (
                    cx + size * math.cos(angle + i * 2 * math.pi / 3),
                    cy + size * math.sin(angle + i * 2 * math.pi / 3)
                )
                for i in range(3)
            ]
            # Fill is very faint; outline is more visible — gives a wireframe-ish look
            draw.polygon(pts, fill=(*color, alpha // 3), outline=(*color, alpha))

        elif pick == "rectangles":
            w = rng.integers(20, size * 2)
            h = rng.integers(20, size * 2)
            draw.rectangle(
                [(cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2)],
                fill=(*color, alpha // 4),
                outline=(*color, alpha),
                width=rng.integers(1, 3),
            )

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")
