import retrievejson as rj
import sys

repo_url = sys.argv[1]
id = sys.argv[2]
rj.retrieve_eclipse_cdt_pull_comments(repo_url, id)