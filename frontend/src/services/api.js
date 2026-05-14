const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

export const api = {
  async get(endpoint, params = {}) {
    const url = new URL(`${API_BASE_URL}${endpoint}`)
    Object.keys(params).forEach(key => {
      if (params[key]) {
        url.searchParams.append(key, params[key])
      }
    })
    
    try {
      const response = await fetch(url.toString())
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  },
  
  async post(endpoint, data = {}) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      })
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  },
  
  async put(endpoint, data = {}) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      })
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  },
  
  async delete(endpoint) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'DELETE'
      })
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }
}
