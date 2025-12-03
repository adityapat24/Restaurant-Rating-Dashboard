# pages/ai_assistant.py
import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from components.ai.llm import rag_answer
import pandas as pd
import os

# Register the page
dash.register_page(__name__, path="/ai-assistant", name="AI Assistant")

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
                                html.Span("🤖", className="header-icon"),
                                html.H1(
                                    "AI Data Assistant",
                                    className="header-title",
                                ),
                            ],
                        ),
                        html.P(
                            "Ask questions about your restaurant data in natural language",
                            className="header-subtitle",
                        ),
                    ],
                )
            ],
        ),

        # Main content container
        html.Div(
            style={
                "maxWidth": "1200px",
                "margin": "40px auto",
                "padding": "0 20px",
            },
            children=[
                # Question input section
                html.Div(
                    style={
                        "backgroundColor": "#ffffff",
                        "borderRadius": "12px",
                        "padding": "30px",
                        "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
                        "marginBottom": "30px",
                    },
                    children=[
                        html.H3(
                            "Ask a Question",
                            style={"marginBottom": "20px", "color": "#2c3e50"},
                        ),
                        dbc.Textarea(
                            id="question-input",
                            placeholder="e.g., What are the top 5 highest rated menu items?\ne.g., Which dishes have the lowest ratings this month?\ne.g., Show me the average rating by category",
                            style={
                                "width": "100%",
                                "minHeight": "100px",
                                "marginBottom": "15px",
                                "fontSize": "16px",
                                "borderRadius": "8px",
                            },
                        ),
                        dbc.Button(
                            "🔍 Ask AI",
                            id="submit-button",
                            color="primary",
                            size="lg",
                            style={
                                "width": "200px",
                                "fontWeight": "bold",
                            },
                        ),
                    ],
                ),

                # Loading indicator
                dcc.Loading(
                    id="loading",
                    type="circle",
                    children=[
                        # Results container
                        html.Div(id="results-container"),
                    ],
                ),
            ],
        ),
    ],
)


@callback(
    Output("results-container", "children"),
    Input("submit-button", "n_clicks"),
    State("question-input", "value"),
    prevent_initial_call=True,
)
def process_question(n_clicks, question):
    if not question or question.strip() == "":
        return html.Div(
            style={
                "backgroundColor": "#fff3cd",
                "border": "1px solid #ffc107",
                "borderRadius": "8px",
                "padding": "20px",
                "color": "#856404",
            },
            children=[
                html.Strong("⚠️ Please enter a question first!")
            ],
        )

    try:
        # Get API key from environment or use the one from test file
        api_key = os.getenv("GEMINI_API_KEY")

        # Use absolute path for SQL file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sql_file = os.path.join(current_dir, "../data/data_fixed.sql")
        sql_file = os.path.abspath(sql_file)

        # Call the RAG pipeline
        answer = rag_answer(question, sql_file, api_key)

        # Parse the printed output to extract SQL and results
        # (This is a simple approach - in production you'd want to modify llm.py to return structured data)

        # Create results display
        results = html.Div([
            # Question display
            html.Div(
                style={
                    "backgroundColor": "#e3f2fd",
                    "borderRadius": "8px",
                    "padding": "20px",
                    "marginBottom": "20px",
                },
                children=[
                    html.H4("❓ Your Question:", style={"color": "#1976d2", "marginBottom": "10px"}),
                    html.P(question, style={"fontSize": "16px", "marginBottom": "0"}),
                ],
            ),

            # Answer display
            html.Div(
                style={
                    "backgroundColor": "#ffffff",
                    "borderRadius": "12px",
                    "padding": "30px",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
                },
                children=[
                    html.H4("💡 AI Answer:", style={"color": "#2c3e50", "marginBottom": "20px"}),
                    dcc.Markdown(
                        answer,
                        style={
                            "fontSize": "16px",
                            "lineHeight": "1.6",
                            "color": "#34495e",
                        },
                    ),
                ],
            ),
        ])

        return results

    except Exception as e:
        return html.Div(
            style={
                "backgroundColor": "#f8d7da",
                "border": "1px solid #f5c6cb",
                "borderRadius": "8px",
                "padding": "20px",
                "color": "#721c24",
            },
            children=[
                html.Strong("❌ Error: "),
                html.Span(str(e)),
            ],
        )
