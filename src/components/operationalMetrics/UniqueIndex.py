import sys
from pathlib import Path
# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Then your import will work:
from data.loadData import loadData
import pandas as pd
import plotly.express as px

import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from data.loadData import loadData


def create_reviewer_diversity_chart():
    """
    Create a simple chart showing unique vs repeat reviewers.
    
    Purpose: Shows if feedback is coming from a broad base or a few frequent users.
    
    Returns:
        plotly.graph_objects.Figure: Bar chart comparing unique vs repeat reviewers
    """
    # Load data
    data = loadData()
    reviews_df = pd.DataFrame(data["reviews"])
    
    # Count reviews per reviewer
    reviewer_counts = reviews_df["reviewer_id"].value_counts()
    
    # Calculate metrics
    unique_reviewers = len(reviewer_counts)  # Total number of unique reviewers
    one_time_reviewers = (reviewer_counts == 1).sum()  # Reviewers with only 1 review
    repeat_reviewers = (reviewer_counts > 1).sum()  # Reviewers with 2+ reviews
    
    # Create bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=["One-Time Reviewers", "Repeat Reviewers"],
        y=[one_time_reviewers, repeat_reviewers],
        marker_color=["#2196F3", "#4CAF50"],
        text=[one_time_reviewers, repeat_reviewers],
        textposition="auto",
        hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>"
    ))
    
    # Update layout
    fig.update_layout(
        title="Reviewer Diversity: One-Time vs Repeat Reviewers",
        xaxis_title="Reviewer Type",
        yaxis_title="Number of Reviewers",
        plot_bgcolor="white",
        showlegend=False,
        font=dict(size=12),
        yaxis=dict(showgrid=True, gridcolor="lightgray"),
        annotations=[
            dict(
                text=f"Total Unique Reviewers: {unique_reviewers}",
                xref="paper",
                yref="paper",
                x=0.5,
                y=1.1,
                showarrow=False,
                font=dict(size=14, color="gray")
            )
        ]
    )
    
    return fig
