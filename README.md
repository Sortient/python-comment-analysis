# Python Review Comment Analysis
This is a collection of scripts designed to help analyse and automatically score code review comments, from projects on GitHub.

# Requirements
Minimum version Python 3.10

A UNIX based OS

# Installation and Set-up
Download the repository and open a terminal window in the python-comment-analysis folder.

Next, install the required Python packages by running the following commands:
```python
pip3 install sqlite3
pip3 install nltk
pip3 install PyGithub
pip3 install tqdm
pip3 install matplotlib
pip3 install pandas
```
## Retrieving Review Comments
Before we can generate any results we first need to retrieve pull request comments in order to analyse results. This can be done by running the following command:
```sh
sh retrieve.sh
```

Verify that the projects are successfully inputted into the database by running the following script:

```python
python3 list.py
```
This will generate a list of all projects in the database along with the number of comments. If this list generates successfully, the 
# Usage Guide
There is a default list of repositories contained within **repos.txt**, however if you wish you can add additional repositories. They must be in the format {owner} {repo} separated by a space.

#Usage
##Adding Additional Projects
repos.txt contains a list of default repositories that retrieve.sh will fetch pull requests from, but you can add additional repositories by adding a new line in the format {owner} {repo}, ensuring that a space separates the two.

By default retrieve.sh will retrieve a maximum of 1000 comments from a repository, however this can be changed by specifying a maximum number as below:
```sh
sh retrieve.sh 1500
```
This would retrieve a maximum of 1500 comments per repository. 

retrieve.sh will skip over any projects that are already in the database. You can also manually retrieve comments from a repository by running the following command:
```python
python3 retrieve.py {owner} {repo} {max_comments}
```
max_comments is an optional variable that will default to 1000 if left blank.
