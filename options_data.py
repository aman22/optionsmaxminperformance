import re
from datetime import datetime

# class OptionsData:
#     def __init__(self, title, timestamp, input_string):
#         self.success = False
#         self.isProfit = False
#         self.profitPercent = 0.0
#         self.title = title
#         self.timestamp = timestamp
#         self.url = None
#         self.time_and_sales_url = None
#         self.interval_volume = 0
#         self.open_interest = 0
#         self.vol_oi = 0
#         self.otm = 0
#         self.bid_ask_percent = "0/0"
#         self.premium = 0.0
#         self.average_fill = 0.0
#         self.multi_leg_volume = "0%"
#         self.ticker = None
#         self.strike = None
#         self.option_type = None
#         self.expiration_date = None
#         self.days_to_expiry = None
#         self.max_avg_price = 0.0
#         self.min_avg_price = 0.0
#         if input_string:
#             self.populate_from_string(input_string)
#
#     def populate_from_string(self, input_string):
#         # Extract URL and Time and Sales URL
#         match_url = re.search(r'\*\*\[([^\]]+)\]\(([^)]+)\)', input_string)
#         if match_url:
#             self.url = match_url.group(2)
#
#         match_time_and_sales_url = re.search(r'\[Time and sales\]\(([^)]+)\)', input_string)
#         if match_time_and_sales_url:
#             self.time_and_sales_url = match_time_and_sales_url.group(1)
#
#         # Extract other attributes
#         match_interval_volume = re.search(r'(Interval|Overall) Volume: (\d{1,3}(?:,\d{3})*(?:\.\d+)?|0)', input_string)
#         if match_interval_volume:
#             attribute_type, interval_volume_str = match_interval_volume.groups()
#             interval_volume_str = interval_volume_str.replace(',', '')  # Remove commas
#             try:
#                 self.interval_volume = int(float(interval_volume_str))
#             except ValueError:
#                 self.interval_volume = 0  # Set to 0 in case of conversion issues
#
#         match_open_interest = re.search(r'Open Interest: (\d+)', input_string)
#         if match_open_interest:
#             self.open_interest = int(match_open_interest.group(1))
#
#         match_vol_oi = re.search(r'Vol/OI: ([\d.]+|-)', input_string)
#         if match_vol_oi:
#             vol_oi_str = match_vol_oi.group(1)
#             self.vol_oi = float(vol_oi_str) if vol_oi_str != "-" else None
#
#         match_otm = re.search(r'OTM: (\d+)%', input_string)
#         if match_otm:
#             self.otm = int(match_otm.group(1))
#
#         match_bid_ask_percent = re.search(r'Bid/Ask %: (\d+)/(\d+)', input_string)
#         if match_bid_ask_percent:
#             self.bid_ask_percent = f"{match_bid_ask_percent.group(1)}/{match_bid_ask_percent.group(2)}"
#
#         match_premium = re.search(r'Premium: \$([\d,]+(?:\.\d{2})?)', input_string)
#         if match_premium:
#             self.premium = float(match_premium.group(1).replace(',', ''))
#
#         match_average_fill = re.search(r'Average Fill: \$([\d,]+(?:\.\d{2})?)', input_string)
#         if match_average_fill:
#             self.average_fill = float(match_average_fill.group(1).replace(',', ''))
#
#         match_multi_leg_volume = re.search(r'Multi-leg Volume: (\d+%)', input_string)
#         if match_multi_leg_volume:
#             self.multi_leg_volume = match_multi_leg_volume.group(1)
#
#         # Extract Ticker, Strike, Type, expiration date, and days to expiry (DTE) from the URL
#         match_ticker_info = re.search(r'(\w+) (\d+(?:\.\d+)?) ([CP]) (\d{2}/\d{2}/\d{4})(?: \((\d+) DTE\))?',
#                                       match_url.group(1))
#         match_timestamp = re.search(r'timestamp": "(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})', self.timestamp)
#         if match_timestamp:
#             timestamp_str = match_timestamp.group(1)
#             timestamp_datetime = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S")
#             self.timestamp = timestamp_datetime.strftime("%Y-%m-%d %H:%M")
#
#         if match_ticker_info:
#             self.ticker, self.strike, self.option_type, self.expiration_date, self.days_to_expiry = match_ticker_info.groups()
#
#
#     def __str__(self):
#         return f"{self.title},{self.timestamp},{self.ticker}, {self.strike}, {self.option_type}, {self.expiration_date}, {self.days_to_expiry}, " \
#                f"{self.interval_volume}, {self.open_interest}, {self.vol_oi}, " \
#                f"{self.otm}, {self.bid_ask_percent}, {self.premium}, {self.average_fill}, {self.multi_leg_volume}, {self.url}, {self.time_and_sales_url}"
#
# def convert_to_desired_format(timestamp_str):
#     try:
#         # Attempt to parse with milliseconds format
#         timestamp_obj = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%f%z')
#     except ValueError:
#         try:
#             # Attempt to parse without milliseconds format
#             timestamp_obj = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S%z')
#         except ValueError:
#             raise ValueError("Invalid timestamp format : ", timestamp_str)
#
#     # Format the timestamp as '%Y-%m-%d %H:%M:%S'
#     formatted_timestamp = timestamp_obj.strftime('%Y-%m-%d %H:%M:%S')
#     return formatted_timestamp
# # Example usage:
# # input_string = "...your input string..."
# # print(options_data)
# def options_data_serializer(obj):
#     if isinstance(obj, OptionsData):
#         return {
#             "success": obj.success,
#             "isProfit": obj.isProfit,
#             "profitPercent": obj.profitPercent,
#             "title": obj.title,
#             "timestamp": obj.timestamp,
#             "url": obj.url,
#             "time_and_sales_url": obj.time_and_sales_url,
#             "interval_volume": obj.interval_volume,
#             "open_interest": obj.open_interest,
#             "vol_oi": obj.vol_oi,
#             "otm": obj.otm,
#             "bid_ask_percent": obj.bid_ask_percent,
#             "premium": obj.premium,
#             "average_fill": obj.average_fill,
#             "multi_leg_volume": obj.multi_leg_volume,
#             "ticker": obj.ticker,
#             "strike": obj.strike,
#             "option_type": obj.option_type,
#             "expiration_date": obj.expiration_date,
#             "days_to_expiry": obj.days_to_expiry,
#             "max_avg_price": obj.max_avg_price,
#             "min_avg_price": obj.min_avg_price,
#         }
#     raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

class OptionsFlow:
    def __init__(self, id, marketcap, stock_multi_vol, full_name, expiry, no_side_vol,
                 nbbo_ask, theta, ask_vol, volume, price, ewma_nbbo_bid, open_interest,
                 nbbo_bid, industry_type, implied_volatility, er_time, sector, multi_vol,
                 gamma, rule_id, underlying_symbol, executed_at, strike, rho, vega,
                 flow_alert_id, delta, size, ewma_nbbo_ask, option_type, underlying_price,
                 next_earnings_date, upstream_condition_detail, bid_vol, canceled, exchange,
                 theo, premium, option_chain_id, mid_vol, success):
        self.id = id
        self.marketcap = marketcap
        self.stock_multi_vol = stock_multi_vol
        self.full_name = full_name
        self.expiry = expiry
        self.no_side_vol = no_side_vol
        self.nbbo_ask = nbbo_ask
        self.theta = theta
        self.ask_vol = ask_vol
        self.volume = volume
        self.price = price
        self.ewma_nbbo_bid = ewma_nbbo_bid
        self.open_interest = open_interest
        self.nbbo_bid = nbbo_bid
        self.industry_type = industry_type
        self.implied_volatility = implied_volatility
        self.er_time = er_time
        self.sector = sector
        self.multi_vol = multi_vol
        self.gamma = gamma
        self.rule_id = rule_id
        self.underlying_symbol = underlying_symbol
        self.executed_at = executed_at
        self.strike = strike
        self.rho = rho
        self.vega = vega
        self.flow_alert_id = flow_alert_id
        self.delta = delta
        self.size = size
        self.ewma_nbbo_ask = ewma_nbbo_ask
        self.option_type = option_type
        self.underlying_price = underlying_price
        self.next_earnings_date = next_earnings_date
        self.upstream_condition_detail = upstream_condition_detail
        self.bid_vol = bid_vol
        self.canceled = canceled
        self.exchange = exchange
        self.theo = theo
        self.premium = premium
        self.option_chain_id = option_chain_id
        self.mid_vol = mid_vol
        self.success = success
