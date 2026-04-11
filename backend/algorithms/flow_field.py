# flow_field.py
# A flow field is an invisible grid of angles.
# We place hundreds of particles on the canvas, and each particle moves
# in the direction that the angle at its position tells it to go.
# Over many small steps, they draw beautiful curving lines.

import numpy as np       # numpy handles fast math and arrays
from PIL import Image, ImageDraw  # Pillow creates and draws on images
import io                # io lets us work with data in memory (no temp files needed)
import base64            # base64 encodes image bytes into a string we can send to the frontend
import math              # math gives us sin, cos, and pi


def generate_flow_field(
    width: int = 800,          # Canvas width in pixels
    height: int = 800,         # Canvas height in pixels
    seed: int = 42,            # Seed makes random numbers repeatable (same seed = same art)
    colors: list = None,       # List of hex color strings like ["#FF6B6B", "#4ECDC4"]
    num_particles: int = 1500, # How many particles travel across the canvas
    noise_scale: float = 0.003,# Controls how "zoomed in" the flow field is (smaller = smoother curves)
    step_length: float = 3.0,  # How far each particle moves per step (in pixels)
    steps: int = 80,           # How many steps each particle takes before stopping
) -> str:
    # Create a random number generator using the seed.
    # np.random.default_rng is newer and better than the old np.random.seed().
    rng = np.random.default_rng(seed)

    # Default colors if none are provided
    if colors is None:
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]

    # Helper: convert a hex string like "#FF6B6B" into an RGB tuple like (255, 107, 107)
    # The frontend and CSS use hex — Pillow needs RGB tuples.
    def hex_to_rgb(hex_color: str):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    rgb_colors = [hex_to_rgb(c) for c in colors]

    # Create the blank canvas with a dark background.
    # "RGBA" mode supports transparency (the A = Alpha channel).
    img = Image.new("RGB", (width, height), (15, 15, 25))

    # ImageDraw lets us draw lines and shapes on the image.
    # We pass "RGBA" so we can draw with transparency (for soft, layered lines).
    draw = ImageDraw.Draw(img, "RGBA")

    # This function returns the "flow angle" at any (x, y) position.
    # We combine layered sine and cosine waves to create a smooth, interesting field.
    # Think of it like wind — at every point in the sky, the wind blows a certain direction.
    def noise_angle(x, y):
        val = (
            math.sin(x * noise_scale + y * noise_scale * 0.5) +
            math.sin(x * noise_scale * 0.5 - y * noise_scale * 1.2) * 0.5 +
            math.cos(x * noise_scale * 0.8 + y * noise_scale * 0.3) * 0.3
        )
        # Multiply by 2π to convert to a full-circle angle (in radians)
        return val * math.pi * 2

    # Randomly place all particles across the canvas at the start.
    # rng.uniform gives us random floats between 0 and width/height.
    px = rng.uniform(0, width, num_particles)
    py = rng.uniform(0, height, num_particles)

    # Move each particle step by step, drawing a line segment at each step.
    for i in range(num_particles):
        # Cycle through our color list (% wraps back to 0 when we exceed list length)
        color = rgb_colors[i % len(rgb_colors)]

        # Random transparency per particle — makes lines overlap softly
        alpha = rng.integers(80, 160)

        x, y = px[i], py[i]

        for _ in range(steps):
            angle = noise_angle(x, y)

            # Move in the direction of the angle using trigonometry:
            # cos(angle) = horizontal movement, sin(angle) = vertical movement
            nx = x + math.cos(angle) * step_length
            ny = y + math.sin(angle) * step_length

            # Only draw if the new position is still on the canvas
            if 0 <= nx < width and 0 <= ny < height:
                draw.line(
                    [(x, y), (nx, ny)],
                    fill=(*color, alpha),  # Unpack RGB + add alpha
                    width=1,
                )
                x, y = nx, ny
            else:
                break  # Particle has left the canvas — stop this particle

    # Save the image to an in-memory buffer (not a file on disk).
    # BytesIO works like a file but lives in RAM.
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)  # Rewind the buffer to the beginning so we can read it

    # Encode the image bytes as a base64 string.
    # This lets us send the image directly in a JSON response.
    return base64.b64encode(buffer.read()).decode("utf-8")
