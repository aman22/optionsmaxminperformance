
import requests
from datetime import datetime
import re

def getChainDataFromUW(url):
    token = "lqMAxR0P9Ty4EmAASMeHopNZbP9OJqzaf468XJVhuu35"
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Assuming the response is in JSON format
            data = response.json()
            return data
        else:
            print(f"Request failed with status code {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error during the request: {e}")
        return None

def get_live_options_flow():

    token = "lqMAxR0P9Ty4EmAASMeHopNZbP9OJqzaf468XJVhuu35"
    url=""
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Assuming the response is in JSON format
            data = response.json()
            return data
        else:
            print(f"Request failed with status code {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error during the request: {e}")
        return None

def getDate(long_date):
    # Convert the string to a datetime object

    date_object = datetime.strptime(long_date, "%Y-%m-%dT%H:%M:%S.%f%z")
    # Extract the date
    formatted_date = date_object.strftime("%Y-%m-%d")
    # print("Extracted date:", formatted_date)
    return formatted_date
# //%Y-%m-%dT%H:%M:%S.%f%z
def convert_to_desired_format(timestamp_str):
    try:
        # Attempt to parse with milliseconds format
        timestamp_obj = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%f%z')
    except ValueError:
        try:
            # Attempt to parse without milliseconds format
            timestamp_obj = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S%z')
        except ValueError:
            raise ValueError("Invalid timestamp format")

    # Format the timestamp as '%Y-%m-%d %H:%M:%S'
    formatted_timestamp = timestamp_obj.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_timestamp
def isExpired(string_date):
    try:
        date_object = datetime.strptime(string_date, "%Y-%m-%d")

        # Get the current date
        current_date = datetime.now().date()

        # Compare the dates
        return date_object.date() < current_date
    except ValueError:
        # Handle invalid date formats
        print("Invalid date format")
        return False

def extract_characters_until_first_number(input_string):
    match = re.search(r'^([^0-9]+)', input_string)
    if match:
        return match.group(1)
    else:
        return input_string
