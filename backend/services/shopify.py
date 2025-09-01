"""Shopify API connector."""

from typing import Tuple
import json
import os
import urllib.parse
import urllib.request
from urllib.error import URLError


def fetch_orders_and_revenue(start_date: str, end_date: str) -> Tuple[int, float]:
    """Return number of orders and revenue from Shopify."""
    shop_url = os.getenv("SHOPIFY_SHOP_URL")
    token = os.getenv("SHOPIFY_ACCESS_TOKEN")
    if not shop_url or not token:
        return 0, 0.0

    params = {
        "status": "any",
        "created_at_min": start_date,
        "created_at_max": end_date,
        "fields": "total_price",
    }
    query = urllib.parse.urlencode(params)
    url = f"https://{shop_url}/admin/api/2023-07/orders.json?{query}"
    headers = {"X-Shopify-Access-Token": token}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.load(resp)
        orders = data.get("orders", [])
        revenue = sum(float(o.get("total_price", 0)) for o in orders)
        return len(orders), revenue
    except URLError:
        pass
    return 0, 0.0
