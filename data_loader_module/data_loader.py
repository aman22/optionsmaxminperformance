# get filter data from UW (links in code) ... sample in file
# https://phx.unusualwhales.com/api/option_trades_v2?excluded_tags[]=dividend&is_multi_leg=true&issue_types[]=Common%20Stock&issue_types[]=ADR&limit=250&max_dte=151&min_premium=500000&watchlist_name=BTO%20100k%20%2B%20calls&ticker_symbol=GRFS
#

import sqlite3
import requests

from data_loader_module.optionsFilterModule import OptionsFlow, Tag
from helper import getDate, getChainDataFromUW

option_chain_url = "https://phx.unusualwhales.com/api/historic_chains/"


def getFilterDataFromUW():
    print('START UW')
    #url = "https://phx.unusualwhales.com/api/option_trades_v2?exclude_deep_itm=true&excluded_tags[]=dividend&excluded_tags[]=mid_side&excluded_tags[]=no_side&excluded_tags[]=bid_side&is_multi_leg=false&is_otm=true&issue_types[]=Common%20Stock&issue_types[]=ADR&limit=50&max_dte=151&min_premium=100000&opening=true&ticker_symbol=-CCJ&type=Calls&watchlist_name=BTO%20100k%20%2B%20calls&older_than=2024-02-01T20%3A05%3A27.468225Z"
    url = "https://phx.unusualwhales.com/api/option_trades_v2?excluded_tags[]=dividend&excluded_tags[]=mid_side&excluded_tags[]=ask_side&excluded_tags[]=no_side&is_multi_leg=false&issue_types[]=Common%20Stock&issue_types[]=ADR&limit=250&max_dte=60&min_premium=100000&opening=true&type=P&watchlist_name=STO%20Puts%20Bullish%2010k%2B&older_than=2024-02-02T14%3A30%3A03.707639Z"
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


def load_data():
    print('START')
    options_filter_data = getFilterDataFromUW()

    DB_PATH = './db/trade.db'
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    for row in options_filter_data.get('data'):
        options_data_instance = OptionsFlow(row)
        tag_list = []
        for tag in row.get('tags'):
            tag_instance = Tag(row.get('id'), tag)
            tag_list.append(tag_instance)
        insert_data(cursor, options_data_instance, tag_list)

    connection.commit()
    connection.close()


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


def insert_data(cursor, record, tag_list):
    insert_statement = '''
        INSERT OR IGNORE INTO options_flow (
            id, marketcap, stock_multi_vol, full_name, expiry, no_side_vol, nbbo_ask, theta, ask_vol, volume, price, ewma_nbbo_bid, open_interest,nbbo_bid, industry_type, implied_volatility, er_time, sector, multi_vol,gamma, rule_id, underlying_symbol, executed_at, strike, rho, vega,flow_alert_id, delta, size, ewma_nbbo_ask, option_type, underlying_price,next_earnings_date, upstream_condition_detail, bid_vol, canceled,exchange, theo, premium, option_chain_id, mid_vol
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        );
    '''

    cursor.execute(insert_statement, record.to_tuple())

    insert_tag_statement = '''
        INSERT OR IGNORE INTO tag (
            flow_id, name
        ) VALUES (
            ?,?
        );
    '''

    for tag in tag_list:
        cursor.execute(insert_tag_statement, tag.to_tuple())
