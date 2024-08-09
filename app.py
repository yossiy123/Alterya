from typing import List, Optional

from flask import Flask, jsonify

from wallet_handler import WalletHandler

API_KEY = "cqt_wFDJ6q9g4BRGdjGBqjdgjy7D4BtF"
wallet_handler = WalletHandler(api_key=API_KEY)

app = Flask(__name__)


@app.route('/assets/<string:chain_name>/<string:wallet_address>', methods=['GET'])
def get_all_assets_of_wallet_address(chain_name, wallet_address):
    assets: Optional[List] = None
    try:
        assets = wallet_handler.get_all_assets_of_wallet_address(chain_name, wallet_address)
    except Exception as ex:
        assets = None

    res = {"assets": assets, }

    return jsonify(res)


@app.route('/total_sum/<string:chain_name>/<string:wallet_address>', methods=['GET'])
def get_sum_balance_of_wallet_address(chain_name, wallet_address):
    balance_sum: Optional[float] = None
    try:
        balance_sum = wallet_handler.get_sum_balance_of_wallet_address(chain_name, wallet_address)
    except Exception as ex:
        balance_sum = None

    res = {"balance_sum": balance_sum, }

    return jsonify(res)


@app.route('/transactions/<string:chain_name>/<string:wallet_address>/<int:page_number>', methods=['GET'])
def get_transactions_of_wallet_address(chain_name, wallet_address, page_number):
    transactions: Optional[List] = None
    try:
        transactions = wallet_handler.get_transactions_with_paging(chain_name, wallet_address, page_number)
    except Exception as ex:
        transactions = None

    res = {"transactions": transactions, }

    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)
