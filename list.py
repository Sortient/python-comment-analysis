import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute("SELECT ProjectID, ProjectURL FROM Project")
for row in c.fetchall():
    print(row[0], row[1])
c.close()
conn.close()