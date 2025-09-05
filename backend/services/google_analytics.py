"""Google Analytics Data API connector."""

from typing import Tuple
import json
import os
import urllib.request
from urllib.error import URLError

API_URL = "https://analyticsdata.googleapis.com/v1beta"


def fetch_orders_and_revenue(start_date: str, end_date: str) -> Tuple[int, float]:
    """Return number of orders and revenue between dates.

    Credentials are read from environment variables:
    GA_PROPERTY_ID and GA_ACCESS_TOKEN.
    """
    property_id = os.getenv("GA_PROPERTY_ID")
    token = os.getenv("GA_ACCESS_TOKEN")
    if not property_id or not token:
        return 0, 0.0

    url = f"{API_URL}/properties/{property_id}:runReport"
    body = {
        "dateRanges": [{"startDate": start_date, "endDate": end_date}],
        "metrics": [{"name": "transactions"}, {"name": "purchaseRevenue"}],
    }
    headers = {"Authorization": f"Bearer {token}"}
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            payload = json.load(resp)
        rows = payload.get("rows", [])
        if rows:
            orders = int(rows[0]["metricValues"][0]["value"])
            revenue = float(rows[0]["metricValues"][1]["value"])
            return orders, revenue
    except URLError:
        pass
    return 0, 0.0
