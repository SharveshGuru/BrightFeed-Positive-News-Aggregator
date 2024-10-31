import sqlite3
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from heapq import nlargest
from string import punctuation
import re


def preprocess_article(data):
    data=data.lower()
    
    data = re.sub(r'[^a-zA-Z\s]', '', data)
    
    tokens=word_tokenize(data)
    stop_words=set(stopwords.words("english"))
    tokens=[token for token in tokens if token not in stop_words]
    
    return " ".join(tokens)

def analyse_article(headline,content):
    clean_headline = preprocess_article(headline)
    clean_content = preprocess_article(content)
    
    article_data = f"{clean_headline} {clean_content}"
    
    sia = SentimentIntensityAnalyzer()
    
    sentiment_scores = sia.polarity_scores(article_data)
    
    if sentiment_scores['compound']>=-0.5:
        return True
    return False

def summarize_article(content, num_sentences=7):
    sentences = sent_tokenize(content)
    
    if len(sentences) <= num_sentences:
        return content
    
    stop_words = set(stopwords.words('english') + list(punctuation))
    word_freq = FreqDist()
    
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word not in stop_words and word.isalnum():
                word_freq[word] += 1
    
    sentence_scores = {}
    for sentence in sentences:
        score = 0
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                score += word_freq[word]
        sentence_scores[sentence] = score
    
    summary_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    
    summary_sentences.sort(key=lambda x: sentences.index(x))
    
    summary = ' '.join(summary_sentences)
    
    return summary

def classify_articles():
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles")
    articles = cursor.fetchall()
    
    nltk.download("punkt_tab")
    nltk.download("stopwords")
    nltk.download('vader_lexicon', quiet=True)
    
    for headline,link,pub_date,content in articles:
        if analyse_article(headline,content):
            insert_query = """
            INSERT INTO positive_articles (headline, link, pub_date, summary)
            VALUES (?, ?, ?, ?);
            """
            cursor.execute(insert_query,(headline,link,pub_date,summarize_article(content)))
            conn.commit()

