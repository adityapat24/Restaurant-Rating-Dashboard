import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta


from data.loadData import loadData


def get_color_by_rating(value):
    """
    Determine color based on rating value.

    Args:
        value: Rating value (1-5)

    Returns:
        Color string (red, yellow, or green)
    """
    if value < 3:
        return "#FF0000"  # Red for 1-2.9
    elif value <= 4:
        return "#FFD700"  # Yellow for 3-4
    else:
        return "#00AA00"  # Green for 4.1-5


def filter_data_by_period(reviews_df, ratings_df, period="overall"):
    """
    Filter data based on selected time period.
    
    Args:
        reviews_df: Reviews DataFrame
        ratings_df: Ratings DataFrame
        period: "overall", "month", or "week"
    
    Returns:
        Filtered ratings DataFrame
    """
    if period == "overall":
        merged = reviews_df.merge(ratings_df, left_on="rating_id", right_on="id")
        return merged 
    
    # Convert timestamps
    reviews_df["date"] = pd.to_datetime(reviews_df["timestamp"], errors="coerce")

    today = datetime.now()

    if period == "month":
        start_date = today - timedelta(days=30)
    elif period == "week":
        start_date = today - timedelta(days=7)
    
    filtered_reviews = reviews_df[reviews_df['date'] >= start_date]

    # Merge with ratings
    merged = filtered_reviews.merge(ratings_df, left_on="rating_id", right_on="id")
    return merged

    
def create_category_kpi_cards(period="overall"):
    """
    Create KPI cards showing average ratings for selected time period.
    
    Args:
        period: "overall", "month", or "week"
    """
    data = loadData()
    reviews_df = pd.DataFrame(data["reviews"])
    ratings_df = pd.DataFrame(data["ratings"])
    
    # Filter data based on period
    filtered_data = filter_data_by_period(reviews_df, ratings_df, period)
    
    # Calculate averages from filtered data
    taste_avg = filtered_data["taste"].mean()
    portion_avg = filtered_data["portion"].mean()
    value_avg = filtered_data["value"].mean()
    overall_avg = filtered_data["overall"].mean()
    
    # Period labels for title
    period_labels = {
        "overall": "All Time",
        "month": "This Month",
        "week": "This Week"
    }
    
    # Create subplots for 3 cards
    fig = make_subplots(
        rows=1, cols=4,
        subplot_titles=("Taste", "Portion", "Value", "Overall Rating"),
        specs=[[{"type": "indicator"}, {"type": "indicator"}, 
                {"type": "indicator"}, {"type": "indicator"}]],
        horizontal_spacing=0.05
    )
    
    # Taste Card
    taste_color = get_color_by_rating(taste_avg)
    fig.add_trace(
        go.Indicator(
            mode="number+gauge",
            value=taste_avg,
            number={"valueformat": ".1f", "font": {"size": 50, "color": taste_color}},
            gauge={
                "axis": {"range": [0, 5], "tickwidth": 1},
                "bar": {"color": taste_color},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "#E0E0E0"
            }
        ),
        row=1, col=1
    )
    
    # Portion Card
    portion_color = get_color_by_rating(portion_avg)
    fig.add_trace(
        go.Indicator(
            mode="number+gauge",
            value=portion_avg,
            number={"valueformat": ".1f", "font": {"size": 50, "color": portion_color}},
            gauge={
                "axis": {"range": [0, 5], "tickwidth": 1},
                "bar": {"color": portion_color},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "#E0E0E0"
            }
        ),
        row=1, col=2
    )
    
    # Value Card
    value_color = get_color_by_rating(value_avg)
    fig.add_trace(
        go.Indicator(
            mode="number+gauge",
            value=value_avg,
            number={"valueformat": ".1f", "font": {"size": 50, "color": value_color}},
            gauge={
                "axis": {"range": [0, 5], "tickwidth": 1},
                "bar": {"color": value_color},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "#E0E0E0"
            }
        ),
        row=1, col=3
    )

    overall_color = get_color_by_rating(overall_avg)
    fig.add_trace(
        go.Indicator(
            mode="number+gauge",
            value=overall_avg,
            number={"valueformat": ".1f", "font": {"size": 50, "color": overall_color}},
            gauge={
                "axis": {"range": [0,5], "tickwidth": 1},
                "bar": {"color": overall_color},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor":  "#E0E0E0"
            }
        ),
        row=1, col=4
    )
    
    # Update layout with period in title
    fig.update_layout(
        title=f"Satisfaction Metrics - {period_labels[period]}",
        height=400,
        paper_bgcolor="white",
        font={"family": "Arial, sans-serif"},
        margin=dict(t=100, b=50, l=50, r=50)
    )
    
    return fig
