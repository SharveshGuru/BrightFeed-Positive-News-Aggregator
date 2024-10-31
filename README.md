# BrightFeed-Positive-News-Aggregator

BrightFeed is an automated news aggregation system that collects, analyzes, and curates positive news stories to create an uplifting newsletter. The system uses natural language processing to identify positive news articles and generates a professionally formatted PDF newsletter.

## Features

- Automated news article extraction from "NDTV's Top Feed" RSS feed.
- Sentiment analysis to identify positive news stories.
- Intelligent article summarization.
- Automatic PDF newsletter generation.
- SQLite database for efficient data management.

## Technical Architecture

The project consists of three main modules:

1. **Article Extraction** (`extract_articles.py`)
   - Fetches news from RSS feeds
   - Parses XML content using BeautifulSoup
   - Stores articles in SQLite database

2. **Article Classification** (`classify_articles.py`)
   - Performs sentiment analysis using NLTK
   - Generates article summaries
   - Filters and stores positive articles

3. **Newsletter Generation** (`generate_newsletter.py`)
   - Creates professional PDF newsletters using ReportLab
   - Includes headlines, summaries, and source links
   - Formats content with proper styling and layout

## Requirements

```
beautifulsoup4==4.12.3
bs4==0.0.2
certifi==2024.8.30
chardet==5.2.0
charset-normalizer==3.4.0
click==8.1.7
colorama==0.4.6
idna==3.10
joblib==1.4.2
lxml==5.3.0
nltk==3.9.1
pillow==11.0.0
regex==2024.9.11
reportlab==4.2.5
requests==2.32.3
soupsieve==2.6
tqdm==4.66.6
urllib3==2.2.3
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/SharveshGuru/BrightFeed-Positive-News-Aggregator.git
cd BrightFeed-Positive-News-Aggregator
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the main script to generate a newsletter:

```python
python driver.py
```

The process follows these steps:
1. Extracts articles from "NDTV's Top Feed" RSS feed.
2. Analyzes and classifies positive articles.
3. Generates a PDF newsletter named "BrightFeed Newsletter.pdf".

## Database Schema

### Articles Table
- headline (TEXT)
- link (TEXT)
- pub_date (DATETIME)
- content (TEXT)

### Positive Articles Table
- headline (TEXT)
- link (TEXT)
- pub_date (DATETIME)
- summary (TEXT)

## Key Features Explained

### Sentiment Analysis
- Uses NLTK's VADER sentiment analyzer
- Determines article positivity based on compound sentiment scores
- Filters out negative news automatically

### Article Summarization
- Implements frequency-based extractive summarization
- Selects most relevant sentences
- Maintains original context while reducing length

### Newsletter Generation
- Professional PDF layout
- Clickable article links
- Formatted publication dates
- Clean typography and spacing

## Contributing

Contributions to improve the project are welcome. Please feel free to submit issues or pull requests.