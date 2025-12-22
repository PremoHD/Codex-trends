from flask import Flask, request, jsonify
from bitcoinlib.wallets import Wallet

app = Flask(__name__)
NETWORK = 'bitcoin'  # safe in Codespace

# Load or create wallet
WALLET_NAME = 'JustusCodeSpaceWallet'
try:
    wallet = Wallet(WALLET_NAME)
except:
    wallet = Wallet.create(WALLET_NAME, network=NETWORK)

# Routes
@app.route('/wallet/address')
def address():
    key = wallet.get_key()
    return jsonify({"address": key.address})

@app.route('/wallet/balance')
def balance():
    return jsonify({"balance": wallet.balance()})

@app.route('/wallet/send', methods=['POST'])
def send():
    data = request.json  # [{ "address": "...", "amount": 0.00001 }]
    outputs = [(x['address'], float(x['amount'])) for x in data]
    tx = wallet.transaction_create(outputs, fee='normal')
    wallet.transaction_sign(tx)
    wallet.transaction_send(tx)
    return jsonify({"txid": tx.txid})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)