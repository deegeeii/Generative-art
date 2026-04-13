
function Canvas({ imageData }) {
    if (!imageData) return <div>Your are art will appear here</div>

    return <img src={`data:image/png;base64,${imageData}`} alt="Generated Art" />
}

export default Canvas