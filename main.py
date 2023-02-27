import retrievejson as rj
import sqlite3
import plotdata as pd
import pandas

#rj.retrieve_eclipse_cdt_pull_comments()

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

selected_id = int(input("Enter ID:"))

cursor.execute('SELECT AuthorID FROM Author')

author_ids = [row[0] for row in cursor.fetchall()]

cursor.close()
conn.close()
if selected_id in author_ids:
#for id in author_ids:
    pd.plot_average_sentiment(str(selected_id))
    pd.plot_stop_word_ratio_versus_time(str(selected_id))
    pd.plot_review_length(str(selected_id))
else:
    print("Selected ID not found")
