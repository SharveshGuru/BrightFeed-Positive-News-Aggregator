import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

def generate():
    # Connect to the SQLite database and fetch data
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    cursor.execute("SELECT headline, link, pub_date, summary FROM positive_articles")
    articles = cursor.fetchall()

    # Create a PDF document using ReportLab
    pdf_filename = "BrightFeed Newsletter.pdf"
    pdf = SimpleDocTemplate(pdf_filename, pagesize=A4)
    styles = getSampleStyleSheet()

    # List to store content for the PDF
    content = []

    # Title for the newsletter
    title = Paragraph("BrightFeed Newsletter", styles["Title"])
    content.append(title)
    content.append(Spacer(1, 12))

    # Add each article to the PDF content
    for article in articles:
        headline, link, pub_date, summary = article
        # Format the publication date
        pub_date = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z").strftime("%B %d, %Y")

        # Add the headline
        headline_paragraph = Paragraph(f"<b>{headline}</b> ({pub_date})", styles["Heading2"])
        content.append(headline_paragraph)
        content.append(Spacer(1, 6))

        # Add the summary
        summary_paragraph = Paragraph(summary, styles["BodyText"])
        content.append(summary_paragraph)
        content.append(Spacer(1, 6))

        # Add the link as a clickable URL
        link_paragraph = Paragraph(f'<a href="{link}" color="blue">{link}</a>', styles["BodyText"])
        content.append(link_paragraph)
        content.append(Spacer(1, 12))

    # Build the PDF
    pdf.build(content)

    # Close the database connection
    conn.close()
    print(f"Newsletter saved as {pdf_filename}")