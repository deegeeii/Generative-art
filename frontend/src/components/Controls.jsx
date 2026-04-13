import { useState } from 'react';

function Controls({ onGenerate }) {
    const [algorithm, setAlgorithm] = useState('flow_field')  // 👈 this line is missing
    const [numParticles, setNumParticles] = useState(1500)
    const [steps, setSteps] = useState(80)
    const [maxIter, setMaxIter] = useState(100)
    const [zoom, setZoom] = useState(1.0)
    const [mood, setMood] = useState('calm')
    const [palette, setPalette] = useState(null)

    async function handleGenerate() {
        const response = await fetch('http://localhost:8000/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                mode: algorithm,
                num_particles: numParticles,
                steps: steps,
                zoom: zoom,
                max_iter: maxIter,
                colors: palette
            })
        })
        const data = await response.json()
        onGenerate(data.image)
    }

    async function handlePalette() {
        const response = await fetch('http://localhost:8000/palette', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mood: mood })
        })
        const data = await response.json()
        setPalette(data.colors)
    }

    return (
        <div>
            {/* Algorithm dropdown — always visible */}
            <select value={algorithm} onChange={(e) => setAlgorithm(e.target.value)}>
                <option value="flow_field">Flow Field</option>
                <option value="fractal">Fractal</option>
                <option value="geometric">Geometric</option>
            </select>

            {/* Flow field sliders — only show when flow_field is selected */}
            {algorithm === 'flow_field' && (
                <div>
                    <label>Particles: {numParticles}</label>
                    <input
                        type="range"
                        min="100"
                        max="3000"
                        value={numParticles}
                        onChange={(e) => setNumParticles(Number(e.target.value))}
                    />
                    <label>Steps: {steps}</label>
                    <input
                        type="range"
                        min="10"
                        max="200"
                        value={steps}
                        onChange={(e) => setSteps(Number(e.target.value))}
                    />
                </div>
            )}

            {/* Fractal sliders — only show when fractal is selected */}
            {algorithm === 'fractal' && (
                <div>
                    <label>Zoom: {zoom}</label>
                    <input
                        type="range"
                        min="1"
                        max="50"
                        step="0.5"
                        value={zoom}
                        onChange={(e) => setZoom(Number(e.target.value))}
                    />
                    <label>Detail: {maxIter}</label>
                    <input
                        type="range"
                        min="20"
                        max="500"
                        value={maxIter}
                        onChange={(e) => setMaxIter(Number(e.target.value))}
                    />
                </div>
            )}

            {/* Palette picker — always visible */}
            <div>
                <select value={mood} onChange={(e) => setMood(e.target.value)}>
                    <option value="calm">Calm</option>
                    <option value="energetic">Energetic</option>
                    <option value="dark">Dark</option>
                    <option value="nature">Nature</option>
                    <option value="sunset">Sunset</option>
                    <option value="ocean">Ocean</option>
                    <option value="neon">Neon</option>
                    <option value="minimal">Minimal</option>
                </select>
                <button onClick={handlePalette}>Get Palette</button>
            </div>

            {/* Color swatches — only show once a palette has been fetched */}
            {palette && (
                <div>
                    {palette.map((color, index) => (
                        <div
                            key={index}
                            style={{
                                backgroundColor: color,
                                width: '40px',
                                height: '40px',
                                display: 'inline-block'
                            }}
                        />
                    ))}
                </div>
            )}
            {/* Generate button — always visible */}
            <button onClick={handleGenerate}>Generate</button>
        </div>
    )
}

export default Controls
