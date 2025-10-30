"""
Chart components using Plotly
"""

import plotly.graph_objects as go
from data.dishes import (
    get_all_dishes,
    get_bottom_rated_dishes,
    calculate_average_rating
)


def create_performance_chart():
    """
    Create a scatter plot showing rating vs review count
    """
    dishes = get_all_dishes()
    
    # Prepare data
    names = []
    ratings = []
    reviews = []
    colors = []
    
    for dish in dishes:
        avg_rating = calculate_average_rating(dish)
        names.append(dish["name"])
        ratings.append(avg_rating)
        reviews.append(dish["reviewCount"])
        
        # Color coding based on rating
        if avg_rating < 3.5:
            colors.append("#ef4444")  # Red
        elif avg_rating < 4.2:
            colors.append("#f59e0b")  # Amber
        else:
            colors.append("#10b981")  # Green
    
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


def create_weak_points_chart():
    """
    Create a horizontal bar chart showing rating breakdown for bottom dishes
    """
    bottom_dishes = get_bottom_rated_dishes(7)
    
    # Prepare data
    dish_names = []
    taste_ratings = []
    texture_ratings = []
    bang_for_buck_ratings = []
    
    for dish in bottom_dishes:
        # Truncate long names
        name = dish["name"]
        if len(name) > 15:
            name = name[:15] + "..."
        dish_names.append(name)
        
        taste_ratings.append(dish["ratings"]["taste"])
        texture_ratings.append(dish["ratings"]["texture"])
        bang_for_buck_ratings.append(dish["ratings"]["bangForBuck"])
    
    # Create figure
    fig = go.Figure()
    
    # Add bars for each rating dimension
    fig.add_trace(go.Bar(
        y=dish_names,
        x=taste_ratings,
        name='Taste',
        orientation='h',
        marker=dict(color='#ef4444')
    ))
    
    fig.add_trace(go.Bar(
        y=dish_names,
        x=texture_ratings,
        name='Texture',
        orientation='h',
        marker=dict(color='#3b82f6')
    ))
    
    fig.add_trace(go.Bar(
        y=dish_names,
        x=bang_for_buck_ratings,
        name='Bang for Buck',
        orientation='h',
        marker=dict(color='#10b981')
    ))
    
    # Update layout
    fig.update_layout(
        title={
            'text': 'Rating Breakdown: Dishes Needing Attention',
            'font': {'size': 18, 'color': '#1f2937'}
        },
        xaxis_title='Rating',
        xaxis=dict(range=[0, 5]),
        barmode='group',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12, color='#4b5563'),
        height=400,
        margin=dict(l=140, r=30, t=80, b=60),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        annotations=[
            dict(
                text='Identify which specific aspects need improvement',
                xref='paper',
                yref='paper',
                x=0,
                y=1.15,
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
        showgrid=False,
        zeroline=False
    )
    
    return fig
