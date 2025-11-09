import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
from data.loadData import loadData

dash.register_page(__name__, path="/dish-stats", name="Dish Analytics")

# Load data once
data = loadData()
reviews_df = pd.DataFrame(data["reviews"])
ratings_df = pd.DataFrame(data["ratings"])
menu_df = pd.DataFrame(data["menuItems"])

# Merge to get dish names with ratings
merged_df = reviews_df.merge(
    ratings_df, left_on="rating_id", right_on="id", suffixes=("_review", "_rating")
)
merged_df = merged_df.merge(
    menu_df, left_on="menu_item_id", right_on="id", suffixes=("", "_menu")
)

# Layout for the page
layout = html.Div(
    [
        html.H2(
            "🍽️ Individual Dish Analytics",
            style={"textAlign": "center", "marginBottom": "20px"},
        ),

        html.Div(
            [
                dcc.Dropdown(
                    id="dish-dropdown",
                    options=[{"label": name, "value": name} for name in sorted(merged_df["name"].unique())],
                    placeholder="Select a dish...",
                    style={"width": "50%", "display": "inline-block", "marginRight": "10px"},
                ),
                html.Button(
                    "View Stats",
                    id="view-stats-btn",
                    n_clicks=0,
                    className="btn btn-primary",
                    style={"verticalAlign": "middle"},
                ),
            ],
            style={"textAlign": "center", "marginBottom": "25px"},
        ),

        # Start with no figure shown
        html.Div(id="dish-rating-container", style={"textAlign": "center"}),
    ]
)


# Callback to generate the chart only after clicking
@dash.callback(
    Output("dish-rating-container", "children"),
    Input("view-stats-btn", "n_clicks"),
    State("dish-dropdown", "value"),
    prevent_initial_call=True
)
def update_dish_stats(n_clicks, dish_name):
    if not dish_name:
        return html.Div("Please select a dish to view stats.", style={"fontSize": "18px", "color": "gray"})

    filtered = merged_df[merged_df["name"] == dish_name]
    if filtered.empty:
        return html.Div("No reviews found for this dish.", style={"fontSize": "18px", "color": "gray"})

    rating_counts = filtered["overall"].value_counts().sort_index()
    df = pd.DataFrame({"Rating": rating_counts.index, "Count": rating_counts.values})

    fig = px.pie(
        df,
        values="Count",
        names="Rating",
        title=f"Overall Rating Distribution for {dish_name}",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )

    fig.update_traces(textinfo="label+percent", pull=[0.05] * len(df))
    fig.update_layout(title_x=0.5, margin=dict(l=40, r=40, t=80, b=40))

    return dcc.Graph(figure=fig, style={"height": "600px"})
