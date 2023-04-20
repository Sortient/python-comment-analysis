import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import sys
import datetime

result_list = []
try:
    flag = sys.argv[1]
    id = sys.argv[2]
except:
    print("Unexpected variables. Format [flag] [id]")
    sys.exit(1)

if flag == "c":
    sql_statement01 = f"SELECT COUNT(*) FROM Comments WHERE ProjectID = {id}"
    sql_statement02 = f"SELECT COUNT(*) FROM Comments WHERE ProjectID = {id} AND SentimentScore < 0"
    sql_statement03 = f"SELECT AVG(SentimentScore) FROM Comments WHERE ProjectID = {id}"
    sql_statement04 = f"SELECT AVG(StopWordRatio) FROM Comments WHERE ProjectID = {id}"
    sql_statement05 = f"SELECT COUNT(*) FROM Comments WHERE ProjectID = {id} AND CodeSnippetCount > 0"
    sql_statement06 = f"SELECT ProjectURL FROM Project WHERE ProjectID = {id}"
elif flag == "a":
    sql_statement = "SELECT COUNT(*) as CommentCount FROM Comments WHERE AuthorID = " + id
else:
    print("Unknown flag")
    sys.exit(1)

now = datetime.datetime.now()
date_string = now.strftime("%Y-%m-%d_%H-%M-%S")

# Create filename
if flag == "c":
    filename = f"output/project-overall.txt"
elif flag == "a":
    filename = f"output/author-overall.txt"

with open(filename, 'a') as file:
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    try:
        c.execute(sql_statement06)
    except:
        print("SQL error")
        sys.exit(1)
    result = c.fetchone()
    project_url = result[0]
    try:
        c.execute(sql_statement01)
    except:
        print("SQL error")
        sys.exit(1)
    result = c.fetchone()
    total_comments = result[0]
    if flag == "c":
        file.write(f"Project {id}: {project_url}")
        output = "\nComment total: " + str(total_comments)
        #print(output)
        file.write(output)
    elif flag == "a":
        output = ("\nComment total: " + str(result[0]))
        #print(output)
        file.write(output)

    try:
        c.execute(sql_statement02)
    except:
        print("SQL error")
        sys.exit(1)
    result = c.fetchone()
    neg_comments = result[0]
    
    if total_comments != 0:
        pos_ratio = round((1 - (neg_comments / total_comments)) * 100, 1)
        
        output = ("\n" + str(pos_ratio) + "% of comments are positive")
        file.write(output)
        if flag == "c":
            try:
                c.execute(sql_statement03)
            except:
                print("SQL error")
                sys.exit(1)
            result = c.fetchone()
            average_sentiment = result[0]
            output = ("\nAverage sentiment: " + str(round(average_sentiment,4)))
            #print(output)
            file.write(output)
            try:
                c.execute(sql_statement04)
            except:
                print("SQL error")
                sys.exit(1)
            result = c.fetchone()
            avg_stop_word = result[0]
            output = "\nAverage stop word ratio: " + str(round(avg_stop_word,4))
            #print(output)
            file.write(output)
            try:
                c.execute(sql_statement05)
            except:
                print("SQL error")
                sys.exit(1)
            result = c.fetchone()
            code_snippet_count = result[0]
            code_snippet_ratio = (code_snippet_count / total_comments) * 100
            output = f"\nPercentage of comments containing code snippets: {str(round(code_snippet_ratio,2))}%\n\n"
            #print(output)
            file.write(output)
    conn.close()