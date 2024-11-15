import sqlite3
import sys
import pandas as pd
import sentiment_analysis as sa
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize

conn = sqlite3.connect('database.db')
author_id = sys.argv[1]
reviewer_id = sys.argv[2]
c = conn.cursor()

sql_statement = f"SELECT Comments.AuthorID AS 'Reviewer ID', PullRequests.AuthorID AS 'Author ID', Body, SentimentScore, CommentID FROM Comments INNER JOIN PullRequests ON PullRequests.RequestID = Comments.RequestID WHERE Comments.AuthorID != PullRequests.AuthorID AND PullRequests.AuthorID = {author_id} AND Comments.AuthorID = {reviewer_id} AND SentimentScore < 0"
c.execute(sql_statement)
sia = SentimentIntensityAnalyzer()
for row in c.fetchall():
    print(f"Comment ID: {row[4]} Reviewer ID: {row[0]} Author ID: {row[1]} Sentiment: {row[3]}")
    body = row[2]
    sentences = sent_tokenize(body)
    for sentence in sentences:
        print(sentence)
        print(sia.polarity_scores(sentence))
    print("\n")