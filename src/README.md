# Restaurant Analytics Dashboard

A Python Dash application for analyzing restaurant dish performance based on customer feedback.

## Features

- **Top & Bottom Rated Dishes**: Interactive tabs to view the best and worst performing dishes
- **Performance Scatter Plot**: Visualizes rating vs review count to identify high-impact problem areas
- **Weak Points Analysis**: Horizontal bar chart showing specific rating dimensions for underperforming dishes
- **Responsive Design**: Works on desktop and mobile devices

## Installation

1. Install Python 3.8 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python app.py
```

Then open your browser and navigate to:
```
http://localhost:8050
```

## Project Structure

```
.
├── app.py                    # Main application file
├── requirements.txt          # Python dependencies
├── data/
│   └── dishes.py            # Mock dish data and utility functions
├── components/
│   ├── dish_card.py         # Dish card component
│   └── charts.py            # Chart components (Plotly)
└── assets/
    └── styles.css           # CSS styling
```

## Data Model

Each dish contains:
- **id**: Unique identifier
- **name**: Dish name
- **price**: Price in dollars
- **ratings**: Object with three dimensions:
  - `taste`: Rating from 0-5
  - `texture`: Rating from 0-5
  - `bangForBuck`: Value rating from 0-5
- **reviewCount**: Number of customer reviews
- **image**: URL to dish image

## Key Metrics

- **Average Rating**: Calculated as the mean of taste, texture, and bang-for-buck ratings
- **Priority Level**: Based on rating and review count (lower rating + higher reviews = higher priority)

## Customization

### Adding More Dishes

Edit `/data/dishes.py` and add entries to the `dishes` list following the same structure.

### Changing Number of Displayed Dishes

In `app.py`, modify the count parameter:
```python
dishes = get_top_rated_dishes(5)  # Change 5 to desired number
```

### Styling

Modify `/assets/styles.css` to customize the appearance.

## Technologies Used

- **Dash**: Web application framework
- **Plotly**: Interactive charting library
- **Python**: Backend logic and data processing

## License

MIT License
