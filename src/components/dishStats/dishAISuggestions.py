import os
import json
import google.generativeai as genai
import pandas as pd


def generate_dish_suggestions(dish_name, reviews_df, api_key=None):
    """
    Generate 3 AI-powered suggestions for improving a dish based on reviews and comments.
    
    Args:
        dish_name: Name of the dish
        reviews_df: DataFrame with review data (must include 'content' column from merged data)
        api_key: Gemini API key (defaults to env variable if not provided)
    
    Returns:
        List of 3 suggestion dictionaries with keys: 'title', 'description', 'category'
    """
    # Get API key
    if api_key is None:
        api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        return [
            {
                "title": "API Key Required",
                "description": "Please set GEMINI_API_KEY environment variable to get AI suggestions.",
                "category": "error"
            }
        ]
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    # Prepare review comments (column is 'content' not 'comment')
    if reviews_df.empty or 'content' not in reviews_df.columns:
        return [
            {
                "title": "No Reviews Available",
                "description": "This dish doesn't have enough review data to generate suggestions.",
                "category": "info"
            }
        ]
    
    # Get all comments for the dish
    comments = reviews_df['content'].dropna().tolist()
    
    if not comments:
        return [
            {
                "title": "No Comments Available",
                "description": "This dish has reviews but no written comments to analyze.",
                "category": "info"
            }
        ]
    
    # Prepare the prompt with review comments
    comments_text = "\n".join([f"- {comment}" for comment in comments[:50]])  # Limit to 50 most recent
    
    prompt = f"""You are a restaurant consultant analyzing customer feedback for a dish called "{dish_name}".

Based on the following customer comments, provide EXACTLY 3 actionable suggestions to improve the dish's performance.

Customer Comments:
{comments_text}

Return your response as a valid JSON array with exactly 3 objects. Each object must have:
- "title": A short, specific action (3-8 words, e.g., "Reduce salt level", "Offer customizable toppings")
- "description": A brief explanation of why this will help (15-30 words)
- "category": One of ["recipe", "pricing", "portion", "service", "marketing", "menu"]

Example format:
[
  {{
    "title": "Reduce salt level",
    "description": "Multiple customers mentioned the dish is too salty. Reducing sodium by 15-20% could improve satisfaction.",
    "category": "recipe"
  }},
  {{
    "title": "Keep price the same, monitor results",
    "description": "Current pricing appears appropriate based on customer value perception. Monitor for 2-3 months.",
    "category": "pricing"
  }},
  {{
    "title": "Add portion size option",
    "description": "Some customers want smaller portions. Offer a half-size option at reduced price.",
    "category": "portion"
  }}
]

Requirements:
- Respond with ONLY the JSON array, no other text
- Exactly 3 suggestions
- Be specific and actionable
- Base suggestions on the actual customer comments provided
- If comments are mostly positive, suggest ways to maintain or enhance success
"""
    
    try:
        # Call Gemini API
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```"):
            response_text = response_text.split("\n", 1)[1] if "\n" in response_text else response_text[3:]
            response_text = response_text.rsplit("```", 1)[0].strip()
        
        # Parse JSON response
        suggestions = json.loads(response_text)
        
        # Validate structure
        if not isinstance(suggestions, list) or len(suggestions) != 3:
            raise ValueError("Response must be a list of exactly 3 suggestions")
        
        for suggestion in suggestions:
            if not all(key in suggestion for key in ["title", "description", "category"]):
                raise ValueError("Each suggestion must have title, description, and category")
        
        return suggestions
    
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Response text: {response_text}")
        return [
            {
                "title": "Unable to Parse AI Response",
                "description": "The AI returned an invalid format. Please try again.",
                "category": "error"
            }
        ]
    except Exception as e:
        print(f"Error generating suggestions: {e}")
        return [
            {
                "title": "Error Generating Suggestions",
                "description": f"An error occurred: {str(e)}",
                "category": "error"
            }
        ]


def create_suggestion_card(suggestion, index):
    """
    Create a visual card component for a single suggestion.
    
    Args:
        suggestion: Dictionary with 'title', 'description', 'category'
        index: Suggestion number (1, 2, or 3)
    
    Returns:
        Dash HTML component
    """
    from dash import html
    
    # Category icons and colors
    category_config = {
        "recipe": {"icon": "🍳", "color": "#e74c3c"},
        "pricing": {"icon": "💰", "color": "#27ae60"},
        "portion": {"icon": "📏", "color": "#3498db"},
        "service": {"icon": "🛎️", "color": "#9b59b6"},
        "marketing": {"icon": "📣", "color": "#f39c12"},
        "menu": {"icon": "📋", "color": "#34495e"},
        "error": {"icon": "⚠️", "color": "#95a5a6"},
        "info": {"icon": "ℹ️", "color": "#3498db"}
    }
    
    category = suggestion.get("category", "info")
    config = category_config.get(category, category_config["info"])
    
    return html.Div(
        style={
            "backgroundColor": "#ffffff",
            "borderRadius": "12px",
            "padding": "25px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
            "border": f"3px solid {config['color']}",
            "height": "100%",
            "display": "flex",
            "flexDirection": "column",
        },
        children=[
            # Header with number and icon
            html.Div(
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "marginBottom": "15px",
                },
                children=[
                    html.Div(
                        str(index),
                        style={
                            "backgroundColor": config["color"],
                            "color": "white",
                            "borderRadius": "50%",
                            "width": "35px",
                            "height": "35px",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "fontSize": "18px",
                            "fontWeight": "bold",
                            "marginRight": "12px",
                        }
                    ),
                    html.Span(
                        config["icon"],
                        style={"fontSize": "24px", "marginRight": "10px"}
                    ),
                    html.Span(
                        category.upper(),
                        style={
                            "fontSize": "12px",
                            "fontWeight": "600",
                            "color": config["color"],
                            "letterSpacing": "0.5px",
                        }
                    ),
                ],
            ),
            
            # Title
            html.H4(
                suggestion["title"],
                style={
                    "color": "#2c3e50",
                    "marginBottom": "12px",
                    "fontSize": "18px",
                    "fontWeight": "600",
                    "lineHeight": "1.4",
                }
            ),
            
            # Description
            html.P(
                suggestion["description"],
                style={
                    "color": "#555",
                    "fontSize": "15px",
                    "lineHeight": "1.6",
                    "marginBottom": "0",
                    "flex": "1",
                }
            ),
        ]
    )
