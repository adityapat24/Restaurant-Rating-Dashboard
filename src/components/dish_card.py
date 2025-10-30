"""
Dish card component
"""

from dash import html
from data.dishes import calculate_average_rating


def create_dish_card(dish, rank=None):
    """
    Create a dish card component
    
    Args:
        dish: Dictionary containing dish data
        rank: Optional rank number to display
    
    Returns:
        Dash HTML component
    """
    avg_rating = calculate_average_rating(dish)
    
    return html.Div(
        className="dish-card",
        children=[
            # Image section with rank badge
            html.Div(
                className="dish-image-container",
                children=[
                    html.Img(
                        src=dish["image"],
                        alt=dish["name"],
                        className="dish-image"
                    ),
                    html.Div(
                        f"#{rank}",
                        className="rank-badge"
                    ) if rank else None
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
                                    html.H3(dish["name"], className="dish-name"),
                                    html.P(f"${dish['price']}", className="dish-price")
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
                                    html.Span(str(dish["ratings"]["taste"]), className="rating-score")
                                ]
                            ),
                            # Texture
                            html.Div(
                                className="rating-row",
                                children=[
                                    html.Span("Texture", className="rating-label"),
                                    html.Span(str(dish["ratings"]["texture"]), className="rating-score")
                                ]
                            ),
                            # Bang for Buck
                            html.Div(
                                className="rating-row",
                                children=[
                                    html.Span("Bang for Buck", className="rating-label"),
                                    html.Span(str(dish["ratings"]["bangForBuck"]), className="rating-score")
                                ]
                            )
                        ]
                    ),
                    
                    # Review count
                    html.P(
                        f"{dish['reviewCount']} reviews",
                        className="review-count"
                    )
                ]
            )
        ]
    )
