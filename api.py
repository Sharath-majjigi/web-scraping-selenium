from flask import Flask, request, jsonify
from textblob import TextBlob
import sqlite3
app = Flask(__name__)

# Sentiment Analysis API
@app.route('/sentiment_analysis', methods=['POST'])
def sentiment_analysis():
    review = request.json['review']
    blob = TextBlob(review)
    sentiment = blob.sentiment.polarity
    return jsonify({'sentiment': sentiment})

# Review Retrieval API
@app.route('/review_retrieval', methods=['GET'])
def review_retrieval():
    conn = sqlite3.connect('iphone_12_reviews.db')
    color = request.args.get('color')
    rating = request.args.get('rating')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM iphone_reviews WHERE color=? and rating=?',(color),(rating))
    reviews = cursor.fetchall()
    conn.close()
    # code for fetching reviews goes here
    return jsonify({'reviews': reviews})

if __name__ == '__main__':
    app.run(debug=True)