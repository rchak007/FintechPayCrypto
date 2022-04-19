# Cryptocurrency Wallet
################################################################################

# This file contains the Ethereum transaction functions

################################################################################
# Imports
import os

import requests
from bip44 import Wallet
from coincurve import PrivateKey
from dotenv import load_dotenv
from web3 import Account, middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy

load_dotenv()

################################################################################
# Wallet functionality

def generate_account():
    """Create a digital wallet and Ethereum account from a mnemonic seed phrase."""
    # Fetch mnemonic from environment variable.
    mnemonic = os.getenv("MNEMONIC")

    # Create Wallet Object
    wallet = Wallet(mnemonic)
    Account.enable_unaudited_hdwallet_features()
    account_mnem1 = Account.from_mnemonic(mnemonic, account_path="m/44'/60'/0'/0/0")
    account_mnem2 = Account.from_mnemonic(mnemonic, account_path="m/44'/60'/0'/0/1")
    account_mnem3 = Account.from_mnemonic(mnemonic, account_path="m/44'/60'/0'/0/2")
    print("address 0 ", account_mnem1.address)
    print("address 1 ", account_mnem2.address)
    print("address 2 ", account_mnem3.address)
    # print("address 0 private key ", account_mnem1.privateKey)
    # print("address 1 private key", account_mnem2.privateKey)
    # print("address 2 private key ", account_mnem3.privateKey)
    account_mnem3_private = account_mnem3.privateKey
    # Derive Ethereum Private Key
    private, public = wallet.derive_account("eth")
    # print ("private key in hex= ", private.hex())
    # print ("Public key = ", public)
    # sk = PrivateKey(private)
    # print("type of private = ", type(private))
    # print("bytes = ", (bytes.fromhex(private).decode('utf-8')))
    # Convert private key into an Ethereum account
    account = Account.privateKeyToAccount(private)

    #return account , private
    return account_mnem3, account_mnem3_private

def get_balance(w1, address):
    """Using an Ethereum account address access the balance of Ether"""
    # Get balance of address in Wei
    wei_balance = w1.eth.get_balance(address)

    # Convert Wei value to ether
    ether = w1.fromWei(wei_balance, "ether")

    # Return the value in ether
    return ether


def send_transaction(w1, account, to, wage, privKey):
    """Send an authorized transaction to the Kovan blockchain."""
    # Set gas price strategy
    w1.eth.setGasPriceStrategy(medium_gas_price_strategy)

    # Convert eth amount to Wei
    value = w1.toWei(wage, "ether")

    # Calculate gas estimate
    gasEstimate = w1.eth.estimateGas({"to": to, "from": account.address, "value": value})
    n1 = w1.eth.get_transaction_count(account.address)
    print("n1 = ", n1)
    # Construct a raw transaction
    raw_tx = {
        "to": to,
        "from": account.address,
        "value": value,
        "gas": gasEstimate,
        "gasPrice": w1.toWei('150','gwei'),
        "chainId": 42,  # Kovan
        # "nonce": w1.eth.getTransactionCount(account.address)
        "nonce": n1
    }

    # Sign the raw transaction with ethereum account
    # print ("from inside send txn PrivKey in hex = " , privKey.hex())
    #signed_tx = account.signTransaction(raw_tx)
    print (" Raw txn = ", raw_tx)
    try:
        signed_tx = w1.eth.account.sign_transaction(raw_tx, private_key=privKey)
    except Exception as error_sign_txn:
        print(" error signing = ", error_sign_txn)
    # print(" Signed txn = " , signed_tx)
    #signed_tx = account.sign_transaction(raw_tx)
    block = w1.eth.get_block('latest')

    # print ("Latest Block = ", block['number'])
    # print ("Gas estimate = ", gasEstimate)
#     sendTxn = w1.eth.send_transaction({
#     'to': to,
#     'from': account.address,
#     'value': value,
#     'gas': gasEstimate,
#     'maxFeePerGas': w1.toWei(250, 'gwei'),
#     'maxPriorityFeePerGas': w1.toWei(2, 'gwei'),
# })


    print (" to address = " , to)
    print (" from address = " , account.address)
    print (" value = ", value)
    # print (" nonce = ", w1.eth.getTransactionCount(account.address))
    #print (" nonce = ", w1.eth.get_transaction_count(account.address))



    #print (" Signed Txn = ", signed_tx)
    # Send the signed transactions
    # sendTxn = w1.eth.sendRawTransaction(signed_tx.rawTransaction)
    try:
        sendTxn = w1.eth.send_raw_transaction(signed_tx.rawTransaction)
    except Exception as error_sending_txn:
        print (" exception sendTxn ", error_sending_txn)
        error_send = 1
    print (" Send Txn = ", sendTxn.hex())
    # return w1.eth.sendRawTransaction(signed_tx.rawTransaction)

    # print(w1.eth.get_transaction(sendTxn))
    # print( w1.eth.get_transaction_receipt(sendTxn) )
    # https://ethereum.stackexchange.com/questions/101513/send-eth-transaction-from-one-address-to-another-with-web3py
    try:
        receipt1 = w1.eth.wait_for_transaction_receipt(sendTxn)
    except Exception as error_receipt:
        print (" Exception receipt = ". error_receipt)

    return sendTxn
