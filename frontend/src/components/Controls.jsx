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
            <h2>Controls</h2>
            <label>Algorithm</label>
            <select value={algorithm} onChange={(e) => setAlgorithm(e.target.value)}>
                <option value="flow_field">Flow Field</option>
                <option value="fractal">Fractal</option>
                <option value="geometric">Geometric</option>
            </select>
    
            {algorithm === 'flow_field' && (
                <div>
                    <label>Particles: {numParticles}</label>
                    <input type="range" min="100" max="3000" value={numParticles}
                        onChange={(e) => setNumParticles(Number(e.target.value))} />
                    <label>Steps: {steps}</label>
                    <input type="range" min="10" max="200" value={steps}
                        onChange={(e) => setSteps(Number(e.target.value))} />
                </div>
            )}
    
            {algorithm === 'fractal' && (
                <div>
                    <label>Zoom: {zoom}</label>
                    <input type="range" min="1" max="50" step="0.5" value={zoom}
                        onChange={(e) => setZoom(Number(e.target.value))} />
                    <label>Detail: {maxIter}</label>
                    <input type="range" min="20" max="500" value={maxIter}
                        onChange={(e) => setMaxIter(Number(e.target.value))} />
                </div>
            )}
    
            <label>Color Mood</label>
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
    
            <div className="btn-row">
                <button className="btn-secondary" onClick={handlePalette}>Get Palette</button>
                <button className="btn-primary" onClick={handleGenerate}>Generate</button>
            </div>
    
            {palette && (
                <div className="swatches">
                    {palette.map((color, index) => (
                        <div key={index} className="swatch" style={{ backgroundColor: color }} />
                    ))}
                </div>
            )}
        </div>
    )
}

export default Controls
