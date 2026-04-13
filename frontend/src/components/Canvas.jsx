
function Canvas({ imageData }) {
    return (
        <div className="canvas-wrapper">
            {imageData
                ? <img src={`data:image/png;base64,${imageData}`} alt="Generated Art" />
                : <p className="canvas-placeholder">Your art will appear here</p>
            }
        </div>
    )
}

export default Canvas
