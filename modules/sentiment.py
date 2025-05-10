from textblob import TextBlob
from typing import Literal

def analyze_sentiment(text: str) -> Literal["Negative", "Neutral", "Positive"]:
    """
    Analyzes the sentiment of the given text and categorizes it as Negative, Neutral, or Positive.

    Args:
        text (str): The input text to analyze.

    Returns:
        Literal["Negative", "Neutral", "Positive"]: The sentiment category.
    """
    try:
        polarity = TextBlob(text).sentiment.polarity
        if polarity < -0.1:
            return "Negative"
        elif polarity > 0.1:
            return "Positive"
        else:
            return "Neutral"
    except Exception as e:
        raise ValueError(f"Error analyzing sentiment: {e}")
