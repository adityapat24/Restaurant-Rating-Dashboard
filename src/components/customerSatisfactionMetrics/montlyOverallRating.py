# components/charts.py
import json
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from data.loadData import loadData
def create_monthly_mean_rating_chart():
    data = loadData()

    # Convert reviews and ratings to DataFrames
    reviews_df = pd.DataFrame(data["reviews"])
    ratings_df = pd.DataFrame(data["ratings"])

    # Merge reviews with ratings
    merged_df = reviews_df.merge(ratings_df, left_on="rating_id", right_on="id", suffixes=("_review", "_rating"))

    # Convert timestamp to datetime and extract month-year
    merged_df["timestamp"] = pd.to_datetime(merged_df["timestamp"], errors="coerce")
    merged_df["month"] = merged_df["timestamp"].dt.to_period("M").astype(str)

    # Compute mean overall rating by month
    monthly_means = merged_df.groupby("month")["overall"].mean().reset_index()

    # Create line chart
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=monthly_means["month"],
            y=monthly_means["overall"],
            mode="lines+markers",
            line=dict(width=3),
            marker=dict(size=8),
            name="Mean Overall Rating"
        )
    )

    fig.update_layout(
        title="📅 Average Overall Rating by Month",
        xaxis_title="Month",
        yaxis_title="Average Rating (1–5)",
        template="plotly_white",
        yaxis=dict(range=[0, 5]),
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig
