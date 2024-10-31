from bs4 import BeautifulSoup
import requests
import sqlite3

def extract_and_save_to_db():
    conn = sqlite3.connect("news.db")
    cursor=conn.cursor()
    table_query = """
    CREATE TABLE IF NOT EXISTS articles (
        headline TEXT,
        link TEXT,
        pub_date DATETIME,
        content TEXT
    );
    """
    cursor.execute(table_query)
    conn.commit()

    url=requests.get("https://feeds.feedburner.com/ndtvnews-top-stories")
    soup=BeautifulSoup(url.content,'xml')

    items=soup.find_all('item')
    for item in items:
        headline = item.title.text
        link = item.link.text
        pub_date = item.pubDate.text
        content = BeautifulSoup(item.find('content:encoded').text, 'html.parser').get_text()
        print("Headline:", headline)
        print("Link:", link)
        print("Published Date and Time:", pub_date)
        print("Content:", content)
        insert_query = """
        INSERT INTO articles (headline, link, pub_date, content)
        VALUES (?, ?, ?, ?);
        """
        cursor.execute(insert_query,(headline,link,pub_date,content))
        conn.commit()
