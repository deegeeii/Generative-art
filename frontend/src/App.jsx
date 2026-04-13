import Canvas from './components/Canvas';
import Controls from './components/Controls';
import { useState } from 'react';

function App() {
    const [imageData, setImage] = useState(null) //  no image yet

    return (
        <div>
            <h1>Generative Art Studio</h1>
            <Controls onGenerate={setImage} />
            <Canvas imageData={imageData} />
        </div>
    )
}

export default App
