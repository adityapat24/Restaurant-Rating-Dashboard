import plotly.express as px
import pandas as pd

def create_dish_category_breakdown(filtered_df, dish_name):
    means = {
        "Taste": filtered_df["taste"].mean(),
        "Portion": filtered_df["portion"].mean(),
        "Value": filtered_df["value"].mean(),
        "Overall": filtered_df["overall"].mean(),
    }

    df = pd.DataFrame({"Category": means.keys(), "Average Rating": means.values()})

    fig = px.bar(
        df,
        x="Category",
        y="Average Rating",
        text_auto=".2f",
        color="Category",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title=f"Average Ratings Breakdown for {dish_name}",
    )
    fig.update_layout(title_x=0.5, yaxis_range=[0, 5])
    return fig
