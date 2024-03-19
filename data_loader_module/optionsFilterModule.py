import json


class Tag:
    def __init__(self, id, name):
        self.flow_id = id
        self.name = name

    def to_dict(self):
        return vars(self)

    def to_tuple(self):
        return tuple(vars(self).values())

    def print_info(self):
        for key, value in self.to_dict().items():
            print(f"{key}: {value}")


class OptionsFlow:
    def __init__(self, data):
        self.id = data.get("id")
        self.marketcap = data.get("marketcap")
        self.stock_multi_vol = data.get("stock_multi_vol")
        self.full_name = data.get("full_name")
        self.expiry = data.get("expiry")
        self.no_side_vol = data.get("no_side_vol")
        self.nbbo_ask = data.get("nbbo_ask")
        self.theta = data.get("theta")
        # self.report_flags = data.get("report_flags", [])
        self.ask_vol = data.get("ask_vol")
        self.volume = data.get("volume")
        self.price = data.get("price")
        self.ewma_nbbo_bid = data.get("ewma_nbbo_bid")
        self.open_interest = data.get("open_interest")
        self.nbbo_bid = data.get("nbbo_bid")
        self.industry_type = data.get("industry_type")
        self.implied_volatility = data.get("implied_volatility")
        self.er_time = data.get("er_time")
        self.sector = data.get("sector")
        self.multi_vol = data.get("multi_vol")
        self.gamma = data.get("gamma")
        # self.tags = data.get("tags", [])
        self.rule_id = data.get("rule_id")
        self.underlying_symbol = data.get("underlying_symbol")
        self.executed_at = data.get("executed_at")
        self.strike = data.get("strike")
        self.rho = data.get("rho")
        self.vega = data.get("vega")
        self.flow_alert_id = data.get("flow_alert_id")
        self.delta = data.get("delta")
        self.size = data.get("size")
        self.ewma_nbbo_ask = data.get("ewma_nbbo_ask")
        self.option_type = data.get("option_type")
        self.underlying_price = data.get("underlying_price")
        self.next_earnings_date = data.get("next_earnings_date")
        self.upstream_condition_detail = data.get("upstream_condition_detail")
        self.bid_vol = data.get("bid_vol")
        self.canceled = data.get("canceled", False)
        self.exchange = data.get("exchange")
        self.theo = data.get("theo")
        self.premium = data.get("premium")
        self.option_chain_id = data.get("option_chain_id")
        self.mid_vol = data.get("mid_vol")

    def to_dict(self):
        return vars(self)

    def print_info(self):
        print("Options Flow Information:")
        for key, value in self.to_dict().items():
            print(f"{key}: {value}")

    def to_tuple(self):
        return tuple(vars(self).values())

# # Example usage:
# options_filter_data_json = {...}  # Your options data JSON
# options_filter_data_instance = OptionsFilterData(options_filter_data_json)
#
# # Accessing attributes
# print(options_data_instance.full_name)
# print(options_data_instance.volume)
#
# # Convert object to dictionary
# options_data_dict = options_data_instance.to_dict()
# print(json.dumps(options_data_dict, indent=2))
