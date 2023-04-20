import sqlite3
import pandas
import matplotlib
from matplotlib import pyplot as plt
import datetime as dt
import os

min_interactions = 2
def plot_average_sentiment(user_id):
    output_dir = f"output/user/{user_id}"
    current_time = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    conn = sqlite3.connect("database.db")

    #dataframe = pandas.read_sql_query(f"SELECT * from Comments Join Author on Comments.AuthorID = Author.AuthorID WHERE Comments.AuthorID = {user_id} GROUP BY Comments.AuthorID HAVING COUNT(*) >= {min_interactions} ORDER BY Timestamp", conn)
    dataframe = pandas.read_sql_query(f"SELECT * from Comments Join Author on Comments.AuthorID = Author.AuthorID WHERE Comments.AuthorID = {user_id} ORDER BY Timestamp", conn)
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
    plt.savefig(f"{output_dir}/{user_id}_avg_sentiment_{current_time}.png")
    plt.clf()

def plot_sentiment_versus_author(author_id, reviewer_id):
    print("Do something")

def plot_stop_word_ratio_versus_time(user_id):
    output_dir = f"output/user/{user_id}"
    current_time = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    conn = sqlite3.connect("database.db")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    dataframe = pandas.read_sql_query(f"SELECT * from Comments Join Author on Comments.AuthorID = Author.AuthorID WHERE Comments.AuthorID = {user_id} ORDER BY Timestamp", conn)
    cursor = conn.cursor()
    cursor.execute("SELECT Username from Author WHERE AuthorID = " + user_id)
    result = cursor.fetchone()

    username = result[0]

    x = dataframe["Timestamp"]
    y1 = dataframe["StopWordRatio"]

    color = ['r' if value>0.8 else 'g' for value in y1]
    fig, ax1 = plt.subplots()
    ax1.bar(x, y1, color=color)
    plt.title("Stop Word Ratio versus Time for " + username)
    plt.savefig(f"{output_dir}/{user_id}_stop_word_ratio_vs_time_{current_time}.png")
    plt.clf()

def plot_review_length(user_id):
    output_dir = f"output/user/{user_id}"
    current_time = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    conn = sqlite3.connect("database.db")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    dataframe = pandas.read_sql_query(f"SELECT LENGTH(Comments.Body) AS CommentLength, Timestamp from Comments Join Author on Comments.AuthorID = Author.AuthorID WHERE Comments.AuthorID = {user_id} ORDER BY Timestamp", conn)
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
    plt.savefig(f"{output_dir}/{user_id}_comment_length_vs_time_{current_time}.png")
    plt.clf()
def plot_code_snippet_count(user_id):
    output_dir = f"output/user/{user_id}"
    current_time = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    conn = sqlite3.connect("database.db")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    dataframe = pandas.read_sql_query(f"SELECT CodeSnippetCount, Timestamp from Comments Join Author on Comments.AuthorID = Author.AuthorID WHERE Comments.AuthorID = {user_id} ORDER BY Timestamp", conn)
    cursor = conn.cursor()
    cursor.execute("SELECT Username from Author WHERE AuthorID = " + user_id)
    result = cursor.fetchone()

    username = result[0]

    x = dataframe["Timestamp"]
    y1 = dataframe["CodeSnippetCount"]

    color = 'b'
    fig, ax1 = plt.subplots()
    ax1.bar(x, y1, color=color)
    plt.title("Code Snippet Count vs Time For " + username)
    plt.savefig(f"{output_dir}/{user_id}_code_snippet_count_vs_time_{current_time}.png")
    plt.clf()

def plot_heatmap_sentiment():
    print("Do something")