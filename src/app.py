"""
Restaurant Analytics Dashboard - Main Application
Multi-page setup with Sidebar Navigation
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

<<<<<<< Updated upstream
# Initialize Dash app with multi-page support
=======
from components.customerSatisfactionMetrics.monthlyTastePortionValue import (
    create_monthly_category_ratings_chart
)

from components.customerSatisfactionMetrics.customer_return import (
    create_customer_return_chart
)

from components.operationalMetrics.lastTenReviews import (
    create_last_ten_reviews_table
)

from components.operationalMetrics.OvertimeRating import (
    create_average_rating_over_time
) 

from components.customerSatisfactionMetrics.CategoryKPI import (
    create_category_kpi_cards
)


# Initialize the Dash app
>>>>>>> Stashed changes
app = dash.Dash(
    __name__,
    use_pages=True,  # Enables multiple pages
    title="Platemate Restaurant Analytics Dashboard",
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
server = app.server  # For deployment (e.g. Render, Heroku)

# ----------------------------
# Sidebar for navigation
# ----------------------------
sidebar = html.Div(
    [
        html.H2("🍽️ Platemate", className="display-6", style={"textAlign": "center"}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("🏠 Dashboard", href="/", active="exact"),
                dbc.NavLink("📊 Dish Analytics", href="/dish-stats", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "220px",
        "padding": "20px",
        "backgroundColor": "#f8f9fa",
    },
)

<<<<<<< Updated upstream
# ----------------------------
# Main content area (page container)
# ----------------------------
content = html.Div(
    dash.page_container,
    style={
        "marginLeft": "240px",
        "marginRight": "20px",
        "padding": "20px 10px",
    },
)

# ----------------------------
# App Layout
# ----------------------------
app.layout = html.Div([sidebar, content])

# ----------------------------
# Run the App
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True, port=8050)
=======
recent_reviews_fig, reviews_line_fig = create_review_charts()
monthly_rating_fig = create_monthly_mean_rating_chart()
monthly_category_fig = create_monthly_category_ratings_chart()
customer_return = create_customer_return_chart()
last_10_reviews_fig = create_last_ten_reviews_table()
avg_rating_over_time_fig = create_average_rating_over_time() 

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
                                html.H1("Platemate Restaurant Analytics Dashboard", className="header-title")
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
                        # Price range histogram
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
                ),
                html.Hr(style={"marginTop": "60px", "marginBottom": "30px"}),

                html.Div(
                    className="reviews-section",
                    children=[
                        html.H2("🗒️ Customer Reviews", style={"textAlign": "center", "marginBottom": "20px"}),
                        
                        # KPI Cards with Dropdown
                        html.Div(
                            className="kpi-section",
                            style={"marginBottom": "40px"},
                            children=[
                                html.Div(
                                    className="filter-container",
                                    style={"textAlign": "center", "marginBottom": "20px"},
                                    children=[
                                        html.Label("Time Period:", style={"marginRight": "10px", "fontWeight": "bold", "fontSize": "16px"}),
                                        dcc.Dropdown(
                                            id="kpi-period-dropdown",
                                            options=[
                                                {"label": "📊 Overall (All Time)", "value": "overall"},
                                                {"label": "📅 This Month", "value": "month"},
                                                {"label": "📆 This Week", "value": "week"}
                                            ],
                                            value="overall",
                                            clearable=False,
                                            style={"width": "300px", "display": "inline-block"}
                                        )
                                    ]
                                ),
                                html.Div(
                                    className="chart-wrapper",
                                    children=[
                                        dcc.Graph(
                                            id="category-kpi-cards",
                                            config={'displayModeBar': False}
                                        )
                                    ]
                                )
                            ]
                        ),
                        
                        html.Div(
                            className="chart-wrapper",
                            children=[
                                dcc.Graph(
                                    id="reviews-over-time",
                                    figure=reviews_line_fig,
                                    config={'displayModeBar': False}
                                )
                            ]
                        ),
                        html.Div(
                            className="chart-wrapper",
                            children=[
                                dcc.Graph(
                                    id="avg-rating-over-time",
                                    figure=avg_rating_over_time_fig,
                                    config={"displayModeBar": False}
                                )
                            ]
                        ),
                        html.Div(
                            className="chart-wrapper",
                            children=[
                                dcc.Graph(
                                    id="monthly-mean-rating-chart",
                                    figure=create_monthly_mean_rating_chart(),
                                    config={'displayModeBar': False}
                                )
                            ]
                        ),
                        html.Div(
                            className="chart-wrapper",
                            children=[
                                dcc.Graph(
                                    id="monthly-category-rating-chart",
                                    figure=monthly_category_fig,
                                    config={'displayModeBar': False}
                                )
                            ]
                        ),
                        html.Div(
                            className="chart-wrapper",
                            children=[
                                dcc.Graph(
                                    id="customer_return",
                                    figure=customer_return,
                                    config={'displayModeBar': False}
                                )
                            ]
                        ),
                        html.Div(
                            className="chart-wrapper",
                            children=[
                                dcc.Graph(
                                    id="last_ten_reviews",
                                    figure=last_10_reviews_fig,
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


# Callback to update KPI cards based on selected time period
@app.callback(
    Output("category-kpi-cards", "figure"),
    Input("kpi-period-dropdown", "value")
)
def update_kpi_cards(period):
    return create_category_kpi_cards(period)


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
>>>>>>> Stashed changes
