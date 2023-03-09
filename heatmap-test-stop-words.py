import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.colors as colors

# minimum interactions per reviewer and author
# turn into command line parameters
min_rev_interactions = int(input("Enter min_rev_interactions: "))
min_auth_interactions = 0#int(input("Enter min_auth_interactions: "))

# minimum comments per interaction
min_comments = int(input("Enter min_comments: "))

project_id = input("Enter project ID: ")

sql_statement = "SELECT Comments.AuthorID AS CID, PullRequests.AuthorID AS PID, Comments.SentimentScore FROM Comments INNER JOIN PullRequests ON Comments.RequestID = PullRequests.RequestID WHERE ProjectID = " + project_id + " GROUP BY CID, PID HAVING COUNT(*) > " + str(min_comments)
conn = sqlite3.connect("database.db")
dataframe = pd.read_sql_query(sql_statement, conn)
x = dataframe.groupby(['CID', 'PID']).mean().unstack()

# implemented with help of online resources
# filter out code authors below min_interactions
x = x.loc[:, x.count() > min_auth_interactions]

# filter out reviewers below min_interactions
x = x.loc[x.count(axis=1) > min_rev_interactions, :]


c_map = plt.get_cmap('RdYlGn')
norm = colors.TwoSlopeNorm(vmin=x.values.min(), vcenter=0, vmax=x.values.max())

# UPDATE THIS SO THAT USERS WHO HAVE ONLY HAD ONE INTERACTION ARE IGNORED.
# ASK CHATGPT HOW TO DO THIS
plt.imshow(x, cmap=c_map, norm=norm, interpolation='nearest')
plt.colorbar()
plt.xticks(range(len(x.columns)), x.columns.get_level_values(1))
plt.yticks(range(len(x.index)), x.index)

plt.xticks(rotation=90)

plt.xlabel('Code Author ID')
plt.ylabel('Reviewer ID')
plt.title('Average Sentiment of Interactions between \nReviewer and Code Author')

plt.subplots_adjust(bottom=0.25)
plt.show()