import requests
from bs4 import BeautifulSoup

# Example: Scrape news headlines from the Economic Times website
url = "https://economictimes.indiatimes.com/markets/stocks/news"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract and print news headlines
headlines = soup.find_all("a", class_="newsList__headline")
print("Top 10 News Headlines:")
for i, headline in enumerate(headlines[:10], start=1):
    print(f"{i}. {headline.text.strip()}")
