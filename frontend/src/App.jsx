
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
            id: Date.now,
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
        <div>
            <h1>Generative Art Studio</h1>
            <Controls onGenerate={setImage} />
            <Canvas imageData={imageData} />
            <button onClick={handleSave}>Save to Gallery</button>
            <Gallery items={gallery} onDelete={handleDelete} />
        </div>
    )
}

export default App
