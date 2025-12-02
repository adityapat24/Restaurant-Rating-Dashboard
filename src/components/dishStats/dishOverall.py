import plotly.express as px
import pandas as pd

def create_dish_overall_pie(filtered_df, dish_name):
    rating_counts = filtered_df["overall"].value_counts().sort_index()
    df = pd.DataFrame({"Rating": rating_counts.index, "Count": rating_counts.values})

    fig = px.pie(
        df,
        values="Count",
        names="Rating",
        color="Rating",
        title=f"<b>Overall Rating Distribution for {dish_name}</b><br><sup>What percentage of customers have given each rating?</sup>",
        color_discrete_map={1: "#ff4c4c", 2: "#ff9966", 3:"#ffcc66", 4: "#99cc66", 5:"#66cc66"},
    )
    fig.update_traces(textinfo="label+percent", pull=[0.05]*len(df))
    fig.update_layout(title_x=0.5, margin=dict(l=40, r=40, t=80, b=40))
    return fig
