"""
Restaurant Analytics Dashboard - Main Application
Built with Dash and Plotly
"""

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from data.dishes import (
    get_top_rated_dishes,
    get_bottom_rated_dishes,
    get_all_dishes,
    calculate_average_rating
)
from components.dish_card import create_dish_card
from components.charts import (
    create_histogram_price_ranges,
    create_performance_chart,
    create_weak_points_chart,
    create_histogram_price_ranges
)

# Initialize the Dash app
app = dash.Dash(
    __name__,
    title="Restaurant Analytics Dashboard",
    suppress_callback_exceptions=True
)

# Define the layout
app.layout = html.Div(
    className="app-container",
    children=[
        # Header
        html.Div(
            className="header",
            children=[
                html.Div(
                    className="header-content",
                    children=[
                        # Icon and Title
                        html.Div(
                            className="header-title-row",
                            children=[
                                html.Span("🍴", className="header-icon"),
                                html.H1("Restaurant Analytics Dashboard", className="header-title")
                            ]
                        ),
                        html.P(
                            "Track dish performance and identify areas for improvement",
                            className="header-subtitle"
                        )
                    ]
                )
            ]
        ),
        
        # Main Content
        html.Div(
            className="main-content",
            children=[
                # Tabs for Top/Bottom Rated
                html.Div(
                    className="tabs-container",
                    children=[
                        dcc.Tabs(
                            id="dish-tabs",
                            value="top",
                            className="custom-tabs",
                            children=[
                                dcc.Tab(
                                    label="📈 Top Rated",
                                    value="top",
                                    className="custom-tab",
                                    selected_className="custom-tab--selected"
                                ),
                                dcc.Tab(
                                    label="📉 Needs Improvement",
                                    value="bottom",
                                    className="custom-tab",
                                    selected_className="custom-tab--selected"
                                )
                            ]
                        ),
                        html.Div(id="dish-cards-container", className="dish-cards-grid")
                    ]
                ),
                
                # Charts
                html.Div(
                    className="charts-container",
                    children=[
                        html.Div(
                            className="chart-wrapper",
                            children=[
                                dcc.Graph(
                                    id="performance-chart",
                                    figure=create_performance_chart(),
                                    config={'displayModeBar': False}
                                )
                            ]
                        ),
                        html.Div(
                            className="chart-wrapper",
                            children=[
                                dcc.Graph(
                                    id="weak-points-chart",
                                    figure=create_weak_points_chart(),
                                    config={'displayModeBar': False}
                                )
                            ]
                        )
                    ]
                ),

                
                # Price range histogram
                html.Div(
                    className="charts-container",
                    children=[
                        html.Div(
                            className="chart-wrapper",
                            children=[
                                dcc.Graph(
                                    id="price-histogram",
                                    figure=create_histogram_price_ranges(),
                                    config={'displayModeBar': False}
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

# Callback to update dish cards based on selected tab
@app.callback(
    Output("dish-cards-container", "children"),
    Input("dish-tabs", "value")
)
def update_dish_cards(tab_value):
    if tab_value == "top":
        dishes = get_top_rated_dishes(5)
    else:
        dishes = get_bottom_rated_dishes(5)
    
    cards = []
    for index, dish in enumerate(dishes):
        cards.append(create_dish_card(dish, rank=index + 1))
    
    return cards

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
