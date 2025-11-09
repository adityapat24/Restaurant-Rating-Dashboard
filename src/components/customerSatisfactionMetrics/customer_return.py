
import pandas as pd
import plotly.graph_objects as go
from data.loadData import loadData


def create_customer_return_chart():
    data = loadData()

    # Convert reviews and ratings to DataFrames
    reviews_df = pd.DataFrame(data["reviews"])
    ratings_df = pd.DataFrame(data["ratings"])

    # Merge to get return info
    merged_df = reviews_df.merge(
        ratings_df,
        left_on="rating_id",
        right_on="id",
        suffixes=("_review", "_rating")
    )

    # Count returning vs non-returning customers
    return_counts = merged_df["return"].value_counts().reset_index()
    return_counts.columns = ["returning", "count"]

    # Map True/False to readable labels
    return_counts["returning"] = return_counts["returning"].map({
        True: "Returning Customers",
        False: "New Customers"
    })

    # Create pie chart
    fig = go.Figure(
        data=[
            go.Pie(
                labels=return_counts["returning"],
                values=return_counts["count"],
                hole=0.4,  # donut style
                textinfo="label+percent",
                marker=dict(colors=["#2ca02c", "#ff7f0e"])
            )
        ]
    )

    fig.update_layout(
        title="🧾 Returning vs New Customers",
        template="plotly_white",
        legend=dict(
            title="Customer Type",
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )

    return fig
