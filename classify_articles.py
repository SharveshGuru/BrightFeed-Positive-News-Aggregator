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
    # Convert the text to lowercase
    data = data.lower()
    
    # Remove non-alphabetical characters
    data = re.sub(r'[^a-zA-Z\s]', '', data)
    
    # Tokenize the text into individual words
    tokens = word_tokenize(data)
    
    # Remove stop words
    stop_words = set(stopwords.words("english"))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Join tokens back into a single string and return
    return " ".join(tokens)

def analyse_article(headline, content):
    # Clean and preprocess both headline and content
    clean_headline = preprocess_article(headline)
    clean_content = preprocess_article(content)
    
    # Combine cleaned headline and content
    article_data = f"{clean_headline} {clean_content}"
    
    # Initialize the Sentiment Intensity Analyzer
    sia = SentimentIntensityAnalyzer()
    
    # Get sentiment scores for the article
    sentiment_scores = sia.polarity_scores(article_data)
    
    # Determine if the article is positive based on the compound score
    if sentiment_scores['compound'] >= -0.05:  # A threshold for positive/neutral sentiment
        return True
    return False

def summarize_article(content, num_sentences=7):
    # Tokenize content into sentences
    sentences = sent_tokenize(content)
    
    # If the article has fewer sentences than the summary limit, return the full content
    if len(sentences) <= num_sentences:
        return content
    
    # Define stop words and punctuation for filtering
    stop_words = set(stopwords.words('english') + list(punctuation))
    
    # Calculate word frequencies for non-stop words
    word_freq = FreqDist()
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word not in stop_words and word.isalnum():
                word_freq[word] += 1
    
    # Score sentences based on word frequencies
    sentence_scores = {}
    for sentence in sentences:
        score = 0
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                score += word_freq[word]
        sentence_scores[sentence] = score
    
    # Select the highest-scoring sentences for the summary
    summary_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    
    # Sort the summary sentences to maintain original order
    summary_sentences.sort(key=lambda x: sentences.index(x))
    
    # Join sentences to create the final summary
    summary = ' '.join(summary_sentences)
    
    return summary

def classify_article():
    # Connect to the SQLite database
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    
    # Fetch all articles from the "articles" table
    cursor.execute("SELECT * FROM articles")
    articles = cursor.fetchall()
    
    # Download necessary NLTK resources
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download('vader_lexicon', quiet=True)
    
    # Process each article and classify positive ones
    for headline, link, pub_date, content in articles:
        # Check if the article has a positive sentiment
        if analyse_article(headline, content):
            # Insert positive articles along with their summaries into "positive_articles" table
            insert_query = """
            INSERT INTO positive_articles (headline, link, pub_date, summary)
            VALUES (?, ?, ?, ?);
            """
            cursor.execute(insert_query, (headline, link, pub_date, summarize_article(content)))
            conn.commit()  # Commit the insertion for each positive article

    # Close the database connection
    conn.close()
    
    # Indicate completion
    print("Positive articles have been classified and saved.")
