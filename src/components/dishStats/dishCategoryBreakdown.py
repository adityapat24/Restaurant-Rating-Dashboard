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

        # Define a function to assign colors based on value
    def get_bar_colors(values):
        colors = []
        for val in values:
            if val >= 4:
                colors.append("#66cc66") 
            elif val >= 3:
                colors.append("#99cc66")  
            elif val >= 2:
                colors.append("#ffcc66")
            elif val >= 1:
                colors.append("#ff9966")
            else:
                colors.append("#ff4c4c") 
        return colors

    # Get the custom colors
    custom_colors = get_bar_colors(df['Average Rating'])

    fig = px.bar(
        df,
        x="Category",
        y="Average Rating",
        text_auto=".2f",
        color="Category",
        color_discrete_sequence=custom_colors,
        title=f"<b>Average Ratings Breakdown for {dish_name}</b><br><sup>What is the average rating for each category?</sup>",
    )
    fig.update_layout(title_x=0.5, yaxis_range=[0, 5])
    return fig
