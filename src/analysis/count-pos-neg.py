import sqlite3
import sys
import nltk
import datetime
import os
from nltk.sentiment import SentimentIntensityAnalyzer
#nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()
#project_id = sys.argv[1]
#positive = sys.argv[2].lower() in ['pos', 'p', 'positive', 'y', 'yes']
conn = sqlite3.connect('database.db')
c = conn.cursor()
project_id = sys.argv[1]

#if positive:
sql_statement = f"SELECT CommentID, Body, SentimentScore FROM Comments WHERE ProjectID = {project_id}"#WHERE SentimentScore > -1 AND ProjectID = {project_id}"
#else:
#    sql_statement = f"SELECT CommentID, Body, SentimentScore FROM Comments WHERE SentimentScore < 0 AND ProjectID = {project_id}"
try:
    c.execute(sql_statement)
except Exception as e:
    print("WARNING: unable to complete this request.")
    print(e)
    sys.exit(1)

rows = c.fetchall()
pos_words = []
neg_words = []
for row in rows:
    body = row[1]
    words = nltk.word_tokenize(body.lower())
    for word in words:
    #if word not in pos_words and word not in neg_words:
        score = sia.polarity_scores(word)
        if score['compound'] > 0:
            pos_words.append(word)
        elif score['compound'] < 0:
            neg_words.append(word)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
directory = f"output/sentiment"
if not os.path.exists(directory):
    os.makedirs(directory)
pos_filename = f"{directory}/positive_words.txt"
neg_filename = f"{directory}/negative_words.txt"

positive_words = str.replace(str(pos_words), '[', '')
positive_words = str.replace(positive_words, ']', '')
positive_words = str.replace(positive_words, '\'', '')
positive_words = str.replace(positive_words, ',', '')

negative_words = str.replace(str(neg_words), '[', '')
negative_words = str.replace(negative_words, ']', '')
negative_words = str.replace(negative_words, '\'', '')
negative_words = str.replace(negative_words, ',', '')

#if positive:
with open(pos_filename, "a") as file:
    #file.write(f"Comment ID\tComment Body\tSentiment Score\n")
    #for row in rows:
    #    file.write(f"{row[0]}\t{row[1]}\t{row[2]}\n")

    #file.write("\nOverall Feedback:\n")
    file.write(f"{positive_words}\n")
    #file.write(f"Negative words used: {neg_words}\n")
    #if neg_words != []:
    #    file.write("\nConsider focusing your attention to using more instances of positive language in your review comments.")
#else:
with open(neg_filename, "a") as file:
    #file.write(f"Comment ID\tComment Body\tSentiment Score\n")
    #for row in rows:
    #    file.write(f"{row[0]}\t{row[1]}\t{row[2]}\n")

    #file.write("\nOverall Feedback:\n")
    file.write(f"{negative_words}\n")
        #file.write(f"Negative words used: {neg_words}\n")
        #if neg_words != []:
        #    file.write("\nConsider focusing your attention to using more instances of positive language in your review comments.")
    
c.close()
conn.close()
