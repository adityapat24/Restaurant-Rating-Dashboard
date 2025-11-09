import plotly.express as px
import pandas as pd

def create_dish_overall_pie(filtered_df, dish_name):
    rating_counts = filtered_df["overall"].value_counts().sort_index()
    df = pd.DataFrame({"Rating": rating_counts.index, "Count": rating_counts.values})

    fig = px.pie(
        df,
        values="Count",
        names="Rating",
        title=f"Overall Rating Distribution for {dish_name}",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig.update_traces(textinfo="label+percent", pull=[0.05]*len(df))
    fig.update_layout(title_x=0.5, margin=dict(l=40, r=40, t=80, b=40))
    return fig
