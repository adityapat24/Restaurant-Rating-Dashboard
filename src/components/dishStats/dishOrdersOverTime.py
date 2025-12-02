import plotly.express as px
import pandas as pd

def create_dish_orders_over_time(filtered_df, dish_name):
    if "timestamp" not in filtered_df.columns:
        return px.line(title=f"No timestamp data for {dish_name}")

    filtered_df["timestamp"] = pd.to_datetime(filtered_df["timestamp"])
    orders_by_month = (
        filtered_df.groupby(filtered_df["timestamp"].dt.to_period("M"))
        .size()
        .reset_index(name="Orders")
    )
    orders_by_month["Month"] = orders_by_month["timestamp"].dt.strftime("%b %Y")

    fig = px.line(
        orders_by_month,
        x="Month",
        y="Orders",
        markers=True,
        title=f"<b>Number of Orders Over Time for {dish_name}</b><br><sup>How have orders changed over each month?</sup>",
    )
    fig.update_layout(title_x=0.5, xaxis_title="Month", yaxis_title="Orders")
    return fig
