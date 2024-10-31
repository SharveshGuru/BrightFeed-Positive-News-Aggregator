# Import necessary modules for extracting, classifying, and generating the newsletter
import extract_articles
import classify_articles
import generate_newsletter

# Step 1: Extract and save articles to the database
# This function will scrape news articles and store them in the database for further processing
extract_articles.extract_and_save_to_db()

# Step 2: Classify the articles
# This function will analyze the articles in the database to determine positive articles
# It will also summarize them and store them in a separate table for easy access
classify_articles.classify_article()

# Step 3: Generate the newsletter
# This function will retrieve positive articles and format them into a newsletter
generate_newsletter.generate()
