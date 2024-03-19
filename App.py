from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Configure the database path
DB_PATH = '/Users/Aman/trade.db'


@app.route('/')
def index():
    # Fetch column names and data from the options_flow table
    options_data = fetch_table_data('options_flow')
    return render_template('index.html', options_data=options_data)


def fetch_table_data(table_name):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(f'SELECT executed_at, marketcap, option_chain_id, underlying_symbol, industry_type, expiry, price, volume, open_interest, option_type, '
                   f' underlying_price, size, premium FROM {table_name}')

    options_data = cursor.fetchall()

    connection.close()

    return options_data


if __name__ == '__main__':
    app.run(debug=True)
# <th>Executed At</th>
#                 <th>Market Cap</th>
#                 <th>Option Chain ID</th>
#                 <th>Full Name</th>
#                 <th>Industry Type</th>
#                 <th>Expiry</th>
#                 <th>Price</th>
#                 <th>Volume</th>
#                 <th>Open Interest</th>
#                 <th>Option Type</th>
#                 <th>Underlying Price</th>
#                 <th>Size</th>
#                 <th>Premium</th>