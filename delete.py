import sqlite3
import sys
def delete_project_and_comments(project_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM Comments WHERE ProjectID=?", (project_id,))
    c.execute("DELETE FROM PullRequests WHERE ProjectID=?", (project_id,))
    c.execute("DELETE FROM Project WHERE ProjectID=?", (project_id,))
    conn.commit()
    conn.close()

project_id = sys.argv[1]
delete_project_and_comments(project_id)
print(f"Project {project_id} removed from database.")