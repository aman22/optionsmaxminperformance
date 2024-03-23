from datetime import datetime
from options_data import OptionsFlow
import requests
import sqlite3

# Configure the database path
DB_PATH = './db/trade.db'

def getDate(long_date):
    # Convert the string to a datetime object

    date_object = datetime.strptime(long_date, "%Y-%m-%dT%H:%M:%S.%f%z")
    # Extract the date
    formatted_date = date_object.strftime("%Y-%m-%d")
    # print("Extracted date:", formatted_date)
    return formatted_date

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


def process_each_option(options_data, option_flow_row):
    # print('Trade execution date - ' + filter_data.get('executed_at') + ' ' + filter_data.get('option_chain_id'))
    trade_date = getDate(option_flow_row.get('executed_at'))
    price = float(option_flow_row.get('price'))
    percentage_threshold = 1.5
    max_avg_price = float('-inf')  # Initialize with negative infinity to ensure any average price will be greater

    for day_data in options_data:
        # print(day_data["last_tape_time"])
        if day_data["avg_price"] is not None:
            avg_price = float(day_data["avg_price"])
            if avg_price > max_avg_price:
                max_avg_price = avg_price

    option_flow_row.max_avg_price = max_avg_price
    # result.sector = day_data["industry_type"]
    if max_avg_price > (price * percentage_threshold):
        option_flow_row.success = True
        # insert into DB the updated flag value
        update_success_flag(option_flow_row.get('id'))


def update_success_flag(id):
    def fetch_table_data():
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        update_statement = '''
            update options_flow set success = 1 where id = ?;
        '''

        cursor.execute(update_statement, (id,))
        print("Success flag updated for flow ID:", id)
        connection.close()


def get_filtered_rows_from_db():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        # f'SELECT executed_at, marketcap, option_chain_id, underlying_symbol, industry_type, expiry, price, volume, open_interest, option_type, '
        # f' underlying_price, size, premium, success FROM options_flow')
        '''
            SELECT id, marketcap, stock_multi_vol, full_name, expiry, no_side_vol, nbbo_ask, theta, ask_vol, volume,
            price, ewma_nbbo_bid, open_interest, nbbo_bid, industry_type, implied_volatility, er_time, sector,
            multi_vol, gamma, rule_id, underlying_symbol, executed_at, strike, rho, vega, flow_alert_id, delta,
            size, ewma_nbbo_ask, option_type, underlying_price, next_earnings_date, upstream_condition_detail,
            bid_vol, canceled, exchange, theo, premium, option_chain_id, mid_vol
            FROM options_flow;
        '''
    )

    rows = cursor.fetchall()

    options_flow_rows = []
    for row in rows:
        options_flow = OptionsFlow(*row)
        options_flow_rows.append(options_flow)

    connection.close()

    return options_flow_rows


def evaluateOptionPerformance(option_flow_row):
    history_url = option_chain_url + option_flow_row.option_chain_id + '?date=' + option_flow_row.expiry
    # print(history_url)
    options_data = getChainDataFromUW(history_url)
    # print(options_data)
    # print(isExpired(filter_data.get('expiry')))
    # def __init__(self, trade_date, expiration_date, contract, success, sector, max_avg_price, spot):
    process_each_option(options_data.get('chains'), option_flow_row)


# Example usage:
# json_file_path = "./data-1row"
json_file_path = "data_files/data"
option_chain_url = "https://phx.unusualwhales.com/api/historic_chains/"


def calculate_perf():
    options_data = get_filtered_rows_from_db()
    for row in options_data:
        evaluateOptionPerformance(row)
        break


calculate_perf()
