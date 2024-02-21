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

def process_each_option(options_data, filter_data, result):

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
                #break
            else:
                print("Error: JSON data is not an array.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

# Example usage:
# json_file_path = "./data-1row"
json_file_path = "./data"
option_chain_url="https://phx.unusualwhales.com/api/historic_chains/"

def extract_key_values(description):
    # Use regular expressions to extract key-values from the description
    matches = re.findall(r'\*\*(.*?)\*\*: (.*?)\n', description)
    return dict(matches)
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
def read_and_print_json():
    print(f"START---")
    file_path = "./live_options_flow_data"
    with open(file_path, 'r') as file:
        json_data = json.load(file)

    # Extract and transform descriptions from each JSON object
    transformed_descriptions = [extract_and_transform_description(obj) for obj in json_data]

    table = PrettyTable()
    table.field_names = ["Index", "Transformed Description"]

    # Add data to the table
    for i, transformed_description in enumerate(transformed_descriptions, 1):
        table.add_row([i, transformed_description])

    # Print the table
    print(table)


def extract_and_transform_description(json_object):
    embeds = json_object.get("embeds", [{}])
    description = embeds[0].get("description", "")
    # Transform the description attributes to comma-separated values
    transformed_description = description.replace('\n', ', ')
    return transformed_description

read_and_print_json()

