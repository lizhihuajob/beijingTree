import { useState, useEffect, useMemo } from 'react'
import { useSearchParams } from 'react-router-dom'
import PlantCard from '../components/PlantCard'
import {
  searchPlants,
  getAllFamilies,
  getAllGardenZones,
  getPlantsByFamily,
  getPlantsByGardenZone
} from '../utils/plantUtils'

function PlantListPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedFamily, setSelectedFamily] = useState('')
  const [selectedZone, setSelectedZone] = useState('')

  const families = getAllFamilies()
  const zones = getAllGardenZones()

  useEffect(() => {
    const familyParam = searchParams.get('family')
    const zoneParam = searchParams.get('zone')
    
    if (familyParam) {
      setSelectedFamily(decodeURIComponent(familyParam))
    }
    if (zoneParam) {
      setSelectedZone(decodeURIComponent(zoneParam))
    }
  }, [searchParams])

  const filteredPlants = useMemo(() => {
    let plants = []

    if (selectedFamily) {
      plants = getPlantsByFamily(selectedFamily)
    } else if (selectedZone) {
      plants = getPlantsByGardenZone(selectedZone)
    } else {
      plants = searchPlants(searchTerm)
    }

    if (searchTerm && !selectedFamily && !selectedZone) {
      plants = searchPlants(searchTerm)
    }

    return plants
  }, [searchTerm, selectedFamily, selectedZone])

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value)
    setSelectedFamily('')
    setSelectedZone('')
    setSearchParams({})
  }

  const handleFamilyChange = (e) => {
    const value = e.target.value
    setSelectedFamily(value)
    setSelectedZone('')
    setSearchTerm('')
    if (value) {
      setSearchParams({ family: encodeURIComponent(value) })
    } else {
      setSearchParams({})
    }
  }

  const handleZoneChange = (e) => {
    const value = e.target.value
    setSelectedZone(value)
    setSelectedFamily('')
    setSearchTerm('')
    if (value) {
      setSearchParams({ zone: encodeURIComponent(value) })
    } else {
      setSearchParams({})
    }
  }

  const clearFilters = () => {
    setSearchTerm('')
    setSelectedFamily('')
    setSelectedZone('')
    setSearchParams({})
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">植物列表</h1>
          <p className="text-gray-500">共找到 {filteredPlants.length} 种植物</p>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-6 mb-8 border border-gray-100">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                搜索植物
              </label>
              <div className="relative">
                <input
                  type="text"
                  value={searchTerm}
                  onChange={handleSearchChange}
                  placeholder="输入植物名称、科属或描述..."
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors"
                />
                <span className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400">
                  🔍
                </span>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                按科属筛选
              </label>
              <select
                value={selectedFamily}
                onChange={handleFamilyChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors bg-white"
              >
                <option value="">全部科属</option>
                {families.map(family => (
                  <option key={family} value={family}>
                    {family}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                按园区筛选
              </label>
              <select
                value={selectedZone}
                onChange={handleZoneChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors bg-white"
              >
                <option value="">全部园区</option>
                {zones.map(zone => (
                  <option key={zone} value={zone}>
                    {zone}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {(searchTerm || selectedFamily || selectedZone) && (
            <div className="mt-4 flex items-center">
              <span className="text-sm text-gray-500 mr-2">当前筛选：</span>
              <div className="flex flex-wrap gap-2">
                {searchTerm && (
                  <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm">
                    关键词: {searchTerm}
                  </span>
                )}
                {selectedFamily && (
                  <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm">
                    科属: {selectedFamily}
                  </span>
                )}
                {selectedZone && (
                  <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm">
                    园区: {selectedZone}
                  </span>
                )}
                <button
                  onClick={clearFilters}
                  className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm hover:bg-gray-200 transition-colors"
                >
                  清除筛选
                </button>
              </div>
            </div>
          )}
        </div>

        {filteredPlants.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredPlants.map(plant => (
              <PlantCard key={plant.id} plant={plant} />
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">🌱</div>
            <h3 className="text-xl font-semibold text-gray-700 mb-2">
              未找到匹配的植物
            </h3>
            <p className="text-gray-500 mb-4">
              尝试使用其他关键词或筛选条件
            </p>
            <button
              onClick={clearFilters}
              className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              重置筛选条件
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default PlantListPage
