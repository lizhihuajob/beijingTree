import plantsData from '../data/plants.json'

export const getAllPlants = () => {
  return plantsData.plants || []
}

export const getPlantById = (id) => {
  return plantsData.plants?.find(plant => plant.id === id) || null
}

export const searchPlants = (keyword) => {
  if (!keyword) return getAllPlants()
  
  const lowerKeyword = keyword.toLowerCase()
  return getAllPlants().filter(plant => 
    plant.name_cn.toLowerCase().includes(lowerKeyword) ||
    plant.name_latin.toLowerCase().includes(lowerKeyword) ||
    plant.family.toLowerCase().includes(lowerKeyword) ||
    plant.genus.toLowerCase().includes(lowerKeyword) ||
    plant.description.toLowerCase().includes(lowerKeyword)
  )
}

export const getPlantsByFamily = (family) => {
  return getAllPlants().filter(plant => plant.family === family)
}

export const getPlantsByGardenZone = (zone) => {
  return getAllPlants().filter(plant => 
    plant.garden_zones?.includes(zone)
  )
}

export const getProtectedPlants = () => {
  return getAllPlants().filter(plant => 
    plant.protection_status && plant.protection_status.trim() !== ''
  )
}

export const getAllFamilies = () => {
  const families = new Set()
  getAllPlants().forEach(plant => {
    if (plant.family) {
      families.add(plant.family)
    }
  })
  return Array.from(families).sort()
}

export const getAllGardenZones = () => {
  const zones = new Set()
  getAllPlants().forEach(plant => {
    if (plant.garden_zones) {
      plant.garden_zones.forEach(zone => zones.add(zone))
    }
  })
  return Array.from(zones).sort()
}

export const getStatistics = () => {
  const plants = getAllPlants()
  return {
    total: plants.length,
    families: getAllFamilies().length,
    protected: getProtectedPlants().length,
    zones: getAllGardenZones().length
  }
}

export const formatProtectionStatus = (status) => {
  if (!status) return null
  
  const levelColors = {
    '国家一级保护': 'bg-red-100 text-red-800',
    '国家二级保护': 'bg-orange-100 text-orange-800',
    '国家三级保护': 'bg-yellow-100 text-yellow-800'
  }
  
  return {
    text: status,
    color: levelColors[status] || 'bg-gray-100 text-gray-800'
  }
}
