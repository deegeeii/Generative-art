# palette.py
# This module generates color palettes based on a "mood" keyword.
# Color theory: related hues placed around the color wheel create harmony.
# We use Python's built-in colorsys module to convert between HSL and RGB.
#
# HSL = Hue, Saturation, Lightness
#   Hue: the color (0-360 degrees around the color wheel — 0=red, 120=green, 240=blue)
#   Saturation: how vivid vs. gray (0% = gray, 100% = fully vivid)
#   Lightness: how dark vs. bright (0% = black, 100% = white, 50% = normal)

import colorsys
import random

# Each mood maps to a list of 5 base hues (in degrees, 0-360).
# We'll add slight random variation to each so the palette feels alive, not robotic.
MOOD_HUES = {
    "calm":      [200, 210, 220, 180, 190],   # Cool blues and teals
    "energetic": [0, 15, 30, 330, 350],        # Reds and warm oranges
    "dark":      [260, 270, 240, 280, 250],    # Deep purples
    "nature":    [120, 130, 80, 90, 140],      # Greens and yellow-greens
    "sunset":    [20, 30, 40, 350, 10],        # Oranges and warm pinks
    "ocean":     [190, 200, 210, 170, 220],    # Cyan and sky blues
    "neon":      [300, 180, 60, 120, 240],     # Wild spread across the wheel
    "minimal":   [0, 30, 60, 90, 0],           # Neutral/earthy tones
}

DEFAULT_MOODS = list(MOOD_HUES.keys())


def _hsl_to_hex(h: float, s: float, l: float) -> str:
    """
    Convert HSL values to a hex color string.
    colorsys uses HLS order (not HSL) and expects values between 0 and 1.
    So we divide hue by 360 to normalize it.
    """
    r, g, b = colorsys.hls_to_rgb(h / 360, l, s)
    return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))


def generate_palette(mood: str = None, seed: int = None) -> dict:
    """
    Generate a 5-color palette based on a mood keyword.
    Returns a dict with the mood name, list of hex colors, and a suggested background color.
    """
    # random.Random(seed) creates an isolated random generator.
    # This means calling this function won't affect random numbers anywhere else.
    rng = random.Random(seed)

    # Normalize the input — lowercase and strip whitespace
    if mood:
        mood = mood.lower().strip()

    # If the mood isn't in our list, try a partial match (e.g. "dark night" → "dark")
    if mood not in MOOD_HUES:
        mood = next(
            (m for m in MOOD_HUES if m in (mood or "") or (mood or "") in m),
            rng.choice(DEFAULT_MOODS)   # Fall back to a random mood if nothing matches
        )

    base_hues = MOOD_HUES[mood]
    colors = []

    for base_hue in base_hues:
        # Add a small random variation so the palette feels handcrafted
        hue = (base_hue + rng.uniform(-15, 15)) % 360
        saturation = rng.uniform(0.55, 0.95)
        lightness = rng.uniform(0.35, 0.75)
        colors.append(_hsl_to_hex(hue, saturation, lightness))

    # Suggest a dark background color using the complementary hue (opposite on the wheel)
    background = _hsl_to_hex(
        (base_hues[0] + 180) % 360,
        0.15,   # Low saturation — nearly gray
        0.08,   # Very dark
    )

    return {
        "mood": mood,
        "colors": colors,
        "background": background,
    }
