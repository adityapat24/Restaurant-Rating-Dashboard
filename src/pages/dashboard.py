# pages/dashboard.py
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from data.dishes import (
    get_top_rated_dishes,
    get_bottom_rated_dishes,
)
from components.dish_card import create_dish_card
from components.charts import (
    create_histogram_price_ranges,
    create_performance_chart,
    create_review_charts,
)
from components.customerSatisfactionMetrics.montlyOverallRating import (
    create_monthly_mean_rating_chart,
)
from components.customerSatisfactionMetrics.monthlyTastePortionValue import (
    create_monthly_category_ratings_chart,
)
from components.customerSatisfactionMetrics.customer_return import (
    create_customer_return_chart,
)
from components.operationalMetrics.lastTenReviews import (
    create_last_ten_reviews_table,
)

# Register the page
dash.register_page(__name__, path="/", name="Dashboard")

# Load static figures (you can later move them to callbacks if needed)
recent_reviews_fig, reviews_line_fig = create_review_charts()
monthly_rating_fig = create_monthly_mean_rating_chart()
monthly_category_fig = create_monthly_category_ratings_chart()
customer_return_fig = create_customer_return_chart()
last_10_reviews_table = create_last_ten_reviews_table()

# Define page layout
layout = html.Div(
    className="app-container",
    children=[
        # Header
        html.Div(
            className="header",
            children=[
                html.Div(
                    className="header-content",
                    children=[
                        html.Div(
                            className="header-title-row",
                            children=[
                                html.Span("🍴", className="header-icon"),
                                html.H1(
                                    "Platemate Restaurant Analytics Dashboard",
                                    className="header-title",
                                ),
                            ],
                        ),
                        html.P(
                            "Track dish performance and identify areas for improvement",
                            className="header-subtitle",
                        ),
                    ],
                )
            ],
        ),

        # Tabs for Top/Bottom Rated Dishes
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
                            selected_className="custom-tab--selected",
                        ),
                        dcc.Tab(
                            label="📉 Needs Improvement",
                            value="bottom",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ),
                    ],
                ),
                html.Div(id="dish-cards-container", className="dish-cards-grid"),
            ],
        ),

        # Charts Section
        html.Div(
            className="charts-container",
            children=[
                html.Div(
                    className="chart-wrapper",
                    children=[
                        dcc.Graph(
                            id="performance-chart",
                            figure=create_performance_chart(),
                            config={"displayModeBar": False},
                        )
                    ],
                ),
                html.Div(
                    className="chart-wrapper",
                    children=[
                        dcc.Graph(
                            id="price-histogram",
                            figure=create_histogram_price_ranges(),
                            config={"displayModeBar": False},
                        )
                    ],
                ),
            ],
        ),

        html.Hr(style={"marginTop": "60px", "marginBottom": "30px"}),

        # Customer Reviews Section
        html.Div(
            className="reviews-section",
            children=[
                html.H2(
                    "🗒️ Customer Reviews",
                    style={"textAlign": "center", "marginBottom": "20px"},
                ),

                html.Div(
                    className="chart-wrapper",
                    children=[
                        dcc.Graph(
                            id="reviews-over-time",
                            figure=reviews_line_fig,
                            config={"displayModeBar": False},
                        )
                    ],
                ),

                html.Div(
                    className="chart-wrapper",
                    children=[
                        dcc.Graph(
                            id="monthly-mean-rating-chart",
                            figure=monthly_rating_fig,
                            config={"displayModeBar": False},
                        )
                    ],
                ),

                html.Div(
                    className="chart-wrapper",
                    children=[
                        dcc.Graph(
                            id="monthly-category-rating-chart",
                            figure=monthly_category_fig,
                            config={"displayModeBar": False},
                        )
                    ],
                ),

                html.Div(
                    className="chart-wrapper",
                    children=[
                        dcc.Graph(
                            id="customer-return-chart",
                            figure=customer_return_fig,
                            config={"displayModeBar": False},
                        )
                    ],
                ),

                html.Div(
                    className="chart-wrapper",
                    children=[
                        dcc.Graph(
                            id="last-ten-reviews",
                            figure=last_10_reviews_table,
                            config={"displayModeBar": False},
                        )
                    ],
                ),
            ],
        ),
    ],
)


# Register callback for tab interaction (must use dash.get_app() when using pages)
from dash import callback, Output, Input

@callback(Output("dish-cards-container", "children"), Input("dish-tabs", "value"))
def update_dish_cards(tab_value):
    if tab_value == "top":
        dishes = get_top_rated_dishes(5)
    else:
        dishes = get_bottom_rated_dishes(5)

    return [create_dish_card(d, rank=i + 1) for i, d in enumerate(dishes)]
