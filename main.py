from EtherScanAPI import EtherscanAPI
from get_transaction_data import get_transactions_for_all_addresses
import pandas as pd


# set up Etherscan-API and data
api = EtherscanAPI()
data = pd.read_csv("data.csv", index_col=None)

tx_logs = get_transactions_for_all_addresses(api, data)
print(tx_logs["0xda9dfa130df4de4673b89022ee50ff26f6ea73cf"]["incoming"])
print(tx_logs["0xda9dfa130df4de4673b89022ee50ff26f6ea73cf"]["outgoing"])

value_in = 0
tx_in = 0
for key in tx_logs["0xda9dfa130df4de4673b89022ee50ff26f6ea73cf"]["incoming"].keys():
    value_in += tx_logs["0xda9dfa130df4de4673b89022ee50ff26f6ea73cf"]["incoming"][key]["transferred_value"]
    tx_in += tx_logs["0xda9dfa130df4de4673b89022ee50ff26f6ea73cf"]["incoming"][key]["tx_count"]

print(tx_in)
value_out = 0
for key in tx_logs["0xda9dfa130df4de4673b89022ee50ff26f6ea73cf"]["outgoing"].keys():
    value_out += tx_logs["0xda9dfa130df4de4673b89022ee50ff26f6ea73cf"]["outgoing"][key]["transferred_value"]

print(value_in - value_out)