from bitcoinlib.wallets import Wallet
from config import NETWORK, WALLET_NAME

def load_wallet():
    try:
        return Wallet(WALLET_NAME)
    except:
        return Wallet.create(WALLET_NAME, network=NETWORK)

def get_receive_address(wallet=None):
    if wallet is None:
        wallet = load_wallet()
    return wallet.get_key().address

def get_balance(wallet=None):
    if wallet is None:
        wallet = load_wallet()
    return wallet.balance()

def send_batch(outputs, wallet=None):
    if wallet is None:
        wallet = load_wallet()
    tx = wallet.transaction_create(outputs, fee='normal')
    wallet.transaction_sign(tx)
    wallet.transaction_send(tx)
    return tx.txid