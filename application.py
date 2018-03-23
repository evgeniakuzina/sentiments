from flask import Flask, redirect, render_template, request, url_for

import helpers
from analyzer import Analyzer
import nltk
from nltk.tokenize import TweetTokenizer
import os
import sys

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name)

    # TODO
    if tweets is None:
        print('It is not possible to load timeline')
        sys.exit(1)
    
    tokenizer = nltk.tokenize.TweetTokenizer(preserve_case=False)
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")
    analyzer = Analyzer(positives, negatives)
    positive = 0.0
    negative = 0.0 
    neutral = 0.0
    
    for tweet in tweets:
        tokens = tokenizer.tokenize(tweet)
        positive_score = 0
        negative_score = 0
        for token in tokens:
            score = analyzer.analyze(token)
            if score > 0.0:
                positive_score +=1
            if score < 0.0:
                negative_score -=1
        score = positive_score+negative_score
        if score > 0.0:
            positive +=1
        if score < 0.0:
            negative +=1
        else:
            neutral +=1
    print(positive, negative, neutral)    
        
    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
