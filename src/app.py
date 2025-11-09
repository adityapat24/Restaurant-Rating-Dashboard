"""
Restaurant Analytics Dashboard - Main Application
Multi-page setup with Sidebar Navigation
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Initialize Dash app with multi-page support
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
