import re
import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute("SELECT Body FROM Comments")
rows = c.fetchall()

pattern = re.compile(r'^&gt;.*$', re.MULTILINE)

for row in rows:
    comment = row[0]
    comment = re.sub(pattern, '', comment)
    # Update the comment in the database
    c.execute("UPDATE Comments SET Body=? WHERE Body=?", (comment, row[0]))

conn.commit()
conn.close()