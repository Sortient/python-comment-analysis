from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
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
    return stop_count / total_count

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