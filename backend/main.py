# main.py
# This is the entry point for our Python backend.
# FastAPI is a modern Python web framework that lets us create API endpoints.
# An API endpoint is just a URL that the frontend can send requests to.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# BaseModel from pydantic lets us define the shape of incoming request data.
# FastAPI uses it to automatically validate JSON bodies — if a required field
# is missing or the wrong type, it returns a helpful error automatically.
from pydantic import BaseModel
from typing import List, Optional

# Import our algorithm functions
from algorithms.flow_field import generate_flow_field
from algorithms.fractal import generate_fractal
from algorithms.geometric import generate_geometric
from algorithms.palette import generate_palette

# Create the FastAPI app instance.
# Think of this like turning on the server — everything else attaches to this.
app = FastAPI(title="Generative Art Studio API")

# CORS = Cross-Origin Resource Sharing.
# Browsers block requests between different ports by default (e.g. port 5173 → port 8000).
# This middleware tells the server: "It's okay to accept requests from our React app."
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Create React App default port
        "http://localhost:5173",  # Vite default port (what we're using)
    ],
    allow_credentials=True,
    allow_methods=["*"],   # Allow GET, POST, etc.
    allow_headers=["*"],   # Allow any request headers
)


# --- Request Models ---
# These define what JSON data the frontend must send with each request.
# Optional fields have default values so they don't have to be sent every time.

class GenerateRequest(BaseModel):
    mode: str = "flow_field"          # Which art algorithm to use
    seed: int = 42                    # Random seed for reproducibility
    colors: Optional[List[str]] = None  # List of hex colors e.g. ["#FF6B6B", "#4ECDC4"]
    width: int = 800
    height: int = 800
    # Flow field options
    num_particles: int = 1500
    noise_scale: float = 0.003
    step_length: float = 3.0
    steps: int = 80
    # Fractal options
    max_iter: int = 100
    zoom: float = 1.0
    offset_x: float = -0.5
    offset_y: float = 0.0
    # Geometric options
    num_shapes: int = 60
    shape_type: str = "mixed"


class PaletteRequest(BaseModel):
    mood: Optional[str] = None   # e.g. "calm", "energetic", "dark"
    seed: Optional[int] = None


# --- Endpoints ---

# Simple health check — visit http://localhost:8000/ to confirm the server is running.
@app.get("/")
def root():
    return {"message": "Generative Art Studio API is running"}


# POST /generate
# The frontend sends art parameters, and we return a base64-encoded PNG image.
# We use POST (not GET) because we're sending a body of data, not just URL params.
@app.post("/generate")
def generate(req: GenerateRequest):
    # Route to the correct algorithm based on the "mode" field
    if req.mode == "flow_field":
        image_data = generate_flow_field(
            width=req.width,
            height=req.height,
            seed=req.seed,
            colors=req.colors,
            num_particles=req.num_particles,
            noise_scale=req.noise_scale,
            step_length=req.step_length,
            steps=req.steps,
        )
    elif req.mode == "fractal":
        image_data = generate_fractal(
            width=req.width,
            height=req.height,
            seed=req.seed,
            colors=req.colors,
            max_iter=req.max_iter,
            zoom=req.zoom,
            offset_x=req.offset_x,
            offset_y=req.offset_y,
        )
    elif req.mode == "geometric":
        image_data = generate_geometric(
            width=req.width,
            height=req.height,
            seed=req.seed,
            colors=req.colors,
            num_shapes=req.num_shapes,
            shape_type=req.shape_type,
        )
    else:
        # If an unknown mode is sent, return a clear error
        return {"error": f"Unknown mode '{req.mode}'. Choose: flow_field, fractal, geometric"}

    # Return the base64 image string and the mode used
    # The frontend will display this as: <img src="data:image/png;base64,{image}" />
    return {
        "image": image_data,
        "mode": req.mode,
        "seed": req.seed,
    }


# POST /palette
# The frontend sends a mood keyword and gets back 5 harmonious hex colors.
@app.post("/palette")
def palette(req: PaletteRequest):
    result = generate_palette(mood=req.mood, seed=req.seed)
    return result
