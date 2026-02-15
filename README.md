# Crisis Management System - Django Templates

This package contains 4 fully interactive Django templates for your crisis management hackathon project.

## Files Overview

### 1. overwatch_dashboard.html (736 lines)
**Page 1: The "Overwatch" Dashboard - Command Center**

**Key Features:**
- Sticky top vitals bar with 4 key metrics (AQI, ICU Capacity, Food Stockpile, Threat Level)
- Animated threat heatmap with 8 color-coded sectors
- AI ticker feed with explainable alerts
- Morning briefing with natural language summaries
- Real-time data updates every 5 seconds

**Key CSS Classes:**
- `.vitals-bar` - Top sticky metrics bar
- `.vital-metric` - Individual metric card
- `.heatmap-view` - Main map container
- `.zone` - Individual sector zones (zone-green, zone-amber, zone-red)
- `.ticker-feed` - Scrollable news feed
- `.ticker-item` - Individual news items (priority-high, priority-medium, priority-low)

**Key JavaScript Functions:**
- `updateVitals()` - Simulates real-time vital signs updates
- `setMapView(view)` - Switches between map views
- `explainAlert(element)` - Shows/hides AI explanations
- `addTickerItem()` - Adds new ticker items periodically

**Django Integration Points:**
Replace mock data with:
```django
<div class="vital-value">{{ aqi_value }}</div>
<div class="zone-label">SECTOR {{ sector.id }}</div>
<div class="ticker-content">{{ alert.message }}</div>
```

---

### 2. oracle_simulation.html (896 lines)
**Page 2: The "Oracle" Simulation Lab - Prediction Sandbox**

**Key Features:**
- Chaos control sidebar with event type, intensity, panic level, duration sliders
- Collapse curve graph using Chart.js showing demand vs capacity
- AI mitigation toggle to compare scenarios
- Real-time causal analysis insights
- Counterfactual analysis panel

**Key CSS Classes:**
- `.chaos-controls` - Left sidebar with parameter controls
- `.event-btn` - Event type selection buttons
- `.slider` - Range input sliders
- `.result-card` - Chart and stats containers
- `.insights-panel` - AI analysis section
- `.insight-item` - Individual insight cards

**Key JavaScript Functions:**
- `initChart()` - Initializes Chart.js collapse curve
- `selectEvent(button)` - Handles event type selection
- `updateSliderValue(type)` - Updates slider display values
- `toggleMitigation()` - Toggles AI auto-scaling on/off
- `runSimulation()` - Runs simulation with current parameters
- `checkCollapse()` - Checks if demand exceeds capacity

**Django Integration Points:**
```django
<button data-event="{{ event.type }}" onclick="selectEvent(this)">
    {{ event.icon }} {{ event.name }}
</button>
```

**Dependencies:**
- Chart.js CDN (already included): `https://cdn.jsdelivr.net/npm/chart.js`

---

### 3. convoy_logistics.html (795 lines)
**Page 3: The "Convoy" Logistics Grid - Live Operations**

**Key Features:**
- Split-screen map view (traffic blockages vs AI green corridors)
- Real-time asset tracking cards
- Task force pairing visualizations
- Predictive maintenance alerts
- Multi-objective optimization display

**Key CSS Classes:**
- `.top-bar` - Status indicators header
- `.map-panel` - Individual map containers
- `.map-view` - Map canvas area
- `.road` - Road elements (road-horizontal, road-vertical, blocked, green-corridor)
- `.map-icon` - Vehicle/location icons (ambulance, truck, bulldozer, hospital, blockage)
- `.assets-panel` - Asset cards sidebar
- `.asset-card` - Individual asset cards (paired class for task forces)
- `.task-force-indicator` - Task force pairing display

**Key JavaScript Functions:**
- `updateAssetPositions()` - Simulates vehicle movement
- `updateFuelLevels()` - Updates fuel percentages
- `updateOptimization()` - Updates AI optimization metrics

**Django Integration Points:**
```django
{% for asset in assets %}
<div class="asset-card {% if asset.task_force %}paired{% endif %}">
    <div class="asset-type">
        <span class="asset-icon">{{ asset.icon }}</span>
        <span>{{ asset.name }}</span>
    </div>
    <div class="asset-status status-{{ asset.status }}">{{ asset.status|upper }}</div>
</div>
{% endfor %}
```

---

### 4. citizen_shield.html (883 lines)
**Page 4: The "Citizen Shield" Portal - Public Interface**

**Key Features:**
- Animated resilience score gauge (0-100)
- Detailed score breakdown
- Tax receipt pie chart breakdown
- Gamified preparedness quests with rewards
- Personalized risk assessment cards
- Progress tracking system

**Key CSS Classes:**
- `.score-card` - Main resilience score display
- `.score-circle` - Circular gauge animation
- `.score-ring` - Animated conic gradient ring
- `.tax-receipt` - Monthly investment breakdown
- `.allocation-item` - Individual tax allocation items
- `.preparedness-panel` - Quests section
- `.quest-card` - Individual quest cards (completed class when done)
- `.risk-assessment` - Risk cards grid
- `.risk-card` - Individual risk cards (low, medium, high)

**Key JavaScript Functions:**
- Score animation on page load (runs automatically)
- Quest card click handlers for completion
- Progress bar updates

**Django Integration Points:**
```django
<div class="header-title">🛡️ Citizen Shield</div>
<h2>Welcome back, {{ user.get_full_name }}!</h2>
<div class="location-badge">📍 {{ user.sector }}, {{ user.city }}</div>

<div class="score-value">{{ user.resilience_score }}</div>

{% for allocation in tax_allocations %}
<div class="allocation-item">
    <div class="allocation-color" style="background: {{ allocation.color }};"></div>
    <div class="allocation-info">
        <div class="allocation-label">{{ allocation.category }}</div>
        <div class="allocation-desc">{{ allocation.description }}</div>
    </div>
    <div class="allocation-amount">${{ allocation.amount }}</div>
</div>
{% endfor %}

{% for quest in quests %}
<div class="quest-card {% if quest.completed %}completed{% endif %}">
    <div class="quest-icon">{{ quest.icon }}</div>
    <div class="quest-info">
        <h4>{{ quest.title }}</h4>
        <p class="quest-description">{{ quest.description }}</p>
    </div>
</div>
{% endfor %}
```

---

## Installation Instructions

### 1. Create Django App Structure
```bash
# Create a new Django app for each page (or one app with multiple views)
python manage.py startapp dashboard
python manage.py startapp simulation
python manage.py startapp logistics
python manage.py startapp citizen
```

### 2. Place Templates
```
your_project/
├── templates/
│   ├── dashboard/
│   │   └── overwatch_dashboard.html
│   ├── simulation/
│   │   └── oracle_simulation.html
│   ├── logistics/
│   │   └── convoy_logistics.html
│   └── citizen/
│       └── citizen_shield.html
```

### 3. Configure URLs
```python
# urls.py
from django.urls import path
from dashboard import views as dashboard_views
from simulation import views as simulation_views
from logistics import views as logistics_views
from citizen import views as citizen_views

urlpatterns = [
    path('dashboard/', dashboard_views.overwatch, name='overwatch'),
    path('simulation/', simulation_views.oracle, name='oracle'),
    path('logistics/', logistics_views.convoy, name='convoy'),
    path('citizen/', citizen_views.shield, name='citizen_shield'),
]
```

### 4. Create Views
```python
# dashboard/views.py
from django.shortcuts import render

def overwatch(request):
    context = {
        'aqi_value': 42,
        'icu_capacity': 73,
        'food_days': 45,
        'threat_level': 'DEFCON 3',
        'sectors': Sector.objects.all(),
        'alerts': Alert.objects.order_by('-created_at')[:10]
    }
    return render(request, 'dashboard/overwatch_dashboard.html', context)
```

### 5. Remove Mock Data and Connect to Backend
Each template has JavaScript functions that generate mock data. Replace these with:

**Option A: Template Variables (Server-Side Rendering)**
```django
<div class="vital-value">{{ aqi_value }}</div>
```

**Option B: AJAX/Fetch (Client-Side)**
```javascript
fetch('/api/vitals/')
    .then(response => response.json())
    .then(data => {
        document.getElementById('aqi-value').textContent = data.aqi;
    });
```

---

## Customization Guide

### Changing Colors
Each page has CSS custom properties (variables) at the top:

**Overwatch Dashboard:**
```css
:root {
    --primary-bg: #0a0e14;      /* Main background */
    --accent-green: #00ff88;     /* Success color */
    --accent-amber: #ffb800;     /* Warning color */
    --accent-red: #ff3366;       /* Critical color */
}
```

**Oracle Simulation:**
```css
:root {
    --accent-cyan: #00d9ff;      /* Primary accent */
    --accent-purple: #b066ff;    /* Secondary accent */
    --accent-orange: #ff6b35;    /* Alert color */
}
```

### Changing Fonts
Google Fonts are loaded via CDN. To change:
1. Replace the Google Fonts link in `<head>`
2. Update `font-family` in CSS

### Adding New Metrics/Cards
Follow the existing pattern:
```html
<div class="vital-metric">
    <div class="vital-icon">🔥</div>
    <div class="vital-data">
        <div class="vital-label">New Metric</div>
        <div class="vital-value">123</div>
    </div>
    <div class="vital-status status-good">GOOD</div>
</div>
```

---

## Key Features for Judges

### AI-Driven Features (Highlighted)
1. **Explainable AI**: "Why did AI flag this?" tooltips on every alert
2. **Anomaly Detection**: Statistical deviation detection, not just thresholds
3. **Natural Language Summaries**: Morning briefing synthesizes millions of data points
4. **Causal Inference**: AI explains root causes, not just correlations
5. **Counterfactual Analysis**: "What if we had done X?" scenario testing
6. **Multi-Objective Optimization**: Survival probability over speed
7. **Predictive Maintenance**: Flags equipment before failure
8. **Sentiment Analysis**: Scans social media for panic indicators
9. **Personalized Risk**: Hyper-local assessments using tree density, elevation, etc.

### Human-in-the-Loop Design
- All AI suggestions require human approval
- "Approve" buttons on critical actions
- Transparency through explanations
- User feedback mechanisms

### Multimodal Input Ready
- Designed to accept images (satellite photos)
- Text processing (doctor's notes)
- Numerical data (sensor readings)
- Social media feeds

---

## Browser Compatibility
- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support
- Mobile: Responsive design included

---

## Performance Notes
- Animations use CSS where possible (hardware accelerated)
- JavaScript updates are throttled with setInterval
- Charts use Canvas rendering (Chart.js)
- No external dependencies except Chart.js

---

## Team Division (5 People)
As suggested in your document, divide work by page:

1. **Person 1**: Overwatch Dashboard + Django models for sectors/alerts
2. **Person 2**: Oracle Simulation + Chart.js backend integration
3. **Person 3**: Convoy Logistics + Real-time WebSocket connections
4. **Person 4**: Citizen Shield + User authentication/profiles
5. **Person 5**: API layer + Database design + Integration

Each person owns one "app" = cleaner merges!

---

## License
These templates are provided for your hackathon project. Good luck!