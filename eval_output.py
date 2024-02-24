from prettytable import PrettyTable
import json
with open('output.json', 'r') as json_file:
    data = json.load(json_file)

# Create a new PrettyTable from the saved string
loaded_table = PrettyTable()
loaded_table.field_names = [
    "Alert Type", "Side", "Type", "Alert Time", "Ticker", "Strike", "Expiration", "DTE", "Success?", "Profit?", "Profit%", "Average Fill", "max_avg_price", "min_avg_price",
    "Interval Volume", "Open Interest", "Vol/OI", "OTM", "Bid/Ask %", "Premium",
    "Multi-leg Volume", "URL", "Time and Sales URL"
]

for item in data:
    side = ''
    if "Ask" in item["title"]:
        side = 'Ask'
    else:
        side = 'Bid'
    if "Hot" in item["title"]:
        item["title"] = 'Hot'
    else:
        item["title"] = 'Interval'

    loaded_table.add_row([
        item["title"], side, item["option_type"], item["timestamp"], item["ticker"], item["strike"],
        item["expiration_date"], item["days_to_expiry"],
        item["success"], item["isProfit"], item["profitPercent"], item["average_fill"], round(item["max_avg_price"], 2), round(item["min_avg_price"], 2),
        item["interval_volume"], item["open_interest"], item["vol_oi"], item["otm"],
        item["bid_ask_percent"], item["premium"],
        item["multi_leg_volume"], item["url"], item["time_and_sales_url"]
    ])

loaded_table.sortby = "Type"
# Display the loaded PrettyTable
print("Loaded PrettyTable:")
print(loaded_table)


