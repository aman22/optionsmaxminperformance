import json
from prettytable import PrettyTable
from collections import Counter
from helper import getChainDataFromUW
from helper import extract_characters_until_first_number
from helper import isExpired
from helper import getDate
from options_data import OptionsData
import re

import time
import requests

class Result:
    def __init__(self, trade_date, expiration_date, contract, success, sector, max_avg_price, spot):
        #self.ticker = extract_characters_until_first_number(contract)
        self.trade_date = trade_date
        self.expiration_date = expiration_date
        self.contract = contract
        self.success = success
        self.spot = spot
        self.max_avg_price = max_avg_price
        self.sector = sector

    def extract_characters_until_first_number(input_string):
        match = re.search(r'^([^0-9]+)', input_string)
        if match:
            return match.group(1)
        else:
            return input_string
    def __str__(self):
        return (f"{extract_characters_until_first_number(self.contract)}, {self.trade_date}, {self.expiration_date}, {self.contract}, {self.success}, "
                f"{self.spot}, {self.max_avg_price}, {self.sector}")

# def process_each_option(options_data, filter_data, result):
def process_each_option(options_data):

    #print('Trade execution date - ' + filter_data.get('executed_at') + ' ' + filter_data.get('option_chain_id'))
    trade_date = getDate(filter_data.get('executed_at'))
    price = float(filter_data.get('price'))
    percentage_threshold = 1.5
    max_avg_price = float('-inf')  # Initialize with negative infinity to ensure any average price will be greater

    for day_data in options_data:
        # print(day_data["last_tape_time"])
        if(day_data["avg_price"] is not None):
            avg_price = float(day_data["avg_price"])
            if avg_price > max_avg_price:
                max_avg_price = avg_price

    result.max_avg_price = max_avg_price
    #result.sector = day_data["industry_type"]
    if max_avg_price > (price * percentage_threshold):
        result.success = True


# Example usage:
# json_file_path = "./data-1row"
json_file_path = "./data"
option_chain_url="https://phx.unusualwhales.com/api/historic_chains/"

def extract_key_values(description):
    # Use regular expressions to extract key-values from the description
    matches = re.findall(r'\*\*(.*?)\*\*: (.*?)\n', description)
    return dict(matches)

def read_and_print_json():
    print(f"START---")
    file_path = "./live_options_flow_data"
    with open(file_path, 'r') as file:
        json_data = json.load(file)

    # Extract and transform descriptions from each JSON object
    table = PrettyTable()
    table.field_names = [
        "Alert Type", "Type","Alert Time","Ticker", "Strike",  "Expiration", "DTE", "Interval Volume",
        "Open Interest", "Vol/OI", "OTM", "Bid/Ask %", "Premium", "Average Fill", "Multi-leg Volume", "URL", "Time and Sales URL"
    ]
    discord_alerts = [extract_discord_alerts(obj) for obj in json_data]
    for discord_alert in discord_alerts:
        options_data = OptionsData(discord_alert.title, discord_alert.timestamp, discord_alert.description)
        table.add_row([
            discord_alert.title, options_data.option_type, discord_alert.timestamp, options_data.ticker, options_data.strike, options_data.expiration_date, options_data.days_to_expiry,
             options_data.interval_volume, options_data.open_interest, options_data.vol_oi,
            f"{options_data.otm}%", options_data.bid_ask_percent, options_data.premium, options_data.average_fill, options_data.multi_leg_volume, options_data.url, options_data.time_and_sales_url
        ])

    # for option in options_data:
    #     print(option)
    print(table)

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

