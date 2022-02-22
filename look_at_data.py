import pandas as pd

from EtherScanAPI import EtherscanAPI


def get_transactions_for_all_addresses(api, data):
    outgoing_tx_addresses = incoming_tx_addresses = {}
    addresses = (ad for ad in data["address"])
    tx_amounts = (int(amount) for amount in data["txn_count"])

    counter = 1
    while counter <= 1:
        try:
            address = next(addresses)
            tx_amount = next(tx_amounts)
        except StopIteration:
            break

        if tx_amount > 2000:
            continue
        else:
            print(f"Looking at {address} with {tx_amount} transactions:")
            transactions = api.get_transactions(address, tx_amount)
            for tx in transactions:
                if tx["to"] and tx["to"] != address:
                    if address not in outgoing_tx_addresses.keys():
                        outgoing_tx_addresses[address] = {}
                    if tx["to"] in outgoing_tx_addresses[address].keys():
                        outgoing_tx_addresses = add_to_entry(outgoing_tx_addresses, tx["to"], address, tx)
                    else:
                        outgoing_tx_addresses = new_entry(outgoing_tx_addresses, tx["to"], address, tx)
                elif tx["from"] and tx["from"] != address:
                    if address not in incoming_tx_addresses.keys():
                        incoming_tx_addresses[address] = {}
                    if tx["from"] in incoming_tx_addresses[address].keys():
                        incoming_tx_addresses = add_to_entry(incoming_tx_addresses, address, tx["from"], tx)
                    else:
                        incoming_tx_addresses = new_entry(incoming_tx_addresses, address, tx["from"], tx)
        counter += 1
    return incoming_tx_addresses, outgoing_tx_addresses


def new_entry(transaction_logs, key_address, interacting_address, tx):
    transaction_logs[key_address][interacting_address] = {
        "tx_count": 1,
        "value": tx["value"],
        "gas_usd": tx["gas"] * tx["gasPrice"]
    }
    return transaction_logs


def add_to_entry(transaction_logs, key_address, interacting_address, tx):
    transaction_logs[key_address][interacting_address]["tx_count"] += 1
    transaction_logs[key_address][interacting_address]["value"] += tx["value"]
    transaction_logs[key_address][interacting_address]["gas_usd"] += tx["gas"] * tx["gasPrice"]
    return transaction_logs
