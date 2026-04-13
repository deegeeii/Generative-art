
import PromptInput from './components/PromptInput';
import Canvas from './components/Canvas';
import Controls from './components/Controls';
import Gallery from './components/Gallery';
import { useState, useEffect } from 'react';

function App() {
    const [imageData, setImage] = useState(null) //  no image yet

    // Load gallery from localStorage when the app first opens
    const [gallery, setGallery] = useState(() => {
        const saved = localStorage.getItem('gallery')
        return saved ? JSON.parse(saved) : []
    })

    // Whenever gallery changes, save it to localStorage
    useEffect(() => {
        localStorage.setItem('gallery', JSON.stringify(gallery))
    }, [gallery])

    // Save the current canvas image to the gallery
    function handleSave() {
        if (!imageData) return
        const newPiece = {
            id: Date.now(),
            image: imageData,
            node: 'artwork',
            date: new Date().toLocaleDateString()
        }
        setGallery([newPiece, ...gallery])
    }

    // Remove a piece from the gallery by its id
    function handleDelete(id) {
        setGallery(gallery.filter((item) => item.id !== id))
    }
    return (
        <div className="app">
            <header className="app-header">
                <h1>Generative Art Studio</h1>
                <div className="btn-row">
                    <button className="btn-secondary" onClick={handleSave}>Save to Gallery</button>
                    <button className="btn-primary" onClick={handleDownload}>Download PNG</button>
                </div>
            </header>
    
            <div className="app-body">
                <aside className="sidebar">
                    <div className="card">
                        <PromptInput onGenerate={setImage} />
                    </div>
                    <div className="card">
                        <Controls onGenerate={setImage} />
                    </div>
                </aside>
    
                <div className="main-panel">
                    <Canvas imageData={imageData} />
                </div>
            </div>
    
            <Gallery items={gallery} onDelete={handleDelete} />
        </div>
    )    

    function handleDownload() {
        if (!imageData) return

        // Convert the base64 string back into raw bytes
        const byteCharacters = atob(imageData)
        const byteNumbers = Array.from(byteCharacters).map(c => c.charCodeAt(0))
        const byteArray = new Uint8Array(byteNumbers)

        // Wrap the bytes in Blob - this is how browsers represent file data in memory
        const blob = new Blob([byteArray], { type: 'image/png' })

        // Create a temporary invisible  link pointing to the blob
        const url = URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `generative-art-${Date.now()}.png`  // filename for the downloaded file

        // Trigger the download, then clean up
        link.click()
        URL.revokeObjectURL(url)  // frees memory (always clean up blob URLs)

    }
}

export default App
