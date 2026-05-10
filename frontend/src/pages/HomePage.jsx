import { Link } from 'react-router-dom'
import PlantCard from '../components/PlantCard'
import {
  getAllPlants,
  getStatistics,
  getProtectedPlants,
  getAllFamilies,
  getAllGardenZones
} from '../utils/plantUtils'

function HomePage() {
  const plants = getAllPlants()
  const stats = getStatistics()
  const protectedPlants = getProtectedPlants()
  const featuredPlants = plants.slice(0, 6)
  const families = getAllFamilies()
  const zones = getAllGardenZones()

  return (
    <div className="min-h-screen">
      <section className="relative bg-gradient-to-r from-primary-700 via-primary-600 to-primary-500 text-white py-16 md:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="text-center">
            <h1 className="text-3xl md:text-5xl font-bold mb-4">
              北京植物园植物数据库
            </h1>
            <p className="text-lg md:text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
              探索北京植物园的植物资源，了解植物的分类、生态习性和保护价值
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <Link
                to="/plants"
                className="px-8 py-3 bg-white text-primary-700 font-semibold rounded-lg hover:bg-primary-50 transition-colors shadow-lg"
              >
                浏览全部植物
              </Link>
              <Link
                to="/plants"
                className="px-8 py-3 bg-primary-500 text-white font-semibold rounded-lg hover:bg-primary-400 transition-colors border-2 border-white"
              >
                搜索植物
              </Link>
            </div>
          </div>
        </div>
        <div className="absolute bottom-0 left-0 right-0 h-16 bg-gradient-to-t from-gray-50 to-transparent"></div>
      </section>

      <section className="py-12 -mt-8 relative z-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white rounded-xl shadow-lg p-6 text-center border border-gray-100">
              <div className="text-3xl font-bold text-primary-600">{stats.total}</div>
              <div className="text-gray-500 mt-1">植物种类</div>
            </div>
            <div className="bg-white rounded-xl shadow-lg p-6 text-center border border-gray-100">
              <div className="text-3xl font-bold text-primary-600">{stats.families}</div>
              <div className="text-gray-500 mt-1">植物科属</div>
            </div>
            <div className="bg-white rounded-xl shadow-lg p-6 text-center border border-gray-100">
              <div className="text-3xl font-bold text-primary-600">{stats.protected}</div>
              <div className="text-gray-500 mt-1">保护植物</div>
            </div>
            <div className="bg-white rounded-xl shadow-lg p-6 text-center border border-gray-100">
              <div className="text-3xl font-bold text-primary-600">{stats.zones}</div>
              <div className="text-gray-500 mt-1">园区分布</div>
            </div>
          </div>
        </div>
      </section>

      <section className="py-12 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">精选植物</h2>
              <p className="text-gray-500 mt-1">了解北京植物园的代表性植物</p>
            </div>
            <Link
              to="/plants"
              className="text-primary-600 hover:text-primary-700 font-medium"
            >
              查看全部 →
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {featuredPlants.map(plant => (
              <PlantCard key={plant.id} plant={plant} />
            ))}
          </div>
        </div>
      </section>

      {protectedPlants.length > 0 && (
        <section className="py-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="bg-gradient-to-r from-red-50 to-orange-50 rounded-2xl p-8 border border-red-100">
              <div className="flex items-center mb-6">
                <span className="text-3xl mr-3">🛡️</span>
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">珍稀保护植物</h2>
                  <p className="text-gray-500">北京植物园的国家保护植物资源</p>
                </div>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {protectedPlants.slice(0, 6).map(plant => (
                  <Link
                    key={plant.id}
                    to={`/plants/${plant.id}`}
                    className="flex items-center p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow"
                  >
                    <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mr-4">
                      <span className="text-2xl">🌿</span>
                    </div>
                    <div>
                      <div className="font-semibold text-gray-900">{plant.name_cn}</div>
                      <div className="text-sm text-red-600">{plant.protection_status}</div>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </section>
      )}

      <section className="py-12 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-8">按科属浏览</h2>
          <div className="flex flex-wrap gap-3">
            {families.slice(0, 15).map(family => (
              <Link
                key={family}
                to={`/plants?family=${encodeURIComponent(family)}`}
                className="px-4 py-2 bg-white rounded-full shadow-sm hover:shadow-md transition-shadow text-gray-700 hover:text-primary-600 border border-gray-200"
              >
                {family}
              </Link>
            ))}
          </div>

          <h2 className="text-2xl font-bold text-gray-900 mt-12 mb-8">按园区浏览</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {zones.slice(0, 12).map(zone => (
              <Link
                key={zone}
                to={`/plants?zone=${encodeURIComponent(zone)}`}
                className="p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow text-center"
              >
                <span className="text-2xl block mb-2">🌳</span>
                <span className="text-gray-700 font-medium">{zone}</span>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}

export default HomePage
