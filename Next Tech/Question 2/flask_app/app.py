from flask import Flask, render_template, request
import os
import pandas as pd
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

app = Flask(__name__)
UPLOAD_FOLDER = './static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                if uploaded_file.filename.split('.')[1] == 'csv':
                    uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename))
                    data = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename))
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename))
                    review_text = list(data['Text'])

                    review_star = list(data['Star'])

                    result = []
                    for i,j in zip(review_text, review_star):
                        if type(i) == str:
                            sentiment = sia.polarity_scores(i)
                            polarity  = sentiment['compound']
                            neutral = sentiment['neu']
                            positive = sentiment['pos']
                            negative = sentiment['neg']
                            if polarity <= 0.0 and negative > neutral and j > 3:
                                #print(sia.polarity_scores(i),i, j)
                                result.append([i,j])
                            elif polarity >= 0.0 and positive > neutral and j < 2:
                                #print(sia.polarity_scores(i),i, j)
                                result.append([i,j])
                    
                    context = {
                        "result" : result
                    }
                    return render_template("home.html", context=context)

                else:
                    context = {
                        "error" : "Upload Only CSV File"
                    }
                    return render_template("home.html", context=context)
    
            
    return render_template("home.html")




if __name__ == "__main__":
    app.run()