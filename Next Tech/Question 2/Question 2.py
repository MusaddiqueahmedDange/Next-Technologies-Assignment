import pandas as pd
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()


data = pd.read_csv("./chrome_reviews.csv")

review_text = list(data['Text'])

review_star = list(data['Star'])

for i,j in zip(review_text, review_star):
    polarity  = sia.polarity_scores(i)['compound']
    neutral = sia.polarity_scores(i)['neu']
    positive = sia.polarity_scores(i)['pos']
    negative = sia.polarity_scores(i)['neg']
    if polarity <= 0.0 and negative > neutral and j > 3:
        print(sia.polarity_scores(i),i, j)
    elif polarity >= 0.0 and positive > neutral and j < 2:
        print(sia.polarity_scores(i),i, j)
    
    