from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter

from utils.risk import evaluate_risk


router = APIRouter(tags=["frontend-data"])


@router.get("/dashboard-data")
def get_dashboard_data() -> dict[str, object]:
    crowd_data = [
        {"time": "00:00", "crowd": 2400, "prediction": 2210},
        {"time": "04:00", "crowd": 1398, "prediction": 2290},
        {"time": "08:00", "crowd": 9800, "prediction": 2000},
        {"time": "12:00", "crowd": 3908, "prediction": 2108},
        {"time": "16:00", "crowd": 4800, "prediction": 2200},
        {"time": "20:00", "crowd": 3800, "prediction": 2100},
        {"time": "23:59", "crowd": 4300, "prediction": 2300},
    ]

    temple_metrics = [
        {"name": "Somnath", "value": 35, "color": "#EA6E3C"},
        {"name": "Dwarkadhish", "value": 28, "color": "#4C3A7F"},
        {"name": "Ramnath", "value": 22, "color": "#10B981"},
        {"name": "Shreenathji", "value": 15, "color": "#F59E0B"},
    ]

    current = crowd_data[-1]["crowd"]
    previous = crowd_data[-2]["crowd"]
    predicted = crowd_data[-1]["prediction"]
    risk_score, risk_level = evaluate_risk(current=current, predicted=predicted, previous=previous)

    return {
        "summary": {
            "current_crowd": current,
            "risk_level": risk_level,
            "risk_score": round(risk_score, 2),
            "next_hour_surge_percent": round(max(0.0, ((predicted - current) / max(current, 1)) * 100), 2),
            "response_time_seconds": 0.24,
            "last_updated": datetime.now(timezone.utc).isoformat(),
        },
        "crowd_data": crowd_data,
        "temple_metrics": temple_metrics,
    }


@router.get("/analytics-data")
def get_analytics_data() -> dict[str, object]:
    historical_data = [
        {"month": "Jan", "actual": 2400, "predicted": 2210, "accuracy": 92},
        {"month": "Feb", "actual": 3210, "predicted": 2990, "accuracy": 94},
        {"month": "Mar", "actual": 2290, "predicted": 2000, "accuracy": 88},
        {"month": "Apr", "actual": 2390, "predicted": 2108, "accuracy": 96},
        {"month": "May", "actual": 2490, "predicted": 2200, "accuracy": 95},
        {"month": "Jun", "actual": 2590, "predicted": 2100, "accuracy": 97},
    ]

    festival_data = [
        {"festival": "Diwali", "2022": 4500, "2023": 5200, "2024": 5800},
        {"festival": "Navratri", "2022": 3800, "2023": 4200, "2024": 4900},
        {"festival": "Holi", "2022": 3200, "2023": 3600, "2024": 4100},
        {"festival": "Janmashtami", "2022": 2800, "2023": 3100, "2024": 3500},
    ]

    accuracy_metrics = [
        {
            "metric": "MAE (Mean Absolute Error)",
            "value": "+/-245 people",
            "description": "Average prediction variance",
        },
        {
            "metric": "RMSE (Root Mean Squared Error)",
            "value": "312",
            "description": "Standard deviation of errors",
        },
        {
            "metric": "Model Accuracy",
            "value": "99.2%",
            "description": "Overall prediction success rate",
        },
        {
            "metric": "Peak Hour Accuracy",
            "value": "97.8%",
            "description": "Accuracy during high traffic",
        },
    ]

    return {
        "historical_data": historical_data,
        "festival_data": festival_data,
        "accuracy_metrics": accuracy_metrics,
    }


@router.get("/alerts-data")
def get_alerts_data() -> dict[str, object]:
    alerts = [
        {
            "id": 1,
            "temple": "Somnath Temple",
            "severity": "Critical",
            "type": "Crowd Surge",
            "message": "Predicted surge of 35% in next 2 hours. Current capacity at 85%.",
            "timestamp": "2024-02-26 14:32:15",
            "escalation": "Level 3",
            "response": "Medical team mobilized. Barrier reinforcement initiated.",
            "status": "Active",
        },
        {
            "id": 2,
            "temple": "Dwarkadhish Temple",
            "severity": "Warning",
            "type": "Capacity Alert",
            "message": "Approaching maximum capacity. 68% of current limit reached.",
            "timestamp": "2024-02-26 14:28:43",
            "escalation": "Level 2",
            "response": "Additional staff deployed to entrance.",
            "status": "Active",
        },
        {
            "id": 3,
            "temple": "Ramnath Temple",
            "severity": "Safe",
            "type": "Routine Monitor",
            "message": "Crowd density within normal parameters. All systems nominal.",
            "timestamp": "2024-02-26 14:25:20",
            "escalation": "Level 1",
            "response": "Standard monitoring continues.",
            "status": "Monitoring",
        },
    ]

    return {
        "critical_count": sum(1 for a in alerts if a["severity"] == "Critical"),
        "warning_count": sum(1 for a in alerts if a["severity"] == "Warning"),
        "safe_count": sum(1 for a in alerts if a["severity"] == "Safe"),
        "alerts": alerts,
    }
