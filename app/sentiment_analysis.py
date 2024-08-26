import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import numpy as np

# Initialize the NLTK sentiment analyzer
sia = SentimentIntensityAnalyzer()



def analyze_sentiment(text):
    lines = text.split('\n')
    sentiments = []
    scores = []
    
    for line in lines:
        if line.strip():
            sentiment_scores = sia.polarity_scores(line)
            compound_score = sentiment_scores['compound']
            scores.append(compound_score)
            if compound_score >= 0.05:
                sentiments.append('POSITIVE')
            elif compound_score <= -0.05:
                sentiments.append('NEGATIVE')
            else:
                sentiments.append('NEUTRAL')
        else:
            sentiments.append('NEUTRAL')
            scores.append(0)
    
    # Overall sentiment
    overall_score = np.mean(scores)
    if overall_score >= 0.05:
        overall_sentiment = "Positive"
    elif overall_score <= -0.05:
        overall_sentiment = "Negative"
    else:
        overall_sentiment = "Neutral"
    
    # Sentiment distribution
    total_lines = len(sentiments)
    sentiment_dist = {
        "Positive": sum(1 for s in sentiments if s == 'POSITIVE') / total_lines * 100,
        "Negative": sum(1 for s in sentiments if s == 'NEGATIVE') / total_lines * 100,
        "Neutral": sum(1 for s in sentiments if s == 'NEUTRAL') / total_lines * 100
    }
    
    return {
        "sentiments": sentiments,
        "scores": scores,
        "overall_sentiment": overall_sentiment,
        "sentiment_distribution": sentiment_dist,
    }