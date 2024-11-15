import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import sys
import sentiment_analysis as sa

def analyse_comment(comment):
    sentences = nltk.sent_tokenize(comment)
    feedback = '\n'
    sia = SentimentIntensityAnalyzer()
    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(comment)
    pos_words = []
    neg_words = []
    for word in words:
        if word not in pos_words and word not in neg_words:
            score = sia.polarity_scores(word)
            if score['compound'] > 0:
                pos_words.append(word)
            elif score['compound'] < 0:
                neg_words.append(word)

    code_snippets = sa.code_snippet_count(comment)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    stop_word_ratio = len(filtered_words) / len(words)
    stop_word_label = f"{stop_word_ratio}\nThe lower this ratio, the easier to read your feedback will be.\n"
    for sentence in sentences:
        sentiment = sia.polarity_scores(sentence)
        if sentiment['compound'] > 0:
            sentiment_label = "The sentiment of this sentence is positive."
        elif sentiment['compound'] < 0:
            sentiment_label = "Consider making the sentiment of this sentence more positive."
        else:
            sentiment_label = "The sentiment of this sentence is neutral."
        sentiment_label += f"\nSentiment score: {sentiment['compound']}"
        feedback += "Sentence: {}\n".format(sentence)
        feedback += "{}\n\n".format(sentiment_label)
    feedback += "Stop word ratio: {}\n".format(stop_word_label)
    if pos_words:
        feedback += "Positive words used: {}\n".format(pos_words)
    else:
        feedback += "No positive words detected.\n"
    if neg_words:
        feedback += "Negative words used: {}\n".format(neg_words)
    else:
        feedback += "No negative words detected.\n"
    feedback += "Code snippets used: {}\n".format(code_snippets)
    if code_snippets > 0:
        feedback += "Including code snippets help to indicate you understand the code being reviewed.\n"
    return feedback

def main():
    comment = sys.argv[1]
    feedback = analyse_comment(comment)
    print(feedback)

if __name__ == "__main__":
    main()
