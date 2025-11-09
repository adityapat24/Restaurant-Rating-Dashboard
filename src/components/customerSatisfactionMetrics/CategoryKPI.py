import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta


from data.loadData import loadData


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
    
    # Period labels for title
    period_labels = {
        "overall": "All Time",
        "month": "This Month",
        "week": "This Week"
    }
    
    # Create subplots for 3 cards
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("Taste", "Portion", "Value"),
        specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]],
        horizontal_spacing=0.1
    )
    
    # Taste Card
    fig.add_trace(
        go.Indicator(
            mode="number+gauge",
            value=taste_avg,
            number={"valueformat": ".1f", "font": {"size": 70, "color": "#FF5722"}},
            gauge={
                "axis": {"range": [0, 5], "tickwidth": 1},
                "bar": {"color": "#FF5722"},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "#E0E0E0"
            }
        ),
        row=1, col=1
    )
    
    # Portion Card
    fig.add_trace(
        go.Indicator(
            mode="number+gauge",
            value=portion_avg,
            number={"valueformat": ".1f", "font": {"size": 70, "color": "#2196F3"}},
            gauge={
                "axis": {"range": [0, 5], "tickwidth": 1},
                "bar": {"color": "#2196F3"},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "#E0E0E0"
            }
        ),
        row=1, col=2
    )
    
    # Value Card
    fig.add_trace(
        go.Indicator(
            mode="number+gauge",
            value=value_avg,
            number={"valueformat": ".1f", "font": {"size": 70, "color": "#4CAF50"}},
            gauge={
                "axis": {"range": [0, 5], "tickwidth": 1},
                "bar": {"color": "#4CAF50"},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "#E0E0E0"
            }
        ),
        row=1, col=3
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
