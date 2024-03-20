# Before you run this make sure you have Flask installed... below are the steps how to do it
# Pycharm, you can go to Pycharm->Settings->Project _> Python interpreter, click the green + button (Install), type in flask,
# select Flask from the list then click Install Package.
# After installation, you will get the message saying flask installed successfully.

from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Configure the database path
DB_PATH = './db/trade.db'


@app.route('/')
def index():
    # Fetch column names and data from the options_flow table
    options_data = fetch_table_data('options_flow')
    return render_template('index.html', options_data=options_data)


def fetch_table_data(table_name):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(f'SELECT executed_at, marketcap, option_chain_id, underlying_symbol, industry_type, expiry, price, volume, open_interest, option_type, '
                   f' underlying_price, size, premium, success FROM {table_name}')

    options_data = cursor.fetchall()
    for row in options_data:
        evaluateOptionPerformance(row)
        break
    connection.close()

    return options_data


if __name__ == '__main__':
    app.run(debug=True)

def evaluateOptionsPerformance(option):
    print(option)