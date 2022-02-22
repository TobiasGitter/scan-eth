import pandas as pd

from EtherScanAPI import EtherscanAPI


def get_transactions_for_all_addresses(api, data):
    addresses = (ad for ad in data["address"])
    tx_amounts = (int(amount) for amount in data["txn_count"])
    tx_logs = {}
    counter = 1
    while counter <= 1:
        try:
            address = next(addresses)
            tx_amount = next(tx_amounts)
        except StopIteration:
            break

        if tx_amount > 2000:
            continue

        print(f"Looking at {address} with {tx_amount} transactions:")
        transactions = api.get_transactions(address, tx_amount)
        outgoing_tx = {}
        incoming_tx = {}

        for tx in transactions:
            if tx["to"] != address:
                if tx["to"] in outgoing_tx.keys():
                    outgoing_tx[tx["to"]]["tx_count"] += 1
                    outgoing_tx[tx["to"]]["transferred_value"] += tx["value"]
                    outgoing_tx[tx["to"]]["gas_used"] += tx["gas"] * tx["gasPrice"]
                else:
                    outgoing_tx[tx["to"]] = {
                        "tx_count": 1,
                        "transferred_value": tx["value"],
                        "gas_used": tx["gas"] * tx["gasPrice"]
                    }
            else:
                if tx["from"] in incoming_tx.keys():
                    incoming_tx[tx["from"]]["tx_count"] += 1
                    incoming_tx[tx["from"]]["transferred_value"] += tx["value"]
                    incoming_tx[tx["from"]]["gas_used"] += tx["gas"] * tx["gasPrice"]
                else:
                    incoming_tx[tx["from"]] = {
                        "tx_count": 1,
                        "transferred_value": tx["value"],
                        "gas_used": tx["gas"] * tx["gasPrice"]
                    }
        tx_logs[address] = {
            "incoming": incoming_tx,
            "outgoing": outgoing_tx
        }
        counter += 1
    return tx_logs
