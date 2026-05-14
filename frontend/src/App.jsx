import { Routes, Route, Navigate } from 'react-router-dom'
import Header from './components/Header'
import Footer from './components/Footer'
import HomePage from './pages/HomePage'
import PlantListPage from './pages/PlantListPage'
import PlantDetailPage from './pages/PlantDetailPage'

import { LoginPage } from './admin/pages/LoginPage'
import { DashboardPage } from './admin/pages/DashboardPage'
import { PlantsPage } from './admin/pages/PlantsPage'
import { SpiderPage } from './admin/pages/SpiderPage'
import { ProfilePage } from './admin/pages/ProfilePage'
import { ProtectedRoute } from './admin/components/ProtectedRoute'

function App() {
  return (
    <Routes>
      <Route path="/" element={
        <div className="min-h-screen flex flex-col bg-gray-50">
          <Header />
          <main className="flex-grow">
            <HomePage />
          </main>
          <Footer />
        </div>
      } />
      <Route path="/plants" element={
        <div className="min-h-screen flex flex-col bg-gray-50">
          <Header />
          <main className="flex-grow">
            <PlantListPage />
          </main>
          <Footer />
        </div>
      } />
      <Route path="/plants/:id" element={
        <div className="min-h-screen flex flex-col bg-gray-50">
          <Header />
          <main className="flex-grow">
            <PlantDetailPage />
          </main>
          <Footer />
        </div>
      } />

      <Route path="/admin/login" element={<LoginPage />} />
      <Route path="/admin/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
      <Route path="/admin/plants" element={<ProtectedRoute><PlantsPage /></ProtectedRoute>} />
      <Route path="/admin/spider" element={<ProtectedRoute><SpiderPage /></ProtectedRoute>} />
      <Route path="/admin/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
      <Route path="/admin" element={<Navigate to="/admin/dashboard" replace />} />
    </Routes>
  )
}

export default App
