

function Gallery({ items, onDelete }) {
    if (items.length === 0) return null

    return (
        <div className="gallery">
            <h2>Gallery</h2>
            <div className="gallery-grid">
                {items.map((item) => (
                    <div key={item.id} className="gallery-item">
                        <img
                            src={`data:image/png;base64,${item.image}`}
                            alt="Saved artwork"
                        />
                        <div className="gallery-item-footer">
                            <span className="gallery-item-date">{item.date}</span>
                            <button className="btn-danger" onClick={() => onDelete(item.id)}>Delete</button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default Gallery
