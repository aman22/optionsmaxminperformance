import json, csv
from prettytable import PrettyTable
from collections import Counter
from helper import getChainDataFromUW
from helper import extract_characters_until_first_number
from helper import isExpired
from helper import getDate, convert_to_desired_format
from options_data import OptionsData
from options_data import options_data_serializer
from datetime import datetime
import re
import time
import requests
def process_each_option(options_data, discord_alert):

    history_url = "https://phx.unusualwhales.com/api/historic_chains/" + options_data.url.split('=')[1]
    # print(history_url)
    options_chain = getChainDataFromUW(history_url)
    options_data.timestamp = convert_to_desired_format(options_data.timestamp)

    timestamp_obj = datetime.strptime(options_data.timestamp, '%Y-%m-%d %H:%M:%S')
    trade_date = datetime.strftime(timestamp_obj, '%m/%d/%Y')
    max_avg_price = float('-inf')  # Initialize with negative infinity to ensure any average price will be greater
    min_avg_price = float('inf')

    sorted_chains = sorted(options_chain['chains'], key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))

    for day_data in sorted_chains:
        trade_dt = datetime.strptime(trade_date, "%m/%d/%Y")
        chain_dt = datetime.strptime(day_data["date"], "%Y-%m-%d")
        if day_data["avg_price"] is not None and  chain_dt > trade_dt :
            avg_price = float(day_data["avg_price"])
            if avg_price > max_avg_price:
                max_avg_price = avg_price
            if avg_price < min_avg_price:
                min_avg_price = avg_price

    options_data.max_avg_price = max_avg_price
    options_data.min_avg_price = min_avg_price

    if (max_avg_price > (float(options_data.average_fill) * 1.5) and "Ask" in discord_alert.title) or (max_avg_price < (options_data.average_fill * 0.9) and "Bid" in discord_alert.title):
        options_data.success = True
    if min_avg_price < (float(options_data.average_fill) * 0.5) and "Bid" in discord_alert.title:
        options_data.success = True

json_file_path = "data_files/data"
option_chain_url="https://phx.unusualwhales.com/api/historic_chains/"

def extract_key_values(description):
    # Use regular expressions to extract key-values from the description
    matches = re.findall(r'\*\*(.*?)\*\*: (.*?)\n', description)
    return dict(matches)

def read_and_print_json():
    print(f"START---")
    file_path = "data_files/live_options_flow_data"
    with open(file_path, 'r') as file:
        json_data = json.load(file)

    # Extract and transform descriptions from each JSON object
    table = PrettyTable()
    table.field_names = [
        "Success?", "Profit?", "Profit%", "Alert Type", "Type","Alert Time","Ticker", "Strike",  "Expiration", "DTE", "Average Fill", "Max Price", "Min Price", "Interval Volume",
        "Open Interest", "Vol/OI", "OTM", "Bid/Ask %", "Premium", "Multi-leg Volume", "URL", "Time and Sales URL"
    ]
    discord_alerts = [extract_discord_alerts(obj) for obj in json_data]
    options_list =[]
    for discord_alert in discord_alerts:
        options_data = OptionsData(discord_alert.title, discord_alert.timestamp, discord_alert.description)
        process_each_option(options_data, discord_alert)
        #BTO Call or Put
        if "Ask" in options_data.title:
            options_data.isProfit = options_data.max_avg_price > options_data.average_fill
            options_data.profitPercent = round(options_data.max_avg_price/options_data.average_fill*100, 2)
        #STO Call OR Put
        else:
            options_data.isProfit = options_data.min_avg_price < options_data.average_fill
            options_data.profitPercent = round(options_data.min_avg_price / options_data.average_fill * 100, 2)
        table.add_row([
            options_data.success, options_data.isProfit, options_data.profitPercent, discord_alert.title,
            options_data.option_type, options_data.timestamp, options_data.ticker, options_data.strike,
            options_data.expiration_date,
            options_data.days_to_expiry, options_data.average_fill, round(options_data.max_avg_price, 2), round(options_data.min_avg_price, 2),
            options_data.interval_volume, options_data.open_interest, options_data.vol_oi,
            f"{options_data.otm}%", options_data.bid_ask_percent, options_data.premium,
            options_data.multi_leg_volume, options_data.url, options_data.time_and_sales_url
        ])

        options_list.append(options_data)


    # for option in options_data:
    #     print(option)
    serialized_data = [options_data_serializer(instance) for instance in options_list]

    # Write the list of dictionaries as JSON to a file
    with open('output.json', 'w') as json_file:
        json.dump(serialized_data, json_file, indent=2)


def extract_options_data(data):
    options_data = OptionsData(data)
    return options_data

def extract_discord_alerts(data):
    embed_data = data.get('embeds', [])[0]
    discord_alert_instance = DiscordAlert(embed_data)
    return discord_alert_instance

class DiscordAlert:
    def __init__(self, data):
        self.title = data.get('title', '')
        self.description = data.get('description', '')
        self.timestamp = data.get('timestamp', '')

    def __str__(self):
        return f"Title: {self.title}\nDescription: {self.description}\nTimestamp: {self.timestamp}"

read_and_print_json()

