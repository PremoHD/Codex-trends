from flask import Flask, request, jsonify, render_template
from bitcoinlib.wallets import Wallet
import requests

app = Flask(__name__, template_folder='templates')

# -----------------------------
# Wallet configuration
# -----------------------------
NETWORK = 'bitcoin'  # change to 'bitcoin' for mainnet
WALLET_NAME = 'JustusCodeSpaceWallet'

try:
    wallet = Wallet(WALLET_NAME)
except:
    wallet = Wallet.create(WALLET_NAME, network=NETWORK)

# -----------------------------
# Wallet routes
# -----------------------------
@app.route('/')
def dashboard():
    return render_template('index.html')  # HTML dashboard

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

# -----------------------------
# Faucet route (testnet only)
# -----------------------------
@app.route('/wallet/faucet')
def faucet():
    address = wallet.get_key().address
    faucet_url = 'https://testnet-faucet.mempool.co/api/faucet'
    try:
        resp = requests.post(faucet_url, json={"address": address})
        return jsonify({"status": "requested", "response": resp.json()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)