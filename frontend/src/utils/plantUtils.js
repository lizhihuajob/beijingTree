import { api } from '../services/api'

export const getAllPlants = async () => {
  try {
    const result = await api.get('/plants', { per_page: 1000 })
    return result.plants || []
  } catch (error) {
    console.error('Failed to fetch plants:', error)
    return []
  }
}

export const getPlantById = async (id) => {
  try {
    return await api.get(`/plants/${id}`)
  } catch (error) {
    console.error('Failed to fetch plant:', error)
    return null
  }
}

export const searchPlants = async (keyword) => {
  try {
    const result = await api.get('/plants', { search: keyword, per_page: 1000 })
    return result.plants || []
  } catch (error) {
    console.error('Failed to search plants:', error)
    return []
  }
}

export const getPlantsByFamily = async (family) => {
  try {
    const result = await api.get('/plants', { family, per_page: 1000 })
    return result.plants || []
  } catch (error) {
    console.error('Failed to fetch plants by family:', error)
    return []
  }
}

export const getPlantsByGardenZone = async (zone) => {
  try {
    const result = await api.get('/plants', { zone, per_page: 1000 })
    return result.plants || []
  } catch (error) {
    console.error('Failed to fetch plants by zone:', error)
    return []
  }
}

export const getProtectedPlants = async () => {
  try {
    const result = await api.get('/protected')
    return result.plants || []
  } catch (error) {
    console.error('Failed to fetch protected plants:', error)
    return []
  }
}

export const getAllFamilies = async () => {
  try {
    const result = await api.get('/families')
    return result.families || []
  } catch (error) {
    console.error('Failed to fetch families:', error)
    return []
  }
}

export const getAllGardenZones = async () => {
  try {
    const result = await api.get('/zones')
    return result.zones || []
  } catch (error) {
    console.error('Failed to fetch zones:', error)
    return []
  }
}

export const getStatistics = async () => {
  try {
    return await api.get('/statistics')
  } catch (error) {
    console.error('Failed to fetch statistics:', error)
    return {
      total: 0,
      families: 0,
      protected: 0,
      zones: 0
    }
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
