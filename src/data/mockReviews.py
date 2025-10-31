"""
mockReviews.py
Generates mock restaurant reviews and visualizations for the dashboard.
"""

import random
from datetime import datetime, timedelta
import pandas as pd
from faker import Faker
import plotly.express as px

# ------------------------------
# Generate Mock Review Data
# ------------------------------

fake = Faker()
random.seed(42)
Faker.seed(42)

dishes = [
    "Margherita Pizza", "Truffle Pasta", "Spicy Tuna Roll", "Caesar Salad",
    "BBQ Burger", "Avocado Toast", "Lobster Bisque", "Chicken Tikka Masala",
    "Chocolate Lava Cake", "Sushi Platter", "Steak Frites", "Vegan Bowl"
]


def generate_mock_reviews(n=150):
    """Generate a DataFrame of fake reviews."""
    reviews = []
    for _ in range(n):
        dish = random.choice(dishes)
        overall = random.randint(3, 5)
        taste = random.randint(2, 5)
        texture = random.randint(2, 5)
        portion = random.randint(2, 5)
        text = fake.sentence(nb_words=random.randint(10, 20))
        days_ago = random.randint(0, 3 * 365)
        date = datetime.now() - timedelta(days=days_ago)

        reviews.append({
            "Dish": dish,
            "Overall Rating": overall,
            "Taste Rating": taste,
            "Texture Rating": texture,
            "Price-to-Portion Rating": portion,
            "Review Text": text,
            "Date": date
        })
    return pd.DataFrame(reviews)