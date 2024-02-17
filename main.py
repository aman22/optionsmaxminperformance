from datetime import datetime, timedelta

import yfinance as yf

# Define the options contract symbol and expiration date
symbol = "AAPL210318C00130000"
expiration = "2023-03-18"

# Calculate the start date for retrieving historical data
start = datetime.strptime(expiration, '%Y-%m-%d') - timedelta(days=30)
start = start.strftime('%Y-%m-%d')

# Retrieve the options contract data for the date range
options_data = yf.Ticker(symbol).option_chain(expiration, start=start)

# Extract the Call prices from the options contract data
call_prices = options_data.calls["lastPrice"].tolist()

# Find the highest and lowest prices in the list
highest_price = max(call_prices)
lowest_price = min(call_prices)

# Print the results
print("Symbol: {}".format(symbol))
print("Expiration: {}".format(expiration))
print("Highest Price leading up to expiration: ${:.2f}".format(highest_price))
print("Lowest Price leading up to expiration: ${:.2f}".format(lowest_price))