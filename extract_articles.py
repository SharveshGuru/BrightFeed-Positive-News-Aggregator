from bs4 import BeautifulSoup
import requests
import sqlite3

def extract_and_save_to_db():
    # Connect to a SQLite database
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    
    # SQL query to create the "articles" table if it does not exist
    table_query1 = """
    CREATE TABLE IF NOT EXISTS articles (
        headline TEXT,
        link TEXT,
        pub_date DATETIME,
        content TEXT
    );
    """
    
    # SQL query to create the "positive_articles" table if it does not exist
    table_query2 = """
    CREATE TABLE IF NOT EXISTS positive_articles (
        headline TEXT,
        link TEXT,
        pub_date DATETIME,
        summary TEXT
    );
    """
    
    # Execute table creation queries
    cursor.execute(table_query1)
    cursor.execute(table_query2)
    conn.commit()  # Commit the table creation to the database
    
    # Fetch XML data from the RSS feed URL
    url = requests.get("https://feeds.feedburner.com/ndtvnews-top-stories")
    soup = BeautifulSoup(url.content, 'xml')
    
    # Extract all items from the feed
    items = soup.find_all('item')
    
    # Loop through each news item in the RSS feed
    for item in items:
        # Extract headline, link, publication date, and content
        headline = item.title.text
        link = item.link.text
        pub_date = item.pubDate.text
        # Get article content, using HTML parsing to remove any HTML tags
        content = BeautifulSoup(item.find('content:encoded').text, 'html.parser').get_text()
        
        # SQL query to insert data into the "articles" table
        insert_query = """
        INSERT INTO articles (headline, link, pub_date, content)
        VALUES (?, ?, ?, ?);
        """
        
        # Execute the insertion query with data
        cursor.execute(insert_query, (headline, link, pub_date, content))
        conn.commit()  # Commit the insert operation for each item

    # Close the database connection
    conn.close()
    
    # Indicate completion
    print("Articles have been stored in the database.")
