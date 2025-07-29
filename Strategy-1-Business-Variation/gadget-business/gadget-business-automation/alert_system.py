"""
Alert System Script
Sends automated alerts for low stock, high returns, or negative reviews.
"""

from typing import Dict, List

def check_and_alert(metrics: Dict[str, float], thresholds: Dict[str, float]) -> List[str]:
    """
    Check business metrics and send alerts if thresholds are crossed.
    Args:
        metrics: Dictionary of business metrics (stock, returns, reviews, etc.).
        thresholds: Dictionary of thresholds for alerts.
    Returns:
        list: List of alert messages.
    """
    alerts = []
    for key, value in metrics.items():
        if key in thresholds and value < thresholds[key]:
            alerts.append(f"ALERT: {key} is below threshold! Current: {value}, Threshold: {thresholds[key]}")
    return alerts

if __name__ == "__main__":
    metrics = {"stock": 5, "returns": 10, "reviews": 3.5}
    thresholds = {"stock": 10, "reviews": 4.0}
    print(check_and_alert(metrics, thresholds)) 