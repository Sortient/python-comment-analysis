import retrievejson as rj
import sys
import sqlite3
import retrieve as rcpyg

author = sys.argv[1]
repo = sys.argv[2]
id = sys.argv[3]
pages = sys.argv[4]
debug_mode = len(sys.argv) > 5 and sys.argv[5].lower() == 'true'

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

query = "SELECT * FROM Project WHERE ProjectID = '" + str(id) + "'"
cursor.execute(query)
result = cursor.fetchone()

if result == None:
    repo_url = f"https://api.github.com/repos/{author}/{repo}/pulls?state=all"
    #rj.retrieve_eclipse_cdt_pull_comments(repo_url, id, 3, debug_mode)
    rcpyg.retrieve_eclipse_cdt_pull_comments(author, repo, id, 3, debug_mode)
else:
    print("A project with the same ProjectID already exists in the database.")
