import sqlite3
import re
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from github import Github
import sentiment_analysis
import sys
from tqdm import tqdm

#def retrieve_eclipse_cdt_pull_comments(owner, repo, id, pages, debug_mode):
owner = sys.argv[1]
repo = sys.argv[2]
#id = sys.argv[3]
append = False
if len(sys.argv) > 3:
    max_comments = int(sys.argv[3])
    if len(sys.argv) > 4:
        append = sys.argv[4].lower() in ['true', '1', 't', 'y', 'yes']
else:
    max_comments = 1000

g = Github("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")
s = SentimentIntensityAnalyzer()
try:
    repo = g.get_repo(f"{owner}/{repo}")
except:
    print(f"WARNING: project {owner}/{repo} could not be found.")
    sys.exit(1)
    
url = repo.url
pulls = repo.get_pulls(state="all")
comment_count = 0
cont_flag = True
conn = sqlite3.connect('database.db')
query = f"SELECT * FROM Project WHERE ProjectURL = '{url}'"
cursor = conn.cursor()
cursor.execute(query)
result = cursor.fetchone()
repo_name = repo.full_name

if result is not None:
    print(f"WARNING: project {repo_name} already exists in the database.")
    if not append:
        cont_flag = False
        sys.exit(1)
else:
    cursor.execute('INSERT INTO Project(ProjectURL) VALUES(?)', (url,))
    conn.commit()

if cont_flag:
    query = f"SELECT ProjectID FROM Project WHERE ProjectURL = '{url}'"
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    id = result[0]

    print(f"Now processing pull requests from {repo_name}. This may take a while, please wait...")
    pbar = tqdm(total=max_comments)
    for pull in pulls:
        if comment_count >= max_comments:
            print("Done. (Maximum comment count reached.)")
            sys.exit(1)
        pull_number = pull.number
        pull_author_id = pull.user.id
        pull_author_username = pull.user.login
        pull_author_avatar_url = pull.user.avatar_url
        pull_title = pull.title
        pull_url = pull.html_url
        comments_url = pull.comments_url
        comments = pull.get_issue_comments()

        #if author doesn't exist in database, add them
        query = "SELECT * FROM Author WHERE AuthorID = " + str(pull_author_id)
        cursor.execute(query)
        result = cursor.fetchone()
        if result == None:
            cursor.execute('INSERT INTO Author(AuthorID, Username, AvatarURL) VALUES(?,?,?)', (pull_author_id, pull_author_username, pull_author_avatar_url))

        #if pull request doesn't exist in database, add it
        query = "SELECT * FROM PullRequests WHERE RequestID = " + str(pull_number)
        cursor.execute(query)
        result = cursor.fetchone()
        if result == None:
            cursor.execute('INSERT INTO PullRequests(RequestID, AuthorID, Title, RequestURL, ProjectID) VALUES(?,?,?,?,?)', (pull_number, pull_author_id, pull_title, pull_url, id))
        
        #print(f"Processing comments from pull request #{pull_number}...")
        for comment in comments:
            
            user = comment.user
            association = user.type

            # skips comments from bots
            if association == 'Bot':
                continue
            comment_count = comment_count + 1
            comment_id = comment.id
            author_id = user.id
            text = comment.body
            
            if text is None:
                continue

            lines = text.splitlines()
            lines = [string for string in lines if not string.startswith(">")]
            lines = [re.sub(r"^On .+ [AP]M .+ wrote:", "", string) for string in lines]
            body = "\n".join(lines)
            body_no_snippets = sentiment_analysis.exclude_snippets(body)
            comment_url = comment.url
            sentiment_score = 0
            timestamp = comment.created_at
            username = user.login
            avatar_url = user.avatar_url
            sentiment_score = s.polarity_scores(body_no_snippets)["compound"]
            code_snippet_count = sentiment_analysis.code_snippet_count(body)
            stop_word_ratio = sentiment_analysis.stop_word_ratio(body_no_snippets)

            #adds comment to db if it doesn't already exist
            query = "SELECT * FROM Comments WHERE CommentID = " + str(comment_id)
            cursor.execute(query)
            result = cursor.fetchone()
            if result is None:
                cursor.execute('INSERT INTO Comments(CommentID, AuthorID, Body, Timestamp, CommentURL, SentimentScore, Association, StopWordRatio, RequestID, ProjectID, CodeSnippetCount) VALUES(?,?,?,?,?,?,?,?,?,?,?)', (comment_id, author_id, body, timestamp, comment_url, sentiment_score, association, stop_word_ratio, pull_number, id, code_snippet_count))
            
            #adds author to db if they don't already exist
            query = "SELECT *  FROM Author WHERE AuthorID = " + str(author_id)
            cursor.execute(query)
            result = cursor.fetchone()
            if result is None:
                cursor.execute('INSERT INTO Author(AuthorID, Username, AvatarURL) VALUES (?,?,?)', (author_id, username, avatar_url))

            conn.commit()
            pbar.update(1)
print(f"\Finished retrieving comments from {repo_name}.")