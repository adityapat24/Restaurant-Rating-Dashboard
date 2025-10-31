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

def create_histogram_price_ranges():
    """
    Create a grouped bar chart (histogram-like) that buckets dishes by price range
    and shows average Overall, Taste, Texture and Bang for Buck ratings per bucket.
    """
    dishes = get_all_dishes()

    # Determine buckets (0 to max price)
    prices = [d["price"] for d in dishes]
    max_price = max(prices) if prices else 0
    min_price = 0
    bucket_count = 5
    bucket_width = (max_price - min_price) / bucket_count if max_price - min_price > 0 else 1

    # Initialize accumulators
    accum = []
    for i in range(bucket_count):
        lower = min_price + i * bucket_width
        upper = min_price + (i + 1) * bucket_width if i < bucket_count - 1 else max_price
        label = f"${int(round(lower))} - ${int(round(upper))}"
        accum.append({
            "label": label,
            "overall_sum": 0.0,
            "taste_sum": 0.0,
            "texture_sum": 0.0,
            "bang_sum": 0.0,
            "count": 0,
        })

    # Aggregate
    for dish in dishes:
        price = dish.get("price", 0)
        # ensure index in range
        idx = int((price - min_price) / bucket_width) if bucket_width > 0 else 0
        if idx < 0:
            idx = 0
        if idx >= bucket_count:
            idx = bucket_count - 1

        overall = calculate_average_rating(dish)
        accum[idx]["overall_sum"] += overall
        accum[idx]["taste_sum"] += dish["ratings"]["taste"]
        accum[idx]["texture_sum"] += dish["ratings"]["texture"]
        accum[idx]["bang_sum"] += dish["ratings"]["bangForBuck"]
        accum[idx]["count"] += 1

    # Build chart arrays
    labels = []
    overall_avgs = []
    taste_avgs = []
    texture_avgs = []
    bang_avgs = []

    for a in accum:
        labels.append(a["label"])
        c = a["count"] or 0
        overall_avgs.append(round(a["overall_sum"] / c, 2) if c else 0)
        taste_avgs.append(round(a["taste_sum"] / c, 2) if c else 0)
        texture_avgs.append(round(a["texture_sum"] / c, 2) if c else 0)
        bang_avgs.append(round(a["bang_sum"] / c, 2) if c else 0)

    # Create figure with grouped bars
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=labels,
        y=overall_avgs,
        name='Overall',
        marker=dict(color='#7c3aed')
    ))

    fig.add_trace(go.Bar(
        x=labels,
        y=taste_avgs,
        name='Taste',
        marker=dict(color='#ef4444')
    ))

    fig.add_trace(go.Bar(
        x=labels,
        y=texture_avgs,
        name='Texture',
        marker=dict(color='#3b82f6')
    ))

    fig.add_trace(go.Bar(
        x=labels,
        y=bang_avgs,
        name='Bang for Buck',
        marker=dict(color='#10b981')
    ))

    fig.update_layout(
        title={
            'text': 'Ratings by Price Range',
            'font': {'size': 18, 'color': '#1f2937'}
        },
        xaxis_title='Price Range',
        yaxis_title='Average Rating',
        yaxis=dict(range=[0, 5]),
        barmode='group',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12, color='#4b5563'),
        height=420,
        margin=dict(l=60, r=30, t=80, b=80),
        annotations=[
            dict(
                text='Stats for different price buckets',
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

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='#e5e7eb')

    return fig

    