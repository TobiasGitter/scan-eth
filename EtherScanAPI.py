import requests
import json
import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()


class EtherscanAPI:
    def __init__(self):
        self.API_KEY = os.getenv('API_KEY')

    def create_json(self, response):
        return json.loads(response.text)

    def get_balance(self, address):
        r = requests.get("https://api.etherscan.io/api?module=account&action=balance&"
                         "address=" + address +
                         "&tag=latest&"
                         "apikey=" + self.API_KEY)
        rjson = self.create_json(r)
        return Web3.fromWei(int(rjson["result"]), "ether")

    def get_multi_balance(self, *addresses):
        r = requests.get("https://api.etherscan.io/api?module=account&action=balancemulti&"
                         "address=" + ",".join(str(x) for x in addresses) +
                         "&tag=latest"
                         "&apikey=" + self.API_KEY)
        rjson = self.create_json(r)
        balances = {address: Web3.fromWei(int(balance["balance"]), "ether") for address, balance in
                    zip(addresses, rjson["result"])}
        return balances

    def get_transactions(self, address, tx_amount):
        r = requests.get(f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&"
                         f"endblock=99999999&page=1&offset={tx_amount}&sort=asc&apikey={self.API_KEY}")
        rjson = self.create_json(r)
        transactions = rjson["result"]
        for tx in transactions:
            tx["value"] = Web3.fromWei(int(tx["value"]), "ether")
            tx["gas"] = Web3.fromWei(int(tx["gas"]), "ether")
            tx["gasPrice"] = Web3.fromWei(int(tx["gasPrice"]), "ether")
        return transactions
