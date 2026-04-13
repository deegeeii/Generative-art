
import { useState } from "react";

function PromptInput({ onGenerate }) {
    const [prompt, setPrompt] = useState('')
    const [loading, setLoading] = useState(false)
    const [aiParams, setAiParams] = useState(null)

    async function handleAIGenerate() {
        if (!prompt) return
        setLoading(true)

        const response = await fetch(`${import.meta.env.VITE_API_URL}/ai-prompt`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: prompt })
        })
        const data = await response.json()

        setAiParams(data.params)    // Show what Claude chose
        onGenerate(data.image)
        setLoading(false)
    }

    return (
        <div>
            <h2>AI Prompt</h2>
            <input
                type="text"
                placeholder="e.g. stormy ocean at midnight"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
            />
            <button className="btn-primary" onClick={handleAIGenerate} disabled={loading}>
                {loading ? 'Creating...' : 'AI Generate'}
            </button>
    
            {aiParams && (
                <div className="ai-result">
                    <p>Claude chose: <strong>{aiParams.mode}</strong></p>
                    <div className="swatches">
                        {aiParams.colors.map((color, i) => (
                            <div key={i} className="swatch" style={{ backgroundColor: color }} />
                        ))}
                    </div>
                </div>
            )}
        </div>
    )    

}

export default PromptInput