/**
 * Civilization Shield - API Service
 * Connects Frontend to Django Backend
 */

const API = {
  // Django backend URL
  baseURL: 'http://localhost:8000/api/v1',
  
  // Generic request handler
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    };

    try {
      console.log(`API Request: ${url}`);
      const response = await fetch(url, config);
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || data.error || `HTTP ${response.status}`);
      }
      
      return data;
    } catch (error) {
      console.error(`API Error [${endpoint}]:`, error);
      throw error;
    }
  },

  // ==================== DASHBOARD API ====================
  dashboard: {
    async getStats(state = 'TX') {
      return API.request(`/dashboard/stats/?state=${state}`);
    },

    async getWeatherAlerts(state = 'TX') {
      return API.request(`/dashboard/weather/alerts/?state=${state}`);
    },

    async getWeatherForecast(lat = 30.2672, lon = -97.7431) {
      return API.request(`/dashboard/weather/forecast/?lat=${lat}&lon=${lon}`);
    },

    async getDisasters(state = null, days = 30) {
      let url = `/dashboard/disasters/?days=${days}`;
      if (state) url += `&state=${state}`;
      return API.request(url);
    },

    async getAlerts() {
      return API.request('/dashboard/alerts/');
    },

    async getIncidents(status = null) {
      let url = '/dashboard/incidents/';
      if (status) url += `?status=${status}`;
      return API.request(url);
    },

    async createIncident(data) {
      return API.request('/dashboard/incidents/', {
        method: 'POST',
        body: JSON.stringify(data)
      });
    }
  },

  // ==================== LOGISTICS API ====================
  logistics: {
    async getVehicles(status = null, type = null) {
      let url = '/logistics/vehicles/';
      const params = new URLSearchParams();
      if (status) params.append('status', status);
      if (type) params.append('type', type);
      if (params.toString()) url += `?${params}`;
      return API.request(url);
    },

    async getVehicle(vehicleId) {
      return API.request(`/logistics/vehicles/${vehicleId}/`);
    },

    async createVehicle(data) {
      return API.request('/logistics/vehicles/', {
        method: 'POST',
        body: JSON.stringify(data)
      });
    },

    async updateVehicle(vehicleId, data) {
      return API.request(`/logistics/vehicles/${vehicleId}/`, {
        method: 'PUT',
        body: JSON.stringify(data)
      });
    },

    async updateVehiclePosition(vehicleId, lat, lon) {
      return API.request(`/logistics/vehicles/${vehicleId}/position/`, {
        method: 'PUT',
        body: JSON.stringify({ lat, lon })
      });
    },

    async dispatchVehicle(vehicleId, destination) {
      return API.request(`/logistics/vehicles/${vehicleId}/dispatch/`, {
        method: 'POST',
        body: JSON.stringify({ destination })
      });
    }
  },

  // ==================== INVENTORY API ====================
  inventory: {
    async getItems(category = null) {
      let url = '/inventory/items/';
      if (category) url += `?category=${category}`;
      return API.request(url);
    },

    async getItem(id) {
      return API.request(`/inventory/items/${id}/`);
    },

    async updateItem(id, data) {
      return API.request(`/inventory/items/${id}/`, {
        method: 'PATCH',
        body: JSON.stringify(data)
      });
    },

    async calculateSupplies(people, days = 7, state = null) {
      const body = { people, days };
      if (state) body.state = state;
      return API.request('/inventory/calculate/', {
        method: 'POST',
        body: JSON.stringify(body)
      });
    },

    async getResourceNeeds(state = 'TX', days = 7) {
      return API.request(`/inventory/resource-needs/?state=${state}&days=${days}`);
    },

    async getWarehouses() {
      return API.request('/inventory/warehouses/');
    }
  },

  // ==================== CITIZEN API ====================
  citizen: {
    async getSafetyStatus(state = 'TX') {
      return API.request(`/citizen/safety-status/?state=${state}`);
    },

    async getAlerts(state = 'TX') {
      return API.request(`/citizen/alerts/?state=${state}`);
    },

    async getEmergencyContacts() {
      return API.request('/citizen/emergency-contacts/');
    },

    async getShelters(state = 'TX', openOnly = false) {
      let url = `/citizen/shelters/?state=${state}`;
      if (openOnly) url += '&open=true';
      return API.request(url);
    },

    async getFEMAShelters(state = 'TX') {
      return API.request(`/citizen/shelters/fema/?state=${state}`);
    },

    async getAllShelters(state = 'TX') {
      return API.request(`/citizen/shelters/all/?state=${state}`);
    }
  },

  // ==================== ANALYTICS API ====================
  analytics: {
    async getOverview() {
      return API.request('/analytics/');
    },

    async forecastDisasters(state = 'TX', months = 6) {
      return API.request(`/analytics/forecast/disasters/?state=${state}&months=${months}`);
    },

    async getRiskScore(state = 'TX') {
      return API.request(`/analytics/risk/area/?state=${state}`);
    },

    async recommendShelter(lat, lon, state = 'TX', options = {}) {
      const params = new URLSearchParams({ lat, lon, state });
      if (options.needsAda) params.append('needs_ada', 'true');
      if (options.hasPets) params.append('has_pets', 'true');
      return API.request(`/analytics/recommend/shelter/?${params}`);
    },

    async detectAnomaly(resource, currentRate, historicalAvg, historicalStd) {
      return API.request('/analytics/anomaly/consumption/', {
        method: 'POST',
        body: JSON.stringify({
          resource,
          current_rate: currentRate,
          historical_avg: historicalAvg,
          historical_std: historicalStd
        })
      });
    }
  }
};

// ==================== UI HELPERS ====================
const UI = {
  showNotification(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `notification-toast notification-${type}`;
    toast.innerHTML = `
      <span class="notification-message">${message}</span>
      <button class="notification-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    if (!document.getElementById('notification-styles')) {
      const styles = document.createElement('style');
      styles.id = 'notification-styles';
      styles.textContent = `
        .notification-toast {
          position: fixed;
          top: 70px;
          right: 20px;
          padding: 1rem 1.5rem;
          border-radius: 8px;
          background: rgba(15, 28, 50, 0.95);
          border: 1px solid rgba(255,255,255,0.1);
          color: #E8F0F8;
          font-size: 0.875rem;
          display: flex;
          align-items: center;
          gap: 1rem;
          z-index: 9999;
          animation: slideIn 0.3s ease;
          box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        .notification-info { border-left: 4px solid #00AAFF; }
        .notification-success { border-left: 4px solid #00D68F; }
        .notification-warning { border-left: 4px solid #FFAA00; }
        .notification-error { border-left: 4px solid #FF4D4D; }
        .notification-close { background: none; border: none; color: #8AA0B8; font-size: 1.25rem; cursor: pointer; }
        @keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
      `;
      document.head.appendChild(styles);
    }
    
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 5000);
  },

  formatTime(timestamp) {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });
  },

  formatDate(timestamp) {
    return new Date(timestamp).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  }
};

// ==================== TEST FUNCTION ====================
async function testAPI() {
  console.log('🧪 Testing API Connection...\n');
  
  const tests = [
    { name: 'Health Check', fn: () => fetch(`${API.baseURL}/health/`).then(r => r.json()) },
    { name: 'Dashboard Stats', fn: () => API.dashboard.getStats() },
    { name: 'Weather Alerts', fn: () => API.dashboard.getWeatherAlerts() },
    { name: 'Vehicles', fn: () => API.logistics.getVehicles() },
    { name: 'Inventory', fn: () => API.inventory.getItems() },
    { name: 'Shelters', fn: () => API.citizen.getShelters() },
    { name: 'Risk Score', fn: () => API.analytics.getRiskScore() },
  ];
  
  for (const test of tests) {
    try {
      const result = await test.fn();
      console.log(`✅ ${test.name}:`, result.success !== false ? 'OK' : 'FAILED');
    } catch (e) {
      console.log(`❌ ${test.name}: ${e.message}`);
    }
  }
  
  console.log('\n🧪 Test complete!');
}

// Export
window.API = API;
window.UI = UI;
window.testAPI = testAPI;

console.log('✅ API loaded. Backend:', API.baseURL);
console.log('💡 Run testAPI() in console to test connection');
