from flask import Flask, request, jsonify, render_template
from bitcoinlib.wallets import Wallet
import requests
import json

app = Flask(__name__, template_folder='templates')

# -----------------------------
# Wallet config
# -----------------------------
NETWORK = 'testnet'  # safe for testing
WALLET_NAME = 'JustusCodeSpaceWallet'

try:
    wallet = Wallet(WALLET_NAME)
except:
    wallet = Wallet.create(WALLET_NAME, network=NETWORK)

# -----------------------------
# Routes
# -----------------------------
@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/wallet/address')
def address():
    key = wallet.get_key()
    return jsonify({"address": key.address})

@app.route('/wallet/balance')
def balance():
    return jsonify({"balance": wallet.balance()})

@app.route('/wallet/faucet')
def faucet():
    address = wallet.get_key().address
    faucet_url = 'https://testnet-faucet.mempool.co/api/faucet'
    try:
        resp = requests.post(faucet_url, json={"address": address})
        return jsonify({"status": "requested", "response": resp.json()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/wallet/send', methods=['POST'])
def send():
    data = request.json  # [{"address":"...", "amount":0.00001}, ...]
    if len(data) > 100:
        return jsonify({"error": "Max 100 addresses allowed per transaction"}), 400

    outputs = [(x['address'], float(x['amount'])) for x in data]
    tx = wallet.transaction_create(outputs, fee='normal')
    wallet.transaction_sign(tx)
    wallet.transaction_send(tx)
    return jsonify({"txid": tx.txid})

# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)