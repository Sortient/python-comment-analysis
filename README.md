# Python Review Comment Analysis
This is a modular suite of tools designed to help analyse and automatically score code review comments, from projects on GitHub.

# Requirements
Minimum version Python 3.10

A UNIX based OS

SQLite Studio (recommended)

# Installation and Setup
Download the repository and open a terminal window in the python-comment-analysis folder.

Next, install the required Python packages by running the following command:
```sh
sh install.sh
```
You will also need to generate a personal token in order to make use of the GitHub API. Information on this can be found [here](https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token). Copy this token and paste it into token.txt.

## Retrieving Review Comments
Before we can generate any results we first need to retrieve pull request comments in order to analyse results. This can be done by running the following command:
```sh
sh retrieve.sh
```

The first time this runs will take a while to complete. Once it finishes, you can verify that the projects are successfully inputted into the database by running the following script:

```python
python3 list.py
```
This will generate a list of all projects in the database along with the number of comments. If this list generates successfully, then you have successfully retrieved data from the GitHub API. 

# Usage

## Adding Additional Projects
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

## Generating Results
Figures may be displayed after running the following scripts; they will also be saved to the output folder.

### Overall Project Results
These results will be saved to output/overall.

To compare various metrics across all projects, run the following command:
```sh
sh overall.sh
```
which will automatically generate figures comparing each project that you have stored in your database. It will compare:
- Total number of comments
- Percentage of positive comments
- Average comment sentiment
- Percentage of comments containing code snippets
- Average stop word ratio

### Positive and Negative Words Used
To observe the top x positive and negative words used within a project, run the following command:
```sh
sh pos-neg-project.sh {max_words} {project_id}
```
For example, to retrieve the top 15 most common positive and negative words from project \#2, run:
```sh
sh pos-neg-project.sh 15 2
```
Figures containing the specified number of positive and negative words will be contained within the output folder upon running the script.

### Comparing Project Sentiment - Reviewer vs Author
To generate a heatmap which compares interactions between reviewer and author across a project, run the following command:
```python
python3 heatmap.py {project_id} {min_interactions}
```
where min_interactions is the minimum number of interactions between a reviewer and author required for a given intersection to appear on the heatmap. The heatmap will be contained within the output folder.

### Automated Comment Scoring
To receive automated feedback on a new review comment, run the following command:
```python
python3 input-comment.py '{your comment here}'
```
Ensure that you surround your review comment with apostrophes. You will receive a breakdown of the sentiment of each sentence contained within your review.
