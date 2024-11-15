import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import sys
import datetime

project_id = sys.argv[1]
# minimum interactions per reviewer and author
min_rev_interactions = int(sys.argv[2])
min_auth_interactions = 0

# minimum comments per interaction
if len(sys.argv) > 3:
    min_comments = int(sys.argv[2])
else:
    min_comments = 0

sql_statement = "SELECT Comments.AuthorID AS CID, PullRequests.AuthorID AS PID, Comments.SentimentScore FROM Comments INNER JOIN PullRequests ON Comments.RequestID = PullRequests.RequestID WHERE PullRequests.ProjectID = '" + project_id + "' AND Comments.Association != 'Bot' GROUP BY CID, PID HAVING COUNT(*) > " + str(min_comments)
conn = sqlite3.connect("database.db")
dataframe = pd.read_sql_query(sql_statement, conn)
x = dataframe.groupby(['CID', 'PID']).mean().unstack()
x = x.loc[:, x.count() > min_auth_interactions]
x = x.loc[x.count(axis=1) > min_rev_interactions, :]

c_map = plt.get_cmap('RdYlGn')
try:
    norm = colors.TwoSlopeNorm(vmin=x.values.min(), vcenter=0, vmax=x.values.max())
    plt.imshow(x, cmap=c_map, norm=norm, interpolation='nearest')
    plt.colorbar()
    plt.xticks(range(len(x.columns)), x.columns.get_level_values(1))
    plt.yticks(range(len(x.index)), x.index)
    plt.xticks(rotation=90,fontsize=5)
    plt.yticks(fontsize=5)
    
    plt.xlabel('Code Author ID')
    plt.ylabel('Reviewer ID')
    plt.title(f'Average Sentiment of Interactions between \nReviewer and Code Author for Project #{project_id}, \nMinimum Interactions = {str(min_rev_interactions)}')#, \nMinimum Comments = ' + str(min_comments))
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"output/heatmap_{min_rev_interactions}_{min_comments}_{project_id}_{current_time}.png"
    plt.subplots_adjust(bottom=0.25)
    plt.savefig(filename)
    plt.show()
    
except Exception as e:
    print(f"Could not load data\n{e}")