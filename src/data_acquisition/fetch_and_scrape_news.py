import os
import json
import requests
from datetime import datetime
import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup

# News API settings
API_KEY = "5027a029a85640d48588d1357777d571"
QUERY = "Indian stock market OR FMCG OR Nifty OR Sensex"
API_URL = f"https://newsapi.org/v2/everything?q={QUERY}&language=en&sortBy=publishedAt&apiKey={API_KEY}"

# Directory settings
OUTPUT_DIR = "D:/Docs/Learn AI/stock-recommendation-agent/data/news/"
MERGED_FILE = os.path.join(OUTPUT_DIR, "merged_news.json")
SCRAPED_FILE = os.path.join(OUTPUT_DIR, "scraped_news.json")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Fetch news from News API
def fetch_news_api():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(OUTPUT_DIR, f"news_api_{timestamp}.json")
        with open(output_file, "w") as f:
            json.dump(articles, f, indent=4)
        print(f"Fetched {len(articles)} articles from News API. Saved to {output_file}")
    else:
        print(f"Failed to fetch news from API. HTTP Status Code: {response.status_code}")

# Scrapy Spider settings for web scraping
class StockNewsSpider(scrapy.Spider):
    name = "stocknews"
    
    # List of websites to scrape
    start_urls = [
        "https://www.moneycontrol.com/news/business/markets/",
        "https://economictimes.indiatimes.com/markets/stocks/news",
        "https://www.livemint.com/market/stock-market-news",
        "https://www.business-standard.com/market/stock-market",
        "https://www.nseindia.com/market-data/live-equity-market"
    ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'COOKIES_ENABLED': True,
        'RETRY_TIMES': 2,  # Number of retries
        'RETRY_DELAY': 2,  # Delay in seconds between retries
        'CONCURRENT_REQUESTS': 16,  # Increase the number of concurrent requests
        'DOWNLOAD_DELAY': 0,  # No delay between requests
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,  # Increase the number of concurrent requests per domain
        'HTTPCACHE_ENABLED': True,  # Enable HTTP caching
        'HTTPCACHE_EXPIRATION_SECS': 0,  # Never expire cache
        'HTTPCACHE_DIR': 'httpcache',  # Directory for HTTP cache
        'HTTPCACHE_IGNORE_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 429],  # Ignore these HTTP codes for caching
        'HTTPCACHE_STORAGE': 'scrapy.extensions.httpcache.FilesystemCacheStorage',  # Use filesystem for cache storage
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.articles = []

    def parse(self, response):
        if "moneycontrol" in response.url:
            articles = response.xpath('//li[contains(@class, "clearfix")]')
        elif "economictimes" in response.url:
            articles = response.xpath('//div[contains(@class, "eachStory")]')
        elif "livemint" in response.url:
            articles = response.xpath('//div[contains(@class, "listing-txt")]')
        elif "business-standard" in response.url:
            articles = response.xpath('//div[contains(@class, "news-item")]')
        elif "nseindia" in response.url:
            articles = response.xpath('//a[contains(@class, "news-link")]')

        for article in articles[:10]:  # Limit to top 10 articles per website
            title = article.xpath('.//a/text()').get()
            link = article.xpath('.//a/@href').get()
            if title and link:
                self.articles.append({
                    'title': title.strip(),
                    'link': link.strip(),
                })
            else:
                self.log(f"Missing title or link in article: {article}")

    def closed(self, reason):
        with open(SCRAPED_FILE, "w") as f:
            json.dump(self.articles, f, indent=4)
        print(f"Scraped {len(self.articles)} articles. Saved to {SCRAPED_FILE}")

# Run the Scrapy Spider
def run_scrapy_spider():
    process = CrawlerProcess(settings={
        'ROBOTSTXT_OBEY': False,  # Disable robots.txt rules
    })
    process.crawl(StockNewsSpider)
    process.start()

# Merge and clean data
def merge_and_clean_data():
    articles = []
    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith(".json") and filename != "merged_news.json":
            with open(os.path.join(OUTPUT_DIR, filename), "r") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        articles.extend(data)
                    else:
                        print(f"Skipping non-list JSON file: {filename}")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from file {filename}: {e}")
    
    with open(MERGED_FILE, "w") as f:
        json.dump(articles, f, indent=4)
    print(f"Merged {len(articles)} articles into {MERGED_FILE}")

if __name__ == "__main__":
    #fetch_news_api()
    run_scrapy_spider()
    merge_and_clean_data()