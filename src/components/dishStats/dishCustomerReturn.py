import plotly.graph_objects as go

def create_dish_customer_return_chart(filtered_df, dish_name):

    # Count returning vs non-returning customers
    return_counts = filtered_df["return"].value_counts().reset_index()
    return_counts.columns = ["returning", "count"]

    # Total for percentage
    total = return_counts["count"].sum()

    # Map labels
    label_map = {
        True: f"Would reorder {dish_name}",
        False: f"Would not reorder {dish_name}"
    }
    return_counts["returning"] = return_counts["returning"].map(label_map)

    # Compute percentages
    return_counts["percent"] = (return_counts["count"] / total * 100).round(1)

    # Display text: "42 (63%)"
    return_counts["display"] = return_counts.apply(
        lambda row: f"{row['count']} ({row['percent']}%)", axis=1
    )

    # Color map
    colors = return_counts["returning"].map({
        f"Would reorder {dish_name}": "#2ca02c",  
        f"Would not reorder {dish_name}": "#d62728" 
    })

    # Horizontal bar chart
    fig = go.Figure(
        data=go.Bar(
            x=return_counts["count"],
            y=return_counts["returning"],
            orientation="h",
            text=return_counts["display"],   
            textposition="auto",
            marker=dict(color=colors)
        )
    )

    fig.update_layout(
        title=f"📊 Customer Reorder Intent for {dish_name}",
        xaxis_title="Number of Customers",
        yaxis_title="",
        template="plotly_white",
        bargap=0.3,
    )

    return fig
