import { useState, useEffect } from 'react'
import PlaceCard from './components/PlaceCard'
import './App.css'

const BE_URL = import.meta.env.VITE_BE_URL || '/api'

export default function App() {
  const [places, setPlaces] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch(`${BE_URL}/places`)
      .then((res) => {
        if (!res.ok) throw new Error('Không thể tải dữ liệu')
        return res.json()
      })
      .then((data) => {
        setPlaces(data)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  return (
    <div className="app">
      <header className="header">
        <h1>🌊 Địa Điểm Đẹp Đà Nẵng</h1>
        <p>Khám phá những địa điểm tuyệt vời tại thành phố đáng sống nhất Việt Nam</p>
      </header>

      <main className="main">
        {loading && <div className="status">Đang tải...</div>}
        {error && <div className="status error">Lỗi: {error}</div>}
        {!loading && !error && (
          <div className="grid">
            {places.map((place) => (
              <PlaceCard key={place.id} place={place} />
            ))}
          </div>
        )}
      </main>

      <footer className="footer">
        <p>Made with ❤️ — ArgoCD GitOps Demo</p>
      </footer>
    </div>
  )
}
