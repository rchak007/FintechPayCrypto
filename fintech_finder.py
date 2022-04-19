# Cryptocurrency Wallet
################################################################################

# This file contains the streamlit app

################################################################################
# Imports
import os
from dataclasses import dataclass
from typing import Any, List

import etherscan
import streamlit as st
from dotenv import load_dotenv
from web3 import Account, HTTPProvider, Web3
from web3.middleware import geth_poa_middleware
## from etherscan import Etherscan

load_dotenv()

# w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))  - Chuck
## Chucks
WEB3_INFURA_API_KEY =  os.getenv("WEB3_INFURA_API_KEY")
WEB3_INFURA_PROJECT_ID = os.getenv("WEB3_INFURA_PROJECT_ID")
# print("WEB3_INFURA_PROJECT_ID =", WEB3_INFURA_PROJECT_ID)
# print("WEB3_INFURA_API_KEY =", WEB3_INFURA_API_KEY)
ETHERSCAN_API = os.getenv("ETHERSCAN_API")
#eth = Etherscan(ETHERSCAN_API, net= "KOVAN")
# eth = etherscan.Client(
#     api_key=ETHERSCAN_API,
# #    net= "KOVAN",
#     cache_expire_after=5,
# )
#### Connect to infura kovan
# https_str = f'https://kovan.infura.io/v3/{WEB3_INFURA_PROJECT_ID}'
https_str = f'https://kovan.infura.io/v3/{WEB3_INFURA_PROJECT_ID}'
w1 = Web3(Web3.HTTPProvider(https_str))
w1.middleware_onion.inject(geth_poa_middleware, layer=0)
chain_id = 42
#account_contract_owner = Account.from_key(museum_private_key)
#from web3.auto.infura import w3

#print("w3 connected? ", w3.isConnected())
print("w1 connected? ", w1.isConnected())

# w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:8545'))   --

# Import Ethereum Transaction Functions into the Fintech Finder Application

# Import several functions from the `crypto_wallet.py`
# script into the file `fintech_finder.py`, which contains code for Fintech
# Finder’s customer interface, in order to add wallet operations to the
# application. ., you’ll provide your Ethereum wallet and account
# information to the application).



# Add mnemonic seed phrase  to the .env file.


# From `crypto_wallet.py import the functions generate_account, get_balance,
#  and send_transaction
from crypto_wallet import generate_account, get_balance, send_transaction

################################################################################
# Fintech Finder Candidate Information

# Database of Fintech Finder candidates including their name, digital address, rating and hourly cost per Ether.
# A single Ether is currently valued at $1,500
candidate_database = {
    #"Lane": ["Lane", "0x0a8A314bC0C5300E34f2e4eBF1A7EEC98c3a4D57", "4.3", .20, "Images/lane.jpeg"],
    #"Ash": ["Ash", "0x949D9280768F37a8C0d3C68D29Ad5d2b42756E9C", "5.0", .33, "Images/ash.jpeg"],
    #"Jo": ["Jo", "0x9FC6387cb7722b3B919688218368d217C30f255A", "4.7", .19, "Images/jo.jpeg"],
    #"Kendall": ["Kendall", "0xAB10A3D05394d476E4f2d6066fb525A6D7a6D8E8", "4.1", .16, "Images/kendall.jpeg"]
    "Lane": ["Lane", "0xAB4A0C2ed939f32DE20E7118E23fddaF9739aCe0", "4.3", .20, "Images/lane.jpeg"],  # account 2
    "Ash": ["Ash", "0xbBdBA51a140fcBA90a41e9A5ca290B98e7087104", "5.0", .33, "Images/ash.jpeg"],     # Account 3
    "Jo": ["Jo", "0xA6B5e696329691a1bdB0827221482733B76F0638", "4.7", .19, "Images/jo.jpeg"],        # Account 4
    "Kendall": ["Kendall", "0x00282868a26d11ca1eE85B5B6ff9f667E58Eef19", "4.1", .16, "Images/kendall.jpeg"]   # Account 5
}

# A list of the FinTech Finder candidates first names
people = ["Lane", "Ash", "Jo", "Kendall"]


def get_people():
    """Display the database of Fintech Finders candidate information."""
    db_list = list(candidate_database.values())

    for number in range(len(people)):
        st.image(db_list[number][4], width=200)
        st.write("Name: ", db_list[number][0])
        st.write("Ethereum Account Address: ", db_list[number][1])
        st.write("FinTech Finder Rating: ", db_list[number][2])
        st.write("Hourly Rate per Ether: ", db_list[number][3], "eth")
        st.text(" \n")

################################################################################
# Streamlit Code

# Streamlit application headings
st.markdown("# Fintech Finder!")
st.markdown("## Hire A Fintech Professional!")
st.text(" \n")

################################################################################
# Streamlit Sidebar Code - Start

st.sidebar.markdown("## Client Account Address and Ethernet Balance in Ether")

##########################################

# Create a variable named `account`. Set this variable equal to a call on the
# `generate_account` function. This function will create the Fintech Finder
# customer’s (in this case, your) HD wallet and Ethereum account.


#  Call the `generate_account` function and save it as the variable `account`
account, privKey = generate_account()
# print ("from fintech PrivKey in hex = " , privKey.hex())
# print(Web3.toBytes(privKey))

##########################################

# Write the client's Ethereum account address to the sidebar
st.sidebar.write(account.address)

##########################################

# Define a new `st.sidebar.write` function that will display the balance of the
# customer’s account. Inside this function, call the `get_balance` function and
#  pass it your Ethereum `account.address`.


# Call `get_balance` function and pass it your account address
# Write the returned ether balance to the sidebar
st.sidebar.write(get_balance(w1, account.address))

##########################################

# Create a select box to choose a FinTech Hire candidate
person = st.sidebar.selectbox('Select a Person', people)

# Create a input field to record the number of hours the candidate worked
hours = st.sidebar.number_input("Number of Hours")

st.sidebar.markdown("## Candidate Name, Hourly Rate, and Ethereum Address")

# Identify the FinTech Hire candidate
candidate = candidate_database[person][0]

# Write the Fintech Finder candidate's name to the sidebar
st.sidebar.write(candidate)

# Identify the FinTech Finder candidate's hourly rate
hourly_rate = candidate_database[person][3]

# Write the inTech Finder candidate's hourly rate to the sidebar
st.sidebar.write(hourly_rate)

# Identify the FinTech Finder candidate's Ethereum Address
candidate_address = candidate_database[person][1]

# Write the FinTech Finder candidate's Ethereum Address to the sidebar
st.sidebar.write(candidate_address)

# Write the Fintech Finder candidate's name to the sidebar

st.sidebar.markdown("## Total Wage in Ether")

################################################################################
# Sign and Execute a Payment Transaction




# Calculate total `wage` for the candidate by multiplying the candidate’s hourly
# rate from the candidate database (`candidate_database[person][3]`) by the
# value of the `hours` variable
wage = candidate_database[person][3] * hours


# Write the `wage` calculation to the Streamlit sidebar
st.sidebar.write(wage)

##########################################

# * Call the `send_transaction` function and pass it three parameters:
    # - Ethereum `account` information.

    #- The `candidate_address` (which will be created and identified in the
    # sidebar when a customer selects a candidate). This will populate the `to`
    # data attribute in the raw transaction.
    # - The `wage` value. This will be passed to the `toWei` function to
    # determine the wei value of the payment in the raw transaction.

# * Save the transaction hash that the `send_transaction` function returns as a
# variable named `transaction_hash`, and have it display on the application’s
# web interface.


if st.sidebar.button("Send Transaction"):


    # Call the `send_transaction` function and pass it 3 parameters:
    # Your `account`, the `candidate_address`, and the `wage` as parameters
    # Save the returned transaction hash as a variable named `transaction_hash`
    # print ("from send txn call PrivKey in hex = " , privKey.hex())
    transaction_hash = send_transaction(w1, account, candidate_address, wage, privKey)

    # Markdown for the transaction hash
    st.sidebar.markdown("#### Validated Transaction Hash")

    # Write the returned transaction hash to the screen
    st.sidebar.write(transaction_hash.hex())

    # Celebrate your successful payment
    st.balloons()

# The function that starts the Streamlit application
# Writes FinTech Finder candidates to the Streamlit page
get_people()

################################################################################
# Inspect the Transaction

# Send a test transaction by using the application’s web interface, and then
# look up the resulting transaction hash in Kovan etherscan explorer.

# Complete the following steps:


# Activate your Conda `kovan` environment if it is not already active.

# To launch the Streamlit application,
# type `streamlit run fintech_finder.py`.

# On the resulting webpage, select a candidate that you would like to hire
# from the appropriate drop-down menu. Then, enter the number of hours that you
# would like to hire them for.

# Click the Send Transaction button to sign and send the transaction with
# your Ethereum account information. If the transaction is successfully
# communicated to Kovan, validated, and added to a block,
# a resulting transaction hash code will be written to the Streamlit
# application sidebar.

