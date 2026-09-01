function buildUrl(base, endpoint, params = {}) {
  const isRelative = base.startsWith('/')
  let url
  
  if (isRelative) {
    url = `${base}${endpoint}`
    const queryString = Object.keys(params)
      .filter(key => params[key])
      .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
      .join('&')
    return queryString ? `${url}?${queryString}` : url
  } else {
    url = new URL(`${base}${endpoint}`)
    Object.keys(params).forEach(key => {
      if (params[key]) {
        url.searchParams.append(key, params[key])
      }
    })
    return url.toString()
  }
}

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

export const api = {
  async get(endpoint, params = {}) {
    const url = buildUrl(API_BASE_URL, endpoint, params)
    
    try {
      const response = await fetch(url)
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
    const url = buildUrl(API_BASE_URL, endpoint)
    
    try {
      const response = await fetch(url, {
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
    const url = buildUrl(API_BASE_URL, endpoint)
    
    try {
      const response = await fetch(url, {
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
    const url = buildUrl(API_BASE_URL, endpoint)
    
    try {
      const response = await fetch(url, {
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
