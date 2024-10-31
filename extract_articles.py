from bs4 import BeautifulSoup
import requests
import sqlite3

def extract_and_save_to_db():
    conn = sqlite3.connect("news.db")
    cursor=conn.cursor()
    table_query1 = """
    CREATE TABLE IF NOT EXISTS articles (
        headline TEXT,
        link TEXT,
        pub_date DATETIME,
        content TEXT
    );
    """
    table_query2 = """
    CREATE TABLE IF NOT EXISTS positive_articles (
        headline TEXT,
        link TEXT,
        pub_date DATETIME,
        summary TEXT
    );
    """
    cursor.execute(table_query1)
    cursor.execute(table_query2)
    conn.commit()

    url=requests.get("https://feeds.feedburner.com/ndtvnews-top-stories")
    soup=BeautifulSoup(url.content,'xml')

    items=soup.find_all('item')
    for item in items:
        headline = item.title.text
        link = item.link.text
        pub_date = item.pubDate.text
        content = BeautifulSoup(item.find('content:encoded').text, 'html.parser').get_text()
        insert_query = """
        INSERT INTO articles (headline, link, pub_date, content)
        VALUES (?, ?, ?, ?);
        """
        cursor.execute(insert_query,(headline,link,pub_date,content))
        conn.commit()
    # print("Articles have been stored in the database.")

extract_and_save_to_db()