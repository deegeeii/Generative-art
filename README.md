# Generative Art Studio

A full-stack generative art web app built with React, Python, and Claude AI. Describe a mood or scene in plain English and watch Claude translate it into original artwork using custom algorithms.

![Generative Art Studio](https://img.shields.io/badge/Stack-React%20%7C%20FastAPI%20%7C%20Claude-7c6ff7)

---

## Features

- **AI Prompt** — Describe a scene ("stormy ocean at midnight") and Claude picks the algorithm, colors, and parameters automatically
- **Flow Field** — Hundreds of particles follow a noise-based vector field, drawing organic curving lines
- **Fractal (Mandelbrot Set)** — Zoom into the infinite complexity of the Mandelbrot set with customizable detail
- **Geometric** — Layered translucent shapes with bold, modern compositions
- **Color Palettes** — Mood-based palettes (calm, neon, sunset, ocean, and more)
- **Gallery** — Save your favorite pieces locally; they persist across sessions via localStorage
- **Download** — Export any piece as a full-resolution PNG

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite |
| Backend | Python, FastAPI |
| AI | Anthropic Claude (`claude-opus-4-6`) |
| Image generation | NumPy, Pillow |
| Styling | CSS custom properties (dark theme) |

---

## Project Structure

```
generative-art-studio/
├── backend/
│   ├── main.py                  # FastAPI app, endpoints, Claude integration
│   ├── requirements.txt
│   └── algorithms/
│       ├── flow_field.py        # Particle flow field algorithm
│       ├── fractal.py           # Mandelbrot set renderer
│       ├── geometric.py         # Layered shape generator
│       └── palette.py           # Mood-based color palette generator
└── frontend/
    └── src/
        ├── App.jsx              # Root component, state management
        ├── index.css            # Dark theme, layout, component styles
        └── components/
            ├── PromptInput.jsx  # AI text prompt interface
            ├── Controls.jsx     # Algorithm selector and parameter sliders
            ├── Canvas.jsx       # Art display
            └── Gallery.jsx      # Saved artwork grid
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- An Anthropic API key ([get one here](https://console.anthropic.com))

### 1. Clone the repo

```bash
git clone https://github.com/deegeeii/Generative-art.git
cd Generative-art
```

### 2. Start the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

export ANTHROPIC_API_KEY=your_key_here   # Windows: set ANTHROPIC_API_KEY=your_key_here

uvicorn main:app --reload
```

The API runs at `http://localhost:8000`. Visit `http://localhost:8000/docs` to explore all endpoints interactively.

### 3. Start the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/ai-prompt` | Translate a text prompt into art via Claude |
| POST | `/generate` | Generate art with explicit parameters |
| POST | `/palette` | Get a mood-based color palette |

---

## How It Works

### AI Prompt Flow
1. User types a description (e.g. "cherry blossom storm")
2. The description is sent to Claude with a system prompt that defines the three available algorithms and their parameter shapes
3. Claude responds with a JSON object selecting the best algorithm and colors
4. The backend passes those parameters to the matching algorithm
5. The algorithm renders a PNG in memory and returns it as a base64 string
6. React displays the image directly — no file storage needed

### Image Generation
All images are generated server-side using NumPy for math and Pillow for drawing. Images are encoded as base64 strings and sent in the JSON response, so the frontend can display them with a standard `<img>` tag without any file uploads or static file hosting.

---

## Author

Built by Derek Green — [github.com/deegeeii](https://github.com/deegeeii)
