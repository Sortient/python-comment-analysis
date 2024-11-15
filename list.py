import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute("SELECT Project.ProjectID, Project.ProjectURL, COUNT(Comments.ProjectID) FROM Project INNER JOIN Comments ON Project.ProjectID = Comments.ProjectID GROUP BY Project.ProjectID")
for row in c.fetchall():
    print(f"{row[0]} {row[1]}: {row[2]} comments")
c.close()
conn.close()