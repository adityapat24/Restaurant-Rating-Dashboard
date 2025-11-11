"""
Chart components using Plotly
"""

import random
from datetime import datetime, timedelta
import pandas as pd
from faker import Faker
import plotly.express as px
import plotly.graph_objects as go
from data.loadData import loadData
from dash import dcc, html, Input, Output




# Helper to build merged dataframe from mockData.json
def _build_merged_df():
    data = loadData()
    reviews_df = pd.DataFrame(data.get("reviews", []))
    ratings_df = pd.DataFrame(data.get("ratings", []))
    menu_df = pd.DataFrame(data.get("menuItems", []))
    content_df = pd.DataFrame(data.get("content", [])) if data.get("content") else pd.DataFrame()

    # Safe merges — reviews are expected to have rating_id and menu_item_id
    if not reviews_df.empty and not ratings_df.empty and not menu_df.empty:
        merged = (
            reviews_df
            .merge(ratings_df, left_on="rating_id", right_on="id", suffixes=("_review", "_rating"))
            .merge(menu_df, left_on="menu_item_id", right_on="id", suffixes=("", "_menu"))
        )
        # If content exists, merge in text content
        if not content_df.empty and "content_id" in merged.columns:
            merged = merged.merge(content_df, left_on="content_id", right_on="id", suffixes=("", "_content"))
        return merged

    # Fallback empty df
    return pd.DataFrame()



def create_performance_chart():
    """
    Create a scatter plot showing rating vs review count
    """
    merged = _build_merged_df()

    names = []
    ratings = []
    reviews = []
    colors = []

    if not merged.empty:
        # Expect merged to contain: name, taste, portion, value, rating_id (or id)
        # Compute per-dish aggregated ratings
        # Use the explicit `overall` rating in the ratings table when available
        grp = merged.groupby("name").agg(
            overall_mean=("overall", "mean"),
            review_count=("rating_id", "count")
        ).reset_index()

        for _, row in grp.iterrows():
            # prefer the recorded overall mean if present
            overall = row.get("overall_mean")

            names.append(row["name"])
            ratings.append(overall)
            reviews.append(int(row["review_count"]))

            if overall < 3:
                colors.append("#ef4444")
            elif overall < 4.2:
                colors.append("#f59e0b")
            else:
                colors.append("#10b981")
    else:
        # Fallback: empty dataset
        return go.Figure()
    
    # Create figure
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=reviews,
        y=ratings,
        mode='markers',
        marker=dict(
            size=12,
            color=colors,
            line=dict(width=1, color='white')
        ),
        text=names,
        hovertemplate='<b>%{text}</b><br>' +
                      'Rating: %{y}<br>' +
                      'Reviews: %{x}<br>' +
                      '<extra></extra>'
    ))
    
    # Update layout
    fig.update_layout(
        title={
            'text': 'Dish Performance: Rating vs Review Count',
            'font': {'size': 18, 'color': '#1f2937'}
        },
        xaxis_title='Review Count',
        yaxis_title='Average Rating',
        yaxis=dict(range=[0, 5]),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12, color='#4b5563'),
        height=450,
        margin=dict(l=60, r=30, t=80, b=80),
        annotations=[
            dict(
                text='Lower left quadrant = High priority for improvement (low rating, many reviews)',
                xref='paper',
                yref='paper',
                x=0,
                y=1.08,
                showarrow=False,
                font=dict(size=11, color='#6b7280'),
                xanchor='left'
            )
        ]
    )
    
    # Update axes
    fig.update_xaxes(
        showgrid=True,
        gridcolor='#e5e7eb',
        zeroline=False
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridcolor='#e5e7eb',
        zeroline=False
    )
    
    return fig


def create_all_stats_over_time_chart():
    merged = _build_merged_df()
    merged["Date"] = pd.to_datetime(merged["timestamp"], errors="coerce")
    years = sorted(merged["Date"].dt.year.dropna().unique().astype(int).tolist())

    # Create a component (dropdown + graph). The app should call register_all_stats_callbacks(app)
    dropdown = dcc.Dropdown(
        id="all-stats-year-dropdown",
        options=[{"label": str(y), "value": int(y)} for y in years],
        value=years[-1] if years else None,
        clearable=False,
        placeholder="Select year"
    )

    # Use the figure helper so plotting logic is centralized.
    selected_year = years[-1] if years else None
    initial_fig = create_all_stats_figure_for_year(selected_year, merged) if selected_year is not None else go.Figure()

    container = html.Div(
        children=[
            html.Div(children=[dropdown], style={"width": "200px", "marginBottom": "12px"}),
            dcc.Graph(id="all-stats-graph", figure=initial_fig, config={"displayModeBar": False})
        ]
    )

    return container


def create_review_charts():
    """
    Return two Plotly figures:
    (1) Most recent 10 reviews
    (2) Review volume over time
    """
    merged = _build_merged_df()

    if not merged.empty:
        # ensure timestamp is datetime
        if "timestamp" in merged.columns:
            merged["Date"] = pd.to_datetime(merged["timestamp"], errors="coerce")
        elif "Date" in merged.columns:
            merged["Date"] = pd.to_datetime(merged["Date"], errors="coerce")

        # Use recorded overall rating where available
        if "overall" in merged.columns:
            merged["Overall Rating"] = merged["overall"]
        else:
            # attempt to synthesize if not present
            merged["Overall Rating"] = merged[[c for c in ["taste", "portion", "value"] if c in merged.columns]].mean(axis=1)

        df_sorted = merged.sort_values(by="Date", ascending=False)
        last_10_reviews = df_sorted.head(10)

        # Reviews per month over time
        merged["YearMonth"] = merged["Date"].dt.to_period("M").astype(str)
        reviews_over_time = merged.groupby("YearMonth").size().reset_index(name="Review Count")
    else:
        # Fallback to synthetic sample data
        fake = Faker()
        random.seed(42)
        Faker.seed(42)

        dishes = [
            "Margherita Pizza", "Truffle Pasta", "Spicy Tuna Roll", "Caesar Salad",
            "BBQ Burger", "Avocado Toast", "Lobster Bisque", "Chicken Tikka Masala",
            "Chocolate Lava Cake", "Sushi Platter", "Steak Frites", "Vegan Bowl"
        ]

        # Generate reviews
        reviews = []
        for _ in range(150):
            dish = random.choice(dishes)
            overall = random.randint(3, 5)
            taste = random.randint(2, 5)
            texture = random.randint(2, 5)
            portion = random.randint(2, 5)
            text = fake.sentence(nb_words=random.randint(10, 20))
            days_ago = random.randint(0, 3 * 365)
            date = datetime.now() - timedelta(days=days_ago)

            reviews.append({
                "Dish": dish,
                "Overall Rating": overall,
                "Taste Rating": taste,
                "Texture Rating": texture,
                "Price-to-Portion Rating": portion,
                "Review Text": text,
                "Date": date
            })

        df = pd.DataFrame(reviews)
        df_sorted = df.sort_values(by="Date", ascending=False)
        last_10_reviews = df_sorted.head(10)

        # Reviews per month over time
        df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)
        reviews_over_time = df.groupby("YearMonth").size().reset_index(name="Review Count")

    # Line chart
    line_fig = px.line(
        reviews_over_time,
        x="YearMonth",
        y="Review Count",
        title="📅 Review Volume Over Time",
        markers=True
    )
    line_fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Review Count",
        hovermode="x unified"
    )

    # Scatter chart
    # adapt to column names depending on whether merged data or synthetic was used
    text_col = "name" if "name" in last_10_reviews.columns else "Dish"
    taste_col = "taste" if "taste" in last_10_reviews.columns else "Taste Rating"
    texture_col = "portion" if "portion" in last_10_reviews.columns else "Texture Rating"
    price_col = "value" if "value" in last_10_reviews.columns else "Price-to-Portion Rating"
    review_text_col = "content" if "content" in last_10_reviews.columns else "Review Text"

    scatter_fig = px.scatter(
        last_10_reviews,
        x="Date",
        y="Overall Rating",
        text=text_col,
        hover_data={
            text_col: True,
            "Overall Rating": True,
            taste_col: True,
            texture_col: True,
            price_col: True,
            review_text_col: True,
            "Date": True
        },
        title="⭐ Most Recent 10 Reviews",
    )
    scatter_fig.update_traces(marker=dict(size=12, color="orange"))
    scatter_fig.update_layout(xaxis_title="Date", yaxis_title="Overall Rating")

    return scatter_fig, line_fig


def create_all_stats_figure_for_year(year: int, merged: pd.DataFrame) -> go.Figure:
    """Utility: return the figure for a specific year (used by callbacks)."""
    if merged.empty:
        return go.Figure()

    # Work on a copy to avoid modifying the original dataframe
    merged = merged.copy()

    if "timestamp" in merged.columns:
        merged["Date"] = pd.to_datetime(merged["timestamp"], errors="coerce")
    elif "Date" in merged.columns:
        merged["Date"] = pd.to_datetime(merged["Date"], errors="coerce")
    else:
        return go.Figure()

    merged["YearMonth"] = merged["Date"].dt.to_period("M").astype(str)
    merged["Year"] = merged["Date"].dt.year

    # Use explicit overall
    merged["Overall"] = merged["overall"].astype(float)

    agg_cols = {"Overall": ("Overall", "mean")}
    if "taste" in merged.columns:
        agg_cols["Taste"] = ("taste", "mean")
    if "portion" in merged.columns:
        agg_cols["Portion"] = ("portion", "mean")
    if "value" in merged.columns:
        agg_cols["Value"] = ("value", "mean")

    monthly = merged.groupby("YearMonth").agg(**agg_cols).reset_index()
    for col in ["Overall", "Taste", "Portion", "Value"]:
        if col not in monthly.columns:
            monthly[col] = 0

    # YearMonth is YYYY-MM — append day and parse using %Y-%m-%d
    monthly["Year"] = pd.to_datetime(monthly["YearMonth"] + "-01", format="%Y-%m-%d", errors="coerce").dt.year
    df = monthly[monthly["Year"] == int(year)].sort_values("YearMonth")

    fig = go.Figure()
    if not df.empty:
        fig.add_trace(go.Scatter(x=df["YearMonth"], y=df["Overall"], mode="lines+markers", name="Overall", marker=dict(size=6), line=dict(color="#7c3aed")))
        fig.add_trace(go.Scatter(x=df["YearMonth"], y=df["Taste"], mode="lines+markers", name="Taste", marker=dict(size=6), line=dict(color="#ef4444")))
        fig.add_trace(go.Scatter(x=df["YearMonth"], y=df["Portion"], mode="lines+markers", name="Portion", marker=dict(size=6), line=dict(color="#3b82f6")))
        fig.add_trace(go.Scatter(x=df["YearMonth"], y=df["Value"], mode="lines+markers", name="Value", marker=dict(size=6), line=dict(color="#10b981")))

    fig.update_layout(
        title={"text": f"Ratings Trend Over Time — {year}", "font": {"size": 16, "color": "#1f2937"}},
        xaxis_title="Month",
        yaxis_title="Average Rating",
        yaxis=dict(range=[0, 5]),
        hovermode="x unified",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family='Arial, sans-serif', size=12, color="#4b5563"),
        height=420,
        margin=dict(l=60, r=30, t=80, b=80),
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="#e5e7eb")

    return fig


def register_all_stats_callbacks(app):
    """Register callbacks for the All Stats chart. Call this after Dash app creation.

    Example (in `app.py`):
        from components.charts import register_all_stats_callbacks
        register_all_stats_callbacks(app)
    """

    @app.callback(Output("all-stats-graph", "figure"), Input("all-stats-year-dropdown", "value"))
    def _update_all_stats_graph(selected_year):
        if not selected_year:
            return go.Figure()
        return create_all_stats_figure_for_year(selected_year, _build_merged_df())

