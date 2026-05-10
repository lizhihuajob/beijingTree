import { Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import Footer from './components/Footer'
import HomePage from './pages/HomePage'
import PlantListPage from './pages/PlantListPage'
import PlantDetailPage from './pages/PlantDetailPage'

function App() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Header />
      <main className="flex-grow">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/plants" element={<PlantListPage />} />
          <Route path="/plants/:id" element={<PlantDetailPage />} />
        </Routes>
      </main>
      <Footer />
    </div>
  )
}

export default App
