import requests
import sqlite3
import json
import re
import sentiment_analysis
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer

debug = True
#for pull_request_number in range(1,100):
def retrieve_eclipse_cdt_pull_comments(url, id):
    # "https://api.github.com/repos/eclipse-cdt/cdt/issues"
    repo_url = url
    project_id = id
    auth_token = "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"
    headers = {
        "Authorization": "token " + auth_token,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28" 
    }
    params = {
        "page": 1,
        "per_page": 1000
    }
    response = requests.get(repo_url, headers=headers,params=params)

    if debug:
        print(response.json())

    conn = sqlite3.connect('database.db')

    if response.status_code == 200:
        list_of_issues = response.json()
        if "?state=all" in repo_url:
            repo_url = repo_url.replace("?state=all", "")
        #loop through each pull request
        for issue in list_of_issues:
            issue_number = issue['number']
            issue_author_id = issue['user']['id']
            issue_author_username = issue['user']['login']
            issue_author_avatar_url = issue['user']['avatar_url']
            issue_title = issue['title']
            issue_url = issue['url']

            url = repo_url + '/' + str(issue_number) + '/comments'
            print("Retrieving comments from issue #" + str(issue_number) + "...")
            x = requests.get(url, headers=headers,params=params)
            s = SentimentIntensityAnalyzer()
            cursor = conn.cursor()
            data = x.json()

            if debug:
                print(data)

            #if author doesn't exist in database, add them
            query = "SELECT * FROM Author WHERE AuthorID = " + str(issue_author_id)
            cursor.execute(query)
            result = cursor.fetchone()
            if result == None:
                cursor.execute('INSERT INTO Author(AuthorID, Username, AvatarURL) VALUES(?,?,?)', (issue_author_id, issue_author_username, issue_author_avatar_url))

            #if pull request doesn't exist in database, add it
            query = "SELECT * FROM PullRequests WHERE RequestID = " + str(issue_number)
            cursor.execute(query)
            result = cursor.fetchone()
            if result == None:
                cursor.execute('INSERT INTO PullRequests(RequestID, AuthorID, Title, RequestURL) VALUES(?,?,?,?)', (issue_number, issue_author_id, issue_title, issue_url))
            
            if data is not None and isinstance(data, (list, dict)):
                #loop through each pull request comment
                for comment in data:
                    if 'user' in comment:
                        #gathers data from request about the comments and author
                        comment_id = comment['id']
                        query = "SELECT * FROM Comments WHERE CommentID = " + str(comment_id)
                        cursor.execute(query)
                        result = cursor.fetchone()
                        if result == None:
                            author_id = comment['user']['id']
                            text = comment['body']
                            if text is None:
                                continue
                            lines = text.splitlines()
                            lines = [string for string in lines if not string.startswith(">")]
                            lines = [re.sub(r"^On .+ [AP]M .+ wrote:", "", string) for string in lines]
                            body = "\n".join(lines)
                            #request_id = (comment['issue_url'])#.replace(repo_url + '/', '')
                            comment_url = comment['url']
                            sentiment_score = 0
                            association = comment['author_association']
                            timestamp = comment['created_at']
                            username = comment['user']['login']
                            avatar_url = comment['user']['avatar_url']
                            sentiment_score = s.polarity_scores(body)["compound"]
                            stop_word_ratio = sentiment_analysis.stop_word_ratio(body)

                            #adds comment to db if it doesn't already exist
                            query = "SELECT * FROM Comments WHERE CommentID = " + str(comment_id)
                            cursor.execute(query)
                            result = cursor.fetchone()
                            if result == None:
                                cursor.execute('INSERT INTO Comments(CommentID, AuthorID, Body, Timestamp, CommentURL, SentimentScore, Association, StopWordRatio, RequestID, ProjectID) VALUES(?,?,?,?,?,?,?,?,?,?)', (comment_id, author_id, body, timestamp, comment_url, sentiment_score, association, stop_word_ratio, issue_number, project_id))
                            
                            #adds author to db if they don't already exist
                            query = "SELECT * FROM Author WHERE AuthorID = " + str(author_id)
                            cursor.execute(query)
                            result = cursor.fetchone()
                            if result == None:
                                cursor.execute('INSERT INTO Author(AuthorID, Username, AvatarURL) VALUES (?,?,?)', (author_id, username, avatar_url))

            conn.commit()
        conn.close()

    else:
        print("Invalid request.")
