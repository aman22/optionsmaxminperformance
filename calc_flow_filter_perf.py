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
    token = "fGRTEucJ6qsRPtrdZubn_KWp30Lz3w9sqHf7gm-YVRMwr0Lbwef-TFxbyOEwbW9d"
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


def evaluateBTOCallsSuccess(options_chain, option_flow_row):
    # print('Trade execution date - ' + filter_data.get('executed_at') + ' ' + filter_data.get('option_chain_id'))
    trade_date = option_flow_row.expiry
    price = option_flow_row.price
    percentage_threshold = 1.5
    max_avg_price = float('-inf')  # Initialize with negative infinity to ensure any average price will be greater

    for day_data in options_chain:
        # print(day_data["last_tape_time"])
        if day_data["avg_price"] is not None:
            avg_price = float(day_data["avg_price"])
            if avg_price > max_avg_price:
                max_avg_price = avg_price

    option_flow_row.max_avg_price = max_avg_price
    # result.sector = day_data["industry_type"]
    # if max_avg_price > (price * percentage_threshold) and option_flow_row.success == 0:
    if max_avg_price > (price * percentage_threshold) :
        option_flow_row.success = 1
        # insert into DB the updated flag value
        update_success_flag(option_flow_row.id, max_avg_price)


def evaluateSTOPutsSuccess(options_chain, option_flow_row):
    # print('Trade execution date - ' + filter_data.get('executed_at') + ' ' + filter_data.get('option_chain_id'))
    if options_chain is not None:
        trade_date = option_flow_row.expiry
        price = option_flow_row.price
        percentage_threshold = 0.5
        max_avg_price = float('inf')  # Initialize with  infinity to ensure any average price will be lower in this case max is actually min

        for day_data in options_chain:
            # print(day_data["last_tape_time"])
            if day_data["avg_price"] is not None:
                avg_price = float(day_data["avg_price"])
                if avg_price < max_avg_price:
                    max_avg_price = avg_price

        option_flow_row.max_avg_price = max_avg_price

        if max_avg_price < (price * percentage_threshold) :
            # insert into DB the updated flag value
            update_success_flag(option_flow_row.id, max_avg_price)
    else:
        print('No option chain found for :' , option_flow_row.option_chain_id)

def update_success_flag(flow_id, max_avg_price):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    update_statement = '''
            UPDATE options_flow
            SET max_avg_price = ?,
                success = 1
            WHERE id = ?;
        '''
    cursor.execute(update_statement, (max_avg_price, flow_id))
    print("Success flag updated for flow ID:", flow_id)
    cursor.connection.commit()
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
            bid_vol, canceled, exchange, theo, premium, option_chain_id, mid_vol, success
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
    option_chain_data = getChainDataFromUW(history_url)
    # print(options_data)
    # print(isExpired(filter_data.get('expiry')))
    # def __init__(self, trade_date, expiration_date, contract, success, sector, max_avg_price, spot):
    # if option_flow_row.option_type == 'call' and option_flow_row.option_chain_id == 'AVAV240719C00185000':
    if option_flow_row.option_type == 'call':
        evaluateBTOCallsSuccess(option_chain_data.get('chains'), option_flow_row)
    else:
        evaluateSTOPutsSuccess(option_chain_data.get('chains'), option_flow_row)

# Example usage:
# json_file_path = "./data-1row"
json_file_path = "data_files/data"
option_chain_url = "https://phx.unusualwhales.com/api/historic_chains/"


def calculate_perf():
    options_data = get_filtered_rows_from_db()
    for row in options_data:
        evaluateOptionPerformance(row)

calculate_perf()
