# Smart Crowd Management Backend (FastAPI)

Production-ready backend for crowd counting, future prediction, and risk evaluation.

## Frontend Contract Analysis

The current frontend pages use static mock data (no live API calls yet). The following data shapes were identified for backend integration:

- Dashboard chart points: `{ time, crowd, prediction }`
- Dashboard pie data: `{ name, value, color }`
- Alerts list: `{ id, temple, severity, type, message, timestamp, escalation, response, status }`
- Analytics historical points: `{ month, actual, predicted, accuracy }`
- Festival comparison points: `{ festival, 2022, 2023, 2024 }`

## Folder Structure

backend/
- main.py
- requirements.txt
- README.md
- models/
  - csrnet_model.pth
  - lstm_model.pth
  - lstm_scaler.json (optional)
- routes/
  - inference.py
- utils/
  - model_defs.py
  - model_registry.py
  - preprocessing.py
  - risk.py
  - schemas.py
  - settings.py

## APIs

### 1) POST /predict-count
Input: multipart form-data with `image` file

Response:
```json
{
  "predicted_count": 24532.18
}
```

### 2) POST /predict-future
Input:
```json
{
  "past_counts": [1200, 1300, 1280, 1400, 1510, 1600]
}
```

Response:
```json
{
  "predicted_next_count": 1694.42
}
```

### 3) POST /risk
Input:
```json
{
  "current_count": 24500,
  "predicted_count": 26000,
  "previous_count": 23000
}
```

Response:
```json
{
  "risk_score": 24250,
  "level": "Critical"
}
```

Risk formula used:
      "value": "+/-245 people",
`risk = 0.4*current + 0.3*(current - previous) + 0.3*predicted`

### 4) GET /health
Model/device health endpoint for ops monitoring.

### 5) GET /dashboard-data
Frontend-ready payload for dashboard cards + charts.

### 6) GET /analytics-data
Frontend-ready payload for analytics charts + metric cards.

### 7) GET /alerts-data
Frontend-ready payload for alerts center list + counters.

## Frontend Integration Examples

### fetch (predict count)
```ts
const form = new FormData();
form.append('image', fileInput.files[0]);

const countRes = await fetch('http://127.0.0.1:8000/predict-count', {
  method: 'POST',
  body: form,
});
const countData = await countRes.json();
// countData.predicted_count
```

### fetch (predict future)
```ts
const futureRes = await fetch('http://127.0.0.1:8000/predict-future', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ past_counts: [1200, 1300, 1400, 1500, 1600, 1700] }),
});
const futureData = await futureRes.json();
// futureData.predicted_next_count
```

### fetch (risk)
```ts
const riskRes = await fetch('http://127.0.0.1:8000/risk', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    current_count: 24500,
    predicted_count: 26000,
    previous_count: 23000,
  }),
});
const riskData = await riskRes.json();
// riskData.risk_score, riskData.level
```

### fetch (dashboard page data)
```ts
const dashboardRes = await fetch('http://127.0.0.1:8000/dashboard-data');
const dashboardData = await dashboardRes.json();
// dashboardData.summary
// dashboardData.crowd_data (time, crowd, prediction)
// dashboardData.temple_metrics (name, value, color)
```

### fetch (alerts page data)
```ts
const alertsRes = await fetch('http://127.0.0.1:8000/alerts-data');
const alertsData = await alertsRes.json();
// alertsData.alerts
// alertsData.critical_count / warning_count / safe_count
```

## Run Locally

1. Open terminal in `backend/`
2. Create virtual environment and install dependencies

Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Place model files in `backend/models/`

- `csrnet_model.pth`
- `lstm_model.pth`
- Optional `lstm_scaler.json` if your training used min-max or z-score normalization.

4. Start API server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

5. Open API docs
- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Notes on Inference

- Models are loaded once during application startup and reused per request.
- GPU is used automatically when CUDA is available.
- If model files are missing or invalid, startup fails with a clear error.
- All responses are JSON.
- CORS is enabled to allow frontend integration.
