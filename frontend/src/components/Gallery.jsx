

function Gallery({ items, onDelete }) {
    if (items.length === 0) return <p>No saved artwork yet.</p>

    return (
        <div>
            <h2>Gallery</h2>
            {items.map((item) => (
                <div key={item.id}>
                    <img 
                        src={`data:image/png;base64,${item.image}`}
                        alt={item.mode}
                        width="200"
                    />
                    <p>{item.mode} - {item.date}</p>
                    <button onClick={() => onDelete(item.id)}>Delete</button>
                </div>
            ))}
        </div>
    )
}

export default Gallery