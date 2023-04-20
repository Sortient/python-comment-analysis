import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import sys
nltk.download('vader_lexicon')
def analyse_comment(comment):
    sentences = nltk.sent_tokenize(comment)
    feedback = ''
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

    filtered_words = [word for word in words if word.lower() not in stop_words]
    stop_word_ratio = len(filtered_words) / len(words)
    if stop_word_ratio > 0.3:
        stop_word_label = "Consider using fewer stop words, to improve your review comment's readability."
    else:
        stop_word_label = "There is a good ratio of stop words in your comment. This will help the code author to better understand your feedback."
    for sentence in sentences:
        sentiment = sia.polarity_scores(sentence)
        if sentiment['compound'] > 0:
            sentiment_label = "The sentiment of this sentence is positive."
        elif sentiment['compound'] < 0:
            sentiment_label = "Consider making the sentiment of this sentence more positive."
        else:
            sentiment_label = "The sentiment of this sentence is neutral"
        feedback += "Sentence: {}\n".format(sentence)
        feedback += "{}\n\n".format(sentiment_label)
    feedback += "Stop word ratio: {}\n".format(stop_word_label)
    feedback += "Positive words used: {}\n".format(pos_words)
    feedback += "Negative words used: {}\n".format(neg_words)
    return feedback

def main():
    comment = sys.argv[1]
    feedback = analyse_comment(comment)
    print(feedback)

if __name__ == "__main__":
    main()
