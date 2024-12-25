import yfinance as yf
import os
import matplotlib.pyplot as plt

# Parameters
tickers = ["HDFCBANK.NS", "ITC.NS"]
start_date = "2018-01-01"
end_date = "2023-12-31"

# Directory to save historical data
output_dir = "data/historical/"
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

for ticker in tickers:
    print(f"Fetching data for {ticker}...")
    data = yf.download(ticker, start=start_date, end=end_date)

    # Save the data to CSV in the appropriate folder
    filename = os.path.join(output_dir, f"{ticker}_historical_data.csv")
    data.to_csv(filename)
    print(f"Data saved to {filename}")

    # Plot the closing price
    data['Close'].plot(title=f"{ticker} Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.show()
