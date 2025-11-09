import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from data.loadData import loadData

def create_average_rating_over_time():
    """
    Create an area line chart showing average rating trends over time.
    
    Purpose: Track whether satisfaction is improving or declining.
    Uses color coding to indicate upward vs downward trends.

    """
    # Load data
    data = loadData()
    
    # Create DataFrames
    reviews_df = pd.DataFrame(data["reviews"])
    ratings_df = pd.DataFrame(data["ratings"])
    
    # Merge reviews with ratings to get actual rating values
    df = reviews_df.merge(
        ratings_df[["id", "overall"]], 
        left_on="rating_id", 
        right_on="id", 
        suffixes=("_review", "_rating")
    )
    
    # Convert timestamp to datetime
    df["date"] = pd.to_datetime(df["timestamp"], errors="coerce")
    
    # Group by month and calculate average rating
    df["YearMonth"] = df["date"].dt.to_period("M").astype(str)
    avg_rating_over_time = df.groupby("YearMonth")["overall"].mean().reset_index()
    avg_rating_over_time.columns = ["Month", "Average Rating"]
    
    # Calculate trend: compare each month to previous month
    avg_rating_over_time["Trend"] = avg_rating_over_time["Average Rating"].diff()
    avg_rating_over_time["Trend_Direction"] = avg_rating_over_time["Trend"].apply(
        lambda x: "Improving" if x > 0 else ("Declining" if x < 0 else "Stable")
    )
    
    # Create the figure
    fig = go.Figure()
    
    # Add area chart with gradient fill
    fig.add_trace(go.Scatter(
        x=avg_rating_over_time["Month"],
        y=avg_rating_over_time["Average Rating"],
        mode="lines",
        name="Average Rating",
        line=dict(color="#2196F3", width=3),
        fill="tozeroy",
        fillcolor="rgba(33, 150, 243, 0.3)",
        hovertemplate="<b>%{x}</b><br>Avg Rating: %{y:.2f}<extra></extra>"
    ))
    
    # Add colored markers based on trend
    colors = avg_rating_over_time["Trend_Direction"].map({
        "Improving": "#4CAF50",  # Green
        "Declining": "#F44336",  # Red
        "Stable": "#FFC107"      # Yellow
    })
    
    fig.add_trace(go.Scatter(
        x=avg_rating_over_time["Month"],
        y=avg_rating_over_time["Average Rating"],
        mode="markers",
        name="Trend Indicator",
        marker=dict(
            size=10,
            color=colors,
            line=dict(color="white", width=2)
        ),
        hovertemplate="<b>%{x}</b><br>Avg Rating: %{y:.2f}<br>Trend: %{customdata}<extra></extra>",
        customdata=avg_rating_over_time["Trend_Direction"]
    ))
    
    # Update layout
    fig.update_layout(
        title="📈 Average Rating Over Time",
        xaxis_title="Month",
        yaxis_title="Average Overall Rating (out of 5)",
        plot_bgcolor="white",
        hovermode="x unified",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        font=dict(size=12),
        xaxis=dict(showgrid=True, gridcolor="lightgray"),
        yaxis=dict(
            showgrid=True, 
            gridcolor="lightgray",
            range=[0, 5.5]  # Rating scale 0-5
        )
    )
    
    # Add reference line at neutral rating (3.0)
    fig.add_hline(
        y=3.0, 
        line_dash="dash", 
        line_color="gray", 
        annotation_text="Neutral (3.0)",
        annotation_position="right"
    )
    
    return fig


if __name__ == "__main__":
    fig = create_average_rating_over_time()
    fig.write_html("average_rating_over_time.html")
    print("chart ")