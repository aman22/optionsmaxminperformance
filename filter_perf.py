import json
from prettytable import PrettyTable
from collections import Counter
from helper import getChainDataFromUW
from helper import isExpired
from helper import getDate

import time
import requests


def process_options_data(options_data, filter_data):

    trade_date = getDate(filter_data.get('executed_at'))
    price = filter_data.get('price')
    percentage_threshold = 1.5

    max_avg_price = float('-inf')  # Initialize with negative infinity to ensure any average price will be greater

    for day_data in options_data:
        print(day_data["last_tape_time"])
        avg_price = float(day_data["avg_price"])

        if avg_price > max_avg_price:
            max_avg_price = avg_price

    if max_avg_price > (price * percentage_threshold):
        print("True")
    else:
        print("False")

def read_and_print_json(file_path):
    print(f"START---")
    try:
        # Open the JSON file for reading
        with open(file_path, 'r') as file:
            # Load the JSON data
            print(f"FILE OPEN ---")
            fileData = json.load(file)
            # alert_array = fileData.get('alerts')

            for filter_data in fileData:
                history_url = option_chain_url + filter_data.get('option_chain_id') + '?date=' + filter_data.get('expiry')
                print(history_url)
                options_data = getChainDataFromUW(history_url)
                print(options_data)
                print(isExpired(filter_data.get('expiry')))
                process_options_data(options_data.get('chains'), filter_data)


            else:
                print("Error: JSON data is not an array.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

# Example usage:
json_file_path = "/Users/amandetail/PycharmProjects/optionsmaxminperformance/data-1row"
option_chain_url="https://phx.unusualwhales.com/api/historic_chains/"

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

