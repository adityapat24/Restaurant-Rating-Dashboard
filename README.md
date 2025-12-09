# Restaurant Analytics Dashboard

A Python Dash application for analyzing restaurant dish performance based on customer feedback.

## Features

<<<<<<< Updated upstream
## Installation

1. Install Python 3.8 or higher

=======
- **Top & Bottom Rated Dishes**: Interactive tabs to view the best and worst performing dishes
- **Performance Scatter Plot**: Visualizes rating vs review count to identify high-impact problem areas
- **Weak Points Analysis**: Horizontal bar chart showing specific rating dimensions for underperforming dishes
- **Responsive Design**: Works on desktop and mobile devices

## Installation

1. Install Python 3.8 or higher

>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
=======
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

## Data Structure

The JSON file (`mockData.json`) contains five main collections that are related through foreign keys:

### 1. **reviewers** (355 entries)
Anonymous customer identifiers.

**Schema:**
```json
{
  "id": number  // Unique reviewer identifier (1-355)
}
```

**Purpose:** Represents individual customers who have left reviews. Each reviewer can leave multiple reviews over time.

---

### 2. **menuItems** (25 entries)
Restaurant menu items across various categories.

**Schema:**
```json
{
  "id": number,    // Unique menu item identifier (1-25)
  "name": string   // Display name of the dish
}
```
---

### 3. **ratings** (769 entries)
Numerical ratings across multiple dimensions.

**Schema:**
```json
{
  "id": number,       // Unique rating identifier (1-769)
  "portion": number,  // Portion size rating (1-5)
  "taste": number,    // Taste/flavor rating (1-5)
  "value": number,    // Value for money rating (1-5)
  "overall": number,  // Overall satisfaction rating (1-5)
  "return": boolean   // Whether customer would return (true/false)
}
```

**Rating Scale:** 1 (Poor) to 5 (Excellent)

**Metrics:**
- **portion:** How customers perceive the serving size
- **taste:** Quality and flavor of the food
- **value:** Price-to-quality ratio
- **overall:** Holistic satisfaction score
- **return:** Customer loyalty indicator

**Distribution:**
- Ratings range from 1 (very negative) to 5 (very positive)
- The `return` field correlates with overall rating (typically true for ratings ≥4, false for ratings ≤2)

---

### 4. **content** (769 entries)
Written customer reviews and comments.

**Schema:**
```json
{
  "id": number,      // Unique content identifier (1-769)
  "content": string  // Customer's written review text
}
```

**Characteristics:**
- Natural language reviews reflecting the numerical ratings
- Comments mention specific aspects: portion size, taste, value, freshness, quality
- Length varies from brief (20 words) to detailed (50+ words)
- Tone correlates with ratings:
  - **High ratings (4-5):** Positive language ("amazing," "delicious," "highly recommend")
  - **Low ratings (1-2):** Negative language ("disappointed," "overpriced," "bland")
  - **Medium ratings (3):** Neutral language ("decent," "okay," "average")

**Example Reviews:**
```
"WOW! The BBQ chicken pizza is absolutely amazing. Huge portion, incredible flavor, 
and the price is unbeatable. Best pizza I've had in ages. Will definitely be back!"
```

```
"The pepperoni pizza was disappointing honestly. The portion was really small for 
the price and the taste was just meh. Not worth it in my opinion."
```

---

### 5. **reviews** (769 entries)
The main table that links all other tables together.

**Schema:**
```json
{
  "id": number,            // Unique review identifier (1-769)
  "rating_id": number,     // Foreign key → ratings.id
  "content_id": number,    // Foreign key → content.id
  "reviewer_id": number,   // Foreign key → reviewers.id
  "timestamp": string,     // Review date in "M/D/YYYY" format
  "menu_item_id": number   // Foreign key → menuItems.id
}
```

**Relationships:**
- Each review connects a specific reviewer to a menu item
- Each review has exactly one rating record and one content record
- Reviews span from August 2023 to present (December 2025)
- Timestamps are distributed across months to simulate realistic review patterns

---

## Data Relationships (Entity-Relationship Diagram)

```
┌──────────────┐
│  reviewers   │
│  (355)       │
└──────┬───────┘
       │
       │ reviewer_id
       ↓
┌──────────────┐      rating_id     ┌──────────────┐
│   reviews    │─────────────────────→   ratings    │
│   (769)      │                     │   (769)      │
│              │      content_id     ├──────────────┤
│              │─────────────────────→   content    │
└──────┬───────┘                     │   (769)      │
       │                             └──────────────┘
       │ menu_item_id
       ↓
┌──────────────┐
│  menuItems   │
│  (25)        │
└──────────────┘
```

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
>>>>>>> Stashed changes
