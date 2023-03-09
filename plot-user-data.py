import sqlite3
import pandas
import matplotlib
from matplotlib import pyplot as plt

def plot_average_sentiment(user_id):
    conn = sqlite3.connect("database.db")

    dataframe = pandas.read_sql_query("SELECT * from Comments Join Author on Comments.AuthorID = Author.AuthorID WHERE Comments.AuthorID = " + user_id + " AND Association != \"CONTRIBUTOR\" ORDER BY Timestamp", conn)
    cursor = conn.cursor()
    cursor.execute("SELECT Username from Author WHERE AuthorID = " + user_id)
    result = cursor.fetchone()

    username = result[0]

    x = dataframe["Timestamp"]
    y1 = dataframe["SentimentScore"]

    color = ['r' if value<0 else 'g' for value in y1]
    fig, ax1 = plt.subplots()
    color = ['r' if value<0 else 'g' for value in y1]
    ax1.bar(x, y1, color=color)
    plt.title("Average Review Comment Sentiment versus Time for " + username)
    plt.show()

def plot_sentiment_versus_author(author_id, reviewer_id):
    print("Do something")

def plot_stop_word_ratio_versus_time(user_id):
    conn = sqlite3.connect("database.db")

    dataframe = pandas.read_sql_query("SELECT * from Comments Join Author on Comments.AuthorID = Author.AuthorID WHERE Comments.AuthorID = " + user_id + " AND Association != \"CONTRIBUTOR\" ORDER BY Timestamp", conn)
    cursor = conn.cursor()
    cursor.execute("SELECT Username from Author WHERE AuthorID = " + user_id)
    result = cursor.fetchone()

    username = result[0]

    x = dataframe["Timestamp"]
    y1 = dataframe["StopWordRatio"]

    color = ['r' if value>0.4 else 'g' for value in y1]
    fig, ax1 = plt.subplots()
    ax1.bar(x, y1, color=color)
    plt.title("Stop Word Ratio versus Time for " + username)
    plt.show()

def plot_review_length(user_id):
    conn = sqlite3.connect("database.db")

    dataframe = pandas.read_sql_query("SELECT LENGTH(Comments.Body) AS CommentLength, Timestamp from Comments Join Author on Comments.AuthorID = Author.AuthorID WHERE Comments.AuthorID = " + user_id + " AND Association != \"CONTRIBUTOR\" ORDER BY Timestamp", conn)
    cursor = conn.cursor()
    cursor.execute("SELECT Username from Author WHERE AuthorID = " + user_id)
    result = cursor.fetchone()

    username = result[0]

    x = dataframe["Timestamp"]
    y1 = dataframe["CommentLength"]

    color = 'b'
    fig, ax1 = plt.subplots()
    ax1.bar(x, y1, color=color)
    plt.title("Review Comment Length versus Time for " + username)
    plt.show()

def plot_heatmap_sentiment():
    print("Do something")