
import pandas as pd
import plotly.graph_objects as go
from data.loadData import loadData


def create_monthly_category_ratings_chart():
    data = loadData()

    # Convert reviews and ratings to DataFrames
    reviews_df = pd.DataFrame(data["reviews"])
    ratings_df = pd.DataFrame(data["ratings"])

    # Merge reviews with ratings
    merged_df = reviews_df.merge(
        ratings_df,
        left_on="rating_id",
        right_on="id",
        suffixes=("_review", "_rating")
    )

    # Convert timestamp to datetime and extract month-year
    merged_df["timestamp"] = pd.to_datetime(merged_df["timestamp"], errors="coerce")
    merged_df["month"] = merged_df["timestamp"].dt.to_period("M").astype(str)

    # Compute mean ratings by month for each category
    monthly_means = merged_df.groupby("month")[["portion", "taste", "value"]].mean().reset_index()

    # Create line chart with 3 lines
    fig = go.Figure()

    for category, color in zip(["portion", "taste", "value"], ["#1f77b4", "#ff7f0e", "#2ca02c"]):
        fig.add_trace(
            go.Scatter(
                x=monthly_means["month"],
                y=monthly_means[category],
                mode="lines+markers",
                line=dict(width=3, color=color),
                marker=dict(size=8),
                name=f"Average {category.capitalize()} Rating"
            )
        )

    fig.update_layout(
        title="📅 Average Portion, Taste, and Value Ratings by Month",
        xaxis_title="Month",
        yaxis_title="Average Rating (1–5)",
        template="plotly_white",
        yaxis=dict(range=[0, 5]),
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(title="Category", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig
