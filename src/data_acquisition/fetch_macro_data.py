import requests

# Replace 'YOUR_API_KEY' with your Trading Economics API key
api_key = "YOUR_API_KEY"
url = f"https://api.tradingeconomics.com/indicators?c={api_key}"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print("Top 10 Macroeconomic Indicators:")
    for item in data[:10]:  # Print the first 10 indicators
        print(f"{item['Category']} - {item['Country']}: {item['LatestValue']}")
else:
    print("Failed to fetch data:", response.status_code)
