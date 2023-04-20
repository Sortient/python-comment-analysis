import matplotlib.pyplot as plt
import datetime as dt
data = {}
current_time = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

output_dir = "output/overall"

with open('output/project-overall.txt', 'r') as f:
    current_project_id = None
    for line in f:
        line = line.strip()
        if line.startswith('Project'):
            current_project_id = line.split()[1]
            data[current_project_id] = {}
        elif current_project_id is not None:
            if line.startswith('Comment total:'):
                data[current_project_id]['comment_total'] = int(line.split()[2])
            elif line.endswith('% of comments are positive'):
                data[current_project_id]['pos_ratio'] = float(line.split()[0].replace('%',''))
            elif line.startswith('Average sentiment:'):
                data[current_project_id]['avg_sentiment'] = float(line.split()[2])
            elif line.startswith('Average stop word ratio:'):
                data[current_project_id]['avg_stop_word'] = float(line.split()[4])
            elif line.startswith('Percentage of comments containing code snippets'):
                data[current_project_id]['code_snippet_percentage'] = float(line.split()[6].replace('%', ''))

if data is not None:
    x = list(data.keys())
    a = [data[project]['pos_ratio'] for project in x]

    plt.bar(x, a, color='red')
    plt.title('Positive Comment Percentage by Project')
    plt.xlabel('Project')
    plt.ylabel('Positive Comment Percentage')
    plt.savefig(f"{output_dir}/positive_comment_{current_time}.png")

    plt.clf()
    b = [data[project]['comment_total'] for project in x]
    plt.bar(x, b, color='blue')
    plt.title('Total Number of Comments by Project')
    plt.xlabel('Project')
    plt.ylabel('Total Number of Comments')
    plt.savefig(f"{output_dir}/comment_total_{current_time}.png")

    plt.clf()
    c = [data[project]['avg_sentiment'] for project in x]
    plt.bar(x, c, color='green')
    plt.title('Average Review Sentiment by Project')
    plt.xlabel('Project')
    plt.ylabel('Average Review Sentiment')
    plt.savefig(f"{output_dir}/avg_sentiment_{current_time}.png")

    plt.clf()
    d = [data[project]['avg_stop_word'] for project in x]
    plt.bar(x, d, color='orange')
    plt.title('Stop Word Ratio by Project')
    plt.xlabel('Project')
    plt.ylabel('Stop Word Ratio')
    plt.savefig(f"{output_dir}/avg_stop_word_{current_time}.png")

    plt.clf()
    d = [data[project]['code_snippet_percentage'] for project in x]
    plt.bar(x, d, color='cyan')
    plt.title('Percentage of Comments Containing Code Snippets By Project')
    plt.xlabel('Project')
    plt.ylabel('Code Snippet Percentage')
    plt.savefig(f"{output_dir}/code_snippet_percentage_{current_time}.png")