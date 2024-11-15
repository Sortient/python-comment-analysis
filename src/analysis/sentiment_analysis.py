from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import re
stop_words = set(stopwords.words('english'))
s = SentimentIntensityAnalyzer()

stop_word_threshold = 0.4

def is_positive(y: str) -> bool:
    return s.polarity_scores(y)["compound"] >= 0

def stop_word_count(y:str) -> int:
    words = word_tokenize(y)
    count = 0
    for word in words:
        if word in stop_words:
            count += 1
    return count

def stop_word_ratio(y:str) -> float:
    words = word_tokenize(y)
    total_count = 0
    stop_count = 0
    for word in words:
        total_count += 1
        if word in stop_words:
            stop_count += 1
    if total_count != 0:
        return stop_count / total_count
    else:
        return 0
def code_snippet_count(body, language=None):
    body.replace('\\n',' ')
    body.replace('\\t',' ')
    if language:
        code_snippet_regex = rf'```{language}\n([\s\S]+?)```'
    else:
        code_snippet_regex = r'```(?:\w+\n)?([\s\S]+?)```'
    code_snippets = re.findall(code_snippet_regex, body)
    return len(code_snippets)

def exclude_snippets(body):
    text = body
    code_snippets = re.findall(r'```[\s\S]*?```', text)
    for snippet in code_snippets:
        text = text.replace(snippet, '')

    lines = text.splitlines()
    lines = [string for string in lines if not string.startswith(">")]
    lines = [re.sub(r"^On .+ [AP]M .+ wrote:", "", string) for string in lines]
    output = "\n".join(lines)
    return output

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def tag(text):
    tokens = word_tokenize(text)
    tags = pos_tag(tokens)
    return tags

def ratio_request_verbs(text):
    tags = tag(text)
    vor = ['VB', 'VBP', 'VBZ']
    total = 0
    count = 0
    for token, postag in tags:
        if postag.startswith('VB'):
            total += 1
            if postag in vor:
                count += 1
    print(count)
    print(total)
    if total == 0:
        return 0.0
    else:
        return count / total