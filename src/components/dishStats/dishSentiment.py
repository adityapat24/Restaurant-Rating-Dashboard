import plotly.express as px
import pandas as pd
from textblob import TextBlob

def create_dish_sentiment_chart(filtered_df, dish_name):
    if "content" not in filtered_df.columns or filtered_df["content"].isnull().all():
        return px.bar(title=f"No review text available for {dish_name}")

    filtered_df["sentiment"] = filtered_df["content"].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    sentiment_counts = pd.cut(
        filtered_df["sentiment"],
        bins=[-1, -0.2, 0.2, 1],
        labels=["Negative", "Neutral", "Positive"]
    ).value_counts().reindex(["Positive", "Neutral", "Negative"], fill_value=0)

    df = pd.DataFrame({"Sentiment": sentiment_counts.index, "Count": sentiment_counts.values})

    fig = px.bar(
        df,
        x="Sentiment",
        y="Count",
        color="Sentiment",
        color_discrete_map={"Positive": "#90EE90", "Neutral": "#FFD580", "Negative": "#FF9999"},
        text_auto=True,
        title=f"<b>Sentiment Distribution for {dish_name}</b><br><sup>How are customers feeling about this dish?</sup>",
    )
    fig.update_layout(title_x=0.5)
    return fig
