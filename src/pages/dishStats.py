import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
from data.loadData import loadData

# Import dish insights

from components.dishStats.dishOverall import create_dish_overall_pie
from components.dishStats.dishCategoryBreakdown import create_dish_category_breakdown
from components.dishStats.dishSentiment import create_dish_sentiment_chart
from components.dishStats.dishOrdersOverTime import create_dish_orders_over_time
from components.dishStats.dishCustomerReturn import create_dish_customer_return_chart

dash.register_page(__name__, path="/dish-stats", name="Dish Analytics")

# Load data once
# Load data once
data = loadData()
reviews_df = pd.DataFrame(data["reviews"])
ratings_df = pd.DataFrame(data["ratings"])
menu_df = pd.DataFrame(data["menuItems"])
content_df = pd.DataFrame(data["content"]) 

# Merge reviews with ratings and menu
merged_df = (
    reviews_df
    .merge(ratings_df, left_on="rating_id", right_on="id", suffixes=("_review", "_rating"))
    .merge(menu_df, left_on="menu_item_id", right_on="id", suffixes=("", "_menu"))
    .merge(content_df, left_on="content_id", right_on="id", suffixes=("", "_content"))
)


layout = html.Div(
    [
        html.H2("🍽️ Individual Dish Analytics", style={"textAlign": "center", "marginBottom": "20px"}),

        html.Div(
            [
                dcc.Dropdown(
                    id="dish-dropdown",
                    options=[{"label": name, "value": name} for name in sorted(merged_df["name"].unique())],
                    placeholder="Select a dish...",
                    style={"width": "50%", "display": "inline-block", "marginRight": "10px"},
                ),
                html.Button(
                    "View Insights",
                    id="view-stats-btn",
                    n_clicks=0,
                    className="btn btn-primary",
                    style={"verticalAlign": "middle"}
                ),
            ],
            style={"textAlign": "center", "marginBottom": "25px"},
        ),

        html.Div(id="dish-insights-container"),
    ]
)

@dash.callback(
    Output("dish-insights-container", "children"),
    Input("view-stats-btn", "n_clicks"),
    State("dish-dropdown", "value"),
    prevent_initial_call=True
)
def update_dish_insights(n_clicks, dish_name):
    if not dish_name:
        return html.P("Please select a dish to view insights.", style={"textAlign": "center", "color": "gray"})

    filtered = merged_df[merged_df["name"] == dish_name]

    pie_fig = create_dish_overall_pie(filtered, dish_name)
    category_fig = create_dish_category_breakdown(filtered, dish_name)
    sentiment_fig = create_dish_sentiment_chart(filtered, dish_name)
    orders_fig = create_dish_orders_over_time(filtered, dish_name)
    returning_fig = create_dish_customer_return_chart(filtered, dish_name)

    return html.Div(
        [
            dcc.Graph(figure=pie_fig, style={"height": "500px"}),
            dcc.Graph(figure=category_fig, style={"height": "500px"}),
            dcc.Graph(figure=sentiment_fig, style={"height": "500px"}),
            dcc.Graph(figure=orders_fig, style={"height": "500px"}),
            dcc.Graph(figure=returning_fig, style={"height": "500px"}),
        ]
    )
