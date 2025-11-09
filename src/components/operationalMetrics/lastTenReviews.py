# components/lastTenReviews.py

import pandas as pd
import plotly.graph_objects as go
from data.loadData import loadData


def create_last_ten_reviews_table():
    data = loadData()

    # Convert reviews and ratings to DataFrames
    reviews_df = pd.DataFrame(data["reviews"])
    ratings_df = pd.DataFrame(data["ratings"])
    menu_items_df = pd.DataFrame(data["menuItems"])

    # Merge reviews with ratings
    merged_df = reviews_df.merge(
        ratings_df,
        left_on="rating_id",
        right_on="id",
        suffixes=("_review", "_rating")
    )

    merged_df = merged_df.merge(
        menu_items_df,
        left_on="menu_item_id",
        right_on="id",
        suffixes=("", "_menu")
    )

    # Sort by timestamp (most recent first)
    merged_df["timestamp"] = pd.to_datetime(merged_df["timestamp"], errors="coerce")
    merged_df = merged_df.sort_values(by="timestamp", ascending=False)
    print(merged_df.columns)

    # Select the last 10 reviews
    last_ten = merged_df.head(10)[
        ["name", "portion", "taste", "value", "overall", "timestamp"]
    ]

    # Format timestamp for readability
    last_ten["timestamp"] = last_ten["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")

    # Create table
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=[
                        "🍽️ Menu Item",
                        "🍕 Portion",
                        "😋 Taste",
                        "💰 Value",
                        "⭐ Overall",
                        "⏰ Timestamp"
                    ],
                    fill_color="#1f77b4",
                    font=dict(color="white", size=14),
                    align="center",
                ),
                cells=dict(
                    values=[
                        last_ten["name"],
                        last_ten["portion"],
                        last_ten["taste"],
                        last_ten["value"],
                        last_ten["overall"],
                        last_ten["timestamp"],
                    ],
                    fill_color=[["#f9f9f9", "#ffffff"] * 5],
                    align="center",
                    font=dict(size=13),
                    height=30,
                ),
            )
        ]
    )

    fig.update_layout(
        title="📝 Last 10 Customer Reviews",
        template="plotly_white",
        margin=dict(l=20, r=20, t=60, b=20),
    )

    return fig
