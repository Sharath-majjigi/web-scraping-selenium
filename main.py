import requests
from bs4 import BeautifulSoup
import sqlite3
from textblob import TextBlob
from sqlalchemy import Column, Integer, String, Boolean, Float, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import sessionmaker
import random
from flask import Flask


# Open connection to SQLite database
conn = sqlite3.connect('iphone_12_reviews.db')
engine = create_engine('sqlite:///iphone_12_reviews.db')
Session = sessionmaker(bind=engine)
session = Session()
c = conn.cursor()

Base = declarative_base()

class Review(Base):
    __tablename__ = 'iphone_reviews'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)
    style_name = Column(String)
    color = Column(String)
    verified_purchase = Column(Boolean)
    rating =Column(String)
    sentiment_score = Column(Float)

    def __repr__(self):
        return f"<Review(title='{self.title}', sentiment_score={self.sentiment_score})>"

# Create the database tables
Base.metadata.create_all(engine)

# Create table to store reviews (if it doesn't exist)
c.execute('''CREATE TABLE IF NOT EXISTS iphone_reviews_1
             (id int,title text, text text, style_name text, color text, verified_purchase bool, rating text, sentiment_score float)''')


base_url = 'https://www.amazon.in/Apple-New-iPhone-12-128GB/product-reviews/B08L5TNJHG/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

for page_num in range(1, 6):
    url = base_url + f'?pageNumber={page_num}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    reviews = soup.find_all('div', {'data-hook': 'review'})
    
    for review in reviews:
        title = review.find('a', {'data-hook': 'review-title'}).text.strip()
        text = review.find('span', {'data-hook': 'review-body'}).text.strip()
        
       # Find style name and color
        style_name_tag = review.find('a', {'data-hook': 'format-strip'})
        if style_name_tag:
            style_name = style_name_tag.text.strip()
        else:
            style_name = ''

        color_tag = review.find('a', {'data-hook': 'format-strip'})
        if color_tag is not None:
            color_span = color_tag.find('span', {'class': 'a-size-mini a-color-state a-text-bold'})
            if color_span is not None:
               color = color_span.text.strip()
            else:
               color = "NA"
        else:
            color = "NA"

        rating_tag = review.find('i', {'data-hook': 'review-star-rating'})
        if rating_tag:
            rating = float(rating_tag.text.split()[0])
        else:
             rating = None

        
        verified_purchase = 'Verified Purchase' in review.find('span', {'data-hook': 'avp-badge'}).text.strip()
        text = review.text
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity

        id = random.randint(1, 100)


        # Insert data into database
        c.execute("INSERT INTO iphone_reviews_1 VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (id,title, text, style_name, color, verified_purchase,rating,sentiment_score))

    # commit the changes to the database after each page
    conn.commit()   

session.commit()



