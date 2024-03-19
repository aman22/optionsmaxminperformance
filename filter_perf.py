import json
from prettytable import PrettyTable
from collections import Counter
from helper import getChainDataFromUW
from helper import extract_characters_until_first_number
from helper import isExpired
from helper import getDate
import re

import time
import requests


class Result:
    def __init__(self, trade_date, expiration_date, contract, success, sector, max_avg_price, spot):
        # self.ticker = extract_characters_until_first_number(contract)
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
        return (
            f"{extract_characters_until_first_number(self.contract)}, {self.trade_date}, {self.expiration_date}, {self.contract}, {self.success}, "
            f"{self.spot}, {self.max_avg_price}, {self.sector}")


def process_each_option(options_data, filter_data, result):
    # print('Trade execution date - ' + filter_data.get('executed_at') + ' ' + filter_data.get('option_chain_id'))
    trade_date = getDate(filter_data.get('executed_at'))
    price = float(filter_data.get('price'))
    percentage_threshold = 1.5
    max_avg_price = float('-inf')  # Initialize with negative infinity to ensure any average price will be greater

    for day_data in options_data:
        # print(day_data["last_tape_time"])
        if (day_data["avg_price"] is not None):
            avg_price = float(day_data["avg_price"])
            if avg_price > max_avg_price:
                max_avg_price = avg_price

    result.max_avg_price = max_avg_price
    # result.sector = day_data["industry_type"]
    if max_avg_price > (price * percentage_threshold):
        result.success = True


def read_and_print_json(file_path):
    print(f"START---")
    results = []
    try:
        # Open the JSON file for reading
        with open(file_path, 'r') as file:
            # Load the JSON data
            print(f"FILE OPEN ---")
            fileData = json.load(file)
            # alert_array = fileData.get('alerts')

            for filter_data in fileData:
                calcAlertPerformance(filter_data, results)
                # break
            else:
                print("Error: JSON data is not an array.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")


def calcAlertPerformance(filter_data, results):
    history_url = option_chain_url + filter_data.get('option_chain_id') + '?date=' + filter_data.get('expiry')
    # print(history_url)
    options_data = getChainDataFromUW(history_url)
    # print(options_data)
    # print(isExpired(filter_data.get('expiry')))
    # def __init__(self, trade_date, expiration_date, contract, success, sector, max_avg_price, spot):
    result = Result(filter_data.get('executed_at'), filter_data.get('expiry'), filter_data.get('option_chain_id'),
                    False, filter_data.get('sector'), 0.0, filter_data.get('price'))
    process_each_option(options_data.get('chains'), filter_data, result)
    results.append(result)
    print(result)


# Example usage:
# json_file_path = "./data-1row"
json_file_path = "data_files/data"
option_chain_url = "https://phx.unusualwhales.com/api/historic_chains/"


def count_distinct_values(table, column_name):
    # Get the index of the specified column
    column_index = table.field_names.index(column_name) if column_name in table.field_names else -1

    if column_index != -1:
        # Extract values from the specified column
        column_values = [row[column_index] for row in table.rows]

        # Count distinct values using Counter
        distinct_values_count = Counter(column_values)

        # Print the results
        print(f"Distinct values in '{column_name}':")
        for value, count in distinct_values_count.items():
            print(f"{value}: {count}")
    else:
        print(f"Error: Column '{column_name}' not found in the table.")


# Replace with the actual path to your JSON file
read_and_print_json(json_file_path)


class Option:
    def __init__(self, ticker, strike, option_type, expiration_date, days_to_expiry, link, vol, oi, otm, bid, ask,
                 premium, price, multi):
        self.ticker = ticker
        self.strike = strike
        self.option_type = option_type
        self.expiration_date = expiration_date
        self.days_to_expiry = days_to_expiry
        self.link = link
        self.vol = vol
        self.oi = oi
        self.otm = otm
        self.bid = bid
        self.ask = ask
        self.premium = premium
        self.price = price
        self.multi = multi

    def print_comma_separated_values(self):
        values = [
            str(self.ticker), str(self.strike), str(self.option_type),
            str(self.expiration_date), str(self.days_to_expiry), str(self.link),
            str(self.vol), str(self.oi), str(self.otm), str(self.bid),
            str(self.ask), str(self.premium), str(self.price), str(self.multi)
        ]
        print(', '.join(values))
