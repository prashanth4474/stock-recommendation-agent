import yfinance as yf
import json
stock = yf.Ticker("HDFCBANK.NS")  # Stock ticker
# recommendations = stock.info    # Stock recommendations
# OUTPUT_DIR = "D:/Docs/Learn AI/stock-recommendation-agent/data/fundamentals/hdfc_bank.json"
# with open(OUTPUT_DIR, "w") as f:
#     json.dump(recommendations, f, indent=4)
# print(recommendations)


# income_statement = stock.financials  # Income statement
# balance_sheet = stock.balance_sheet  # Balance sheet
# cash_flow = stock.cashflow  # Cash flow statement
# print(income_statement, balance_sheet, cash_flow)

# Fetch the news

OUTPUT_DIR = "D:/Docs/Learn AI/stock-recommendation-agent/data/news/yf_HDFCBANK.json"
news = stock.news
with open(OUTPUT_DIR, "w") as f:
        json.dump(news, f, indent=4)
print(news)

# Display the news articles
# for article in news:
#     print(f"Title: {article['title']}")
#     print(f"Publisher: {article['publisher']}")
#     print(f"Link: {article['link']}")
#     print(f"Published At: {article['providerPublishTime']}")
#     print("-" * 80)

