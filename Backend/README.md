# Civilization Shield - Django Backend

## 📁 Project Structure

```
Backend/
├── manage.py                 # Django CLI
├── requirements.txt          # Dependencies
├── .env.example             # Environment template
│
├── civilshield/             # Project config
│   ├── settings.py          # Settings
│   ├── urls.py              # Root URLs
│   └── wsgi.py              # WSGI entry
│
├── apps/                    # Django apps
│   ├── dashboard/           # Crisis dashboard
│   │   ├── models.py        # Alert, Incident
│   │   ├── views.py         # Stats, Weather, Disasters
│   │   └── urls.py
│   │
│   ├── logistics/           # Vehicle tracking
│   │   ├── models.py        # Vehicle
│   │   ├── views.py         # CRUD + dispatch
│   │   └── urls.py
│   │
│   ├── inventory/           # Supply management
│   │   ├── models.py        # InventoryItem, Warehouse
│   │   ├── views.py         # CRUD + calculations
│   │   └── urls.py
│   │
│   ├── citizen/             # Public portal
│   │   ├── models.py        # Shelter
│   │   ├── views.py         # Safety, Alerts, Shelters
│   │   └── urls.py
│   │
│   └── analytics/           # ML & Forecasting
│       ├── views.py         # Forecast, Risk, Recommend
│       └── urls.py
│
├── services/                # External APIs
│   ├── nws.py               # Weather (api.weather.gov)
│   ├── fema.py              # Disasters (fema.gov)
│   └── census.py            # Population (census.gov)
│
├── static/                  # Static files
└── templates/               # HTML templates
```

## 🚀 Quick Start

```bash
# 1. Setup virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup database
python manage.py migrate

# 4. Load demo data
python manage.py load_demo_data

# 5. Run server
python manage.py runserver 8000
```

**Server:** http://localhost:8000  
**Admin:** http://localhost:8000/admin/ (admin/admin123)  
**API:** http://localhost:8000/api/v1/

## 📡 API Endpoints

### Dashboard
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/dashboard/stats/` | Crisis statistics |
| GET | `/api/v1/dashboard/weather/alerts/` | NWS alerts |
| GET | `/api/v1/dashboard/weather/forecast/` | Weather forecast |
| GET | `/api/v1/dashboard/disasters/` | FEMA disasters |
| GET | `/api/v1/dashboard/incidents/` | Local incidents |

### Logistics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/logistics/vehicles/` | List vehicles |
| POST | `/api/v1/logistics/vehicles/` | Create vehicle |
| GET | `/api/v1/logistics/vehicles/{id}/` | Get vehicle |
| PUT | `/api/v1/logistics/vehicles/{id}/position/` | Update position |
| POST | `/api/v1/logistics/vehicles/{id}/dispatch/` | Dispatch |

### Inventory
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/inventory/items/` | List inventory |
| POST | `/api/v1/inventory/calculate/` | Calculate needs |
| GET | `/api/v1/inventory/resource-needs/` | By state population |
| GET | `/api/v1/inventory/warehouses/` | List warehouses |

### Citizen
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/citizen/safety-status/` | Safety level |
| GET | `/api/v1/citizen/alerts/` | Citizen alerts |
| GET | `/api/v1/citizen/emergency-contacts/` | Emergency numbers |
| GET | `/api/v1/citizen/shelters/` | Local shelters |
| GET | `/api/v1/citizen/shelters/fema/` | FEMA shelters |

### Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/analytics/forecast/disasters/` | Disaster prediction |
| GET | `/api/v1/analytics/risk/area/` | Risk scoring |
| GET | `/api/v1/analytics/recommend/shelter/` | Shelter recommendations |
| POST | `/api/v1/analytics/anomaly/consumption/` | Anomaly detection |

## 🔗 Frontend Integration

Update `Frontend/api.js`:
```javascript
const API = {
  baseURL: 'http://localhost:8000/api/v1',
  // ...
};
```

## 📊 Data Sources

| Source | URL | Auth | Data |
|--------|-----|------|------|
| NWS | api.weather.gov | None | Weather, Alerts |
| FEMA | fema.gov/api/open | None | Disasters, Shelters |
| Census | api.census.gov | Optional | Population |
| SQLite | Local | N/A | Vehicles, Inventory |

## 🎯 Demo Tips

1. **Show Django Admin** - Edit data live
2. **Show Browsable API** - Interactive testing
3. **Show real NWS alerts** - Live weather data
4. **Show FEMA disasters** - Recent declarations
5. **Run analytics** - Forecasting, risk scores

## 🔄 Reset Data

```bash
rm db.sqlite3
python manage.py migrate
python manage.py load_demo_data
```
