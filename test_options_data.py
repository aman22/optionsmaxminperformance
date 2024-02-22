import re
import unittest
from discord_alert_perf import OptionsData

class TestOptionsData(unittest.TestCase):
    def setUp(self):
        # Replace this with the actual data you want to test
        self.options_data_string = "**[ENPH 122 P 02/23/2024 (3 DTE)](https://unusualwhales.com/flow/option_chains?chain=ENPH240223P00122000)**\n" \
                                  "[Time and sales](https://unusualwhales.com/live-options-flow?limit=50&chain=ENPH240223P00122000)\n" \
                                  "Interval Volume: 1,001\nOpen Interest: 199\nVol/OI: 5.03\nOTM: 4%\nBid/Ask %: 0/100\n" \
                                  "Premium: $173,111\nAverage Fill: $1.73\nMulti-leg Volume: 0%"

    def test_options_data(self):
        options_data = OptionsData("url_placeholder", "time_and_sales_url_placeholder", 0, 0, 0, 0, "0/0", "$0", "$0", "0%")
        options_data.populate_from_string(self.options_data_string)

        # Test the extracted values
        self.assertEqual(options_data.ticker, "ENPH")
        self.assertEqual(options_data.strike, "122")
        self.assertEqual(options_data.option_type, "P")
        self.assertEqual(options_data.expiration_date, "02/23/2024")
        self.assertEqual(options_data.days_to_expiry, "3")

if __name__ == '__main__':
    unittest.main()