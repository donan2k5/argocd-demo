export default function PlaceCard({ place }) {
  return (
    <div className="card">
      <div className="card-image">
        <img
          src={place.image_url}
          alt={place.name}
          onError={(e) => {
            e.target.src = 'https://placehold.co/400x220/0ea5e9/white?text=Da+Nang'
          }}
        />
        <span className="badge" data-category={place.category}>{place.category}</span>
      </div>
      <div className="card-body">
        <h2>{place.name}</h2>
        <p>{place.description}</p>
      </div>
    </div>
  )
}
