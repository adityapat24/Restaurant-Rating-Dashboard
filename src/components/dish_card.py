"""
Dish card component
"""

from dash import html
import pandas as pd
from data.loadData import loadData


def _get_aggregated_stats_for_name(name: str):
    """Return aggregated (taste, portion, value, overall, review_count) for a menu item name."""
    data = loadData()
    reviews_df = pd.DataFrame(data.get("reviews", []))
    ratings_df = pd.DataFrame(data.get("ratings", []))
    menu_df = pd.DataFrame(data.get("menuItems", []))

    if reviews_df.empty or ratings_df.empty or menu_df.empty:
        return None

    merged = (
        reviews_df
        .merge(ratings_df, left_on="rating_id", right_on="id", suffixes=("_review", "_rating"))
        .merge(menu_df, left_on="menu_item_id", right_on="id", suffixes=("", "_menu"))
    )

    filtered = merged[merged["name"] == name]
    if filtered.empty:
        return None

    taste = filtered["taste"].mean() if "taste" in filtered.columns else 0
    portion = filtered["portion"].mean() if "portion" in filtered.columns else 0
    value = filtered["value"].mean() if "value" in filtered.columns else 0
    overall = filtered["overall"].mean() if "overall" in filtered.columns else 0
    review_count = int(filtered.shape[0])

    return {
        "taste": round(float(taste), 1),
        "portion": round(float(portion), 1),  
        "value": round(float(value), 1),
        "overall": round(float(overall), 1),
        "reviewCount": review_count,
    }


def create_dish_card(dish, rank=None):
    """
    Create a dish card component

    dish: can be either a dict from mockData menuItems/reviews merged rows or the legacy dish dict
    """
    name = dish.get("name") if isinstance(dish, dict) else str(dish)

    agg = _get_aggregated_stats_for_name(name) if name else None

    # prefer values from aggregated data, otherwise fall back to fields on `dish`
    avg_rating = agg["overall"] if agg else dish.get("rating") or dish.get("avg") or 0
    taste = agg["taste"] if agg else (dish.get("ratings", {}).get("taste") if isinstance(dish, dict) else 0)
    portion = agg["portion"] if agg else (dish.get("ratings", {}).get("portion") if isinstance(dish, dict) else 0)
    value = agg["value"] if agg else (dish.get("ratings", {}).get("value") if isinstance(dish, dict) else 0)
    review_count = agg["reviewCount"] if agg else dish.get("reviewCount", 0)
    price = dish.get("price") if isinstance(dish, dict) else None
    image = dish.get("image") if isinstance(dish, dict) else None

    return html.Div(
        className="dish-card",
        children=[
            # Image section with rank badge
            html.Div(
                className="dish-image-container",
                children=[
                    html.Img(src=image, alt=name, className="dish-image") if image else None,
                    html.Div(f"#{rank}", className="rank-badge") if rank else None,
                ]
            ),

            # Card content
            html.Div(
                className="dish-card-content",
                children=[
                    # Header with name, price, and rating
                    html.Div(
                        className="dish-header",
                        children=[
                            html.Div(
                                children=[
                                    html.H3(name, className="dish-name"),
                                    html.P(f"${price}", className="dish-price") if price is not None else None,
                                ]
                            ),
                            html.Div(
                                className="dish-rating",
                                children=[
                                    html.Span("⭐", className="star-icon"),
                                    html.Span(str(avg_rating), className="rating-value")
                                ]
                            )
                        ]
                    ),

                    # Rating details
                    html.Div(
                        className="rating-details",
                        children=[
                            # Taste
                            html.Div(
                                className="rating-row",
                                children=[
                                    html.Span("Taste", className="rating-label"),
                                    html.Span(str(taste), className="rating-score")
                                ]
                            ),
                            # Portion
                            html.Div(
                                className="rating-row",
                                children=[
                                    html.Span("Portion", className="rating-label"),
                                    html.Span(str(portion), className="rating-score")
                                ]
                            ),
                            # Value
                            html.Div(
                                className="rating-row",
                                children=[
                                    html.Span("Value", className="rating-label"),
                                    html.Span(str(value), className="rating-score")
                                ]
                            )
                        ]
                    ),

                    # Review count
                    html.P(f"{review_count} reviews", className="review-count")
                ]
            )
        ]
    )
