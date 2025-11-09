"""Utility functions that build dish summaries from the mockData.json payload.

These functions use `data/loadData.py` to load `src/data/mockData.json` and
aggregate ratings per menu item (join reviews -> ratings -> menuItems).

Returned dish dicts follow the shape expected by the rest of the app:
{
  "id": <menu_item_id>,
  "name": <menu item name>,
  "price": <price if available or None>,
  "ratings": { "taste": <mean>, "texture": <mean mapped from portion>, "bangForBuck": <mean mapped from value> },
  "reviewCount": <int>
}
"""

from typing import List, Dict, Optional
import pandas as pd
from data.loadData import loadData


def _build_aggregated_menu() -> List[Dict]:
    """Return a list of aggregated menu items constructed from mockData.json.

    This function is idempotent and intentionally lightweight — it rebuilds
    the aggregation on each call (data is small). If you prefer, we can add
    simple caching later.
    """
    data = loadData()

    reviews = pd.DataFrame(data.get("reviews", []))
    ratings = pd.DataFrame(data.get("ratings", []))
    menu = pd.DataFrame(data.get("menuItems", []))

    if reviews.empty or ratings.empty or menu.empty:
        # If any piece is missing, fall back to an empty list
        return []

    # Join reviews -> ratings to attribute rating values to menu_item_id
    merged = reviews.merge(ratings, left_on="rating_id", right_on="id", suffixes=("_review", "_rating"))
    merged = merged.merge(menu, left_on="menu_item_id", right_on="id", suffixes=("", "_menu"))

    # For each menu item compute mean taste, portion (map to texture), value (map to bangForBuck), and overall mean
    agg = (
        merged
        .groupby(["menu_item_id", "name"], as_index=False)
        .agg(
            taste_mean=("taste", "mean"),
            portion_mean=("portion", "mean"),
            value_mean=("value", "mean"),
            overall_mean=("overall", "mean"),
            review_count=("rating_id", "count"),
        )
    )

    dishes: List[Dict] = []
    for row in agg.to_dict(orient="records"):
        dishes.append({
            "id": int(row.get("menu_item_id")),
            "name": row.get("name"),
            "price": None,  # price not present in mockData.json menuItems; keep None
            "ratings": {
                "taste": round(float(row.get("taste_mean", 0) or 0), 1),
                "texture": round(float(row.get("portion_mean", 0) or 0), 1),
                "bangForBuck": round(float(row.get("value_mean", 0) or 0), 1),
            },
            "overall": round(float(row.get("overall_mean", 0) or 0), 1),
            "reviewCount": int(row.get("review_count", 0) or 0),
        })

    return dishes


def calculate_average_rating(dish: Dict) -> float:
    """Calculate the average rating for a dish dict.

    If `dish` already has an explicit `overall` field (from aggregation), prefer
    that. Otherwise fall back to averaging taste/texture/bangForBuck.
    """
    if not isinstance(dish, dict):
        return 0.0

    if "overall" in dish and dish.get("overall") is not None:
        try:
            return round(float(dish.get("overall")), 1)
        except Exception:
            pass

    ratings = dish.get("ratings", {})
    taste = float(ratings.get("taste", 0) or 0)
    texture = float(ratings.get("texture", 0) or 0)
    bang = float(ratings.get("bangForBuck", 0) or 0)
    avg = (taste + texture + bang) / 3 if (taste or texture or bang) else 0.0
    return round(avg, 1)


def get_all_dishes() -> List[Dict]:
    """Return the aggregated list of menu items with rating summaries."""
    return _build_aggregated_menu()


def get_top_rated_dishes(count: int = 5) -> List[Dict]:
    """Get the top N rated dishes by average (overall) rating."""
    all_d = get_all_dishes()
    sorted_dishes = sorted(all_d, key=lambda d: calculate_average_rating(d), reverse=True)
    return sorted_dishes[:count]


def get_bottom_rated_dishes(count: int = 5) -> List[Dict]:
    """Get the bottom N rated dishes by average (overall) rating."""
    all_d = get_all_dishes()
    sorted_dishes = sorted(all_d, key=lambda d: calculate_average_rating(d))
    return sorted_dishes[:count]

