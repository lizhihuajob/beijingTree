const API_BASE = '/admin/api';

class AdminApi {
  constructor() {
    this.token = localStorage.getItem('admin_token');
  }

  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('admin_token', token);
    } else {
      localStorage.removeItem('admin_token');
    }
  }

  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    return headers;
  }

  async request(endpoint, options = {}) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers: this.getHeaders(),
      ...options.headers,
    });

    const data = await response.json();

    if (!response.ok) {
      if (response.status === 401) {
        this.setToken(null);
        window.location.href = '/admin/login';
      }
      throw new Error(data.error || 'Request failed');
    }

    return data;
  }

  async login(username, password) {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Login failed');
    }

    this.setToken(data.token);
    return data;
  }

  logout() {
    this.setToken(null);
  }

  async getCurrentUser() {
    return this.request('/auth/me');
  }

  async changePassword(oldPassword, newPassword) {
    return this.request('/auth/change-password', {
      method: 'POST',
      body: JSON.stringify({ old_password: oldPassword, new_password: newPassword }),
    });
  }

  async getPlants(page = 1, perPage = 20, search = '') {
    const params = new URLSearchParams({ page, per_page: perPage, search });
    return this.request(`/plants?${params}`);
  }

  async getPlant(id) {
    return this.request(`/plants/${id}`);
  }

  async createPlant(data) {
    return this.request('/plants', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updatePlant(id, data) {
    return this.request(`/plants/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deletePlant(id) {
    return this.request(`/plants/${id}`, {
      method: 'DELETE',
    });
  }

  async getDashboardStats() {
    return this.request('/dashboard/stats');
  }

  async getVisitTrend(days = 7) {
    return this.request(`/dashboard/visit-trend?days=${days}`);
  }

  async getSpiderConfig() {
    return this.request('/spider/config');
  }

  async updateSpiderConfig(data) {
    return this.request('/spider/config', {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async runSpiderNow() {
    return this.request('/spider/run-now', {
      method: 'POST',
    });
  }

  async getSystemInfo() {
    return this.request('/system/info');
  }
}

export const adminApi = new AdminApi();
