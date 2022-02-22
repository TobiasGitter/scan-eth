from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
import pandas as pd

DICT_TEMPLATE = {
    "entryId": None,
    "address": None,
    "name": None,
    "balance": None,
    "percentage_of_eth": None,
    "txn_count": None
}

URL = "https://etherscan.io/accounts/"
data = []
COUNTER = 1
NUMBER_OF_PAGES = 400


def do_it_all(counter):
    if counter > NUMBER_OF_PAGES:
        return False
    print("Looking at page", counter)
    url = URL + str(counter)
    soup = open_new_url(url)
    data.extend(fetch_data(soup))
    counter += 1
    time.sleep(0.5)
    do_it_all(counter)


def open_new_url(url) -> BeautifulSoup:
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    return BeautifulSoup(webpage, 'lxml')


def fetch_data(soup) -> list:
    time.sleep(1)
    rows = soup.find("table").find("tbody").find_all("tr")
    temp_data = []
    for row in rows:
        new_entry = {key: c.text for key, c in zip(DICT_TEMPLATE, row.find_all("td"))}
        temp_data.append(new_entry)
    return temp_data


do_it_all(COUNTER)
with open("top_wallets.txt", "w") as emma:
    for d in data:
        line = ""
        for key in DICT_TEMPLATE:
            line += d[key] + "@"
        line += "\n"
        emma.write(line)

col_names =["address", "name", "balance", "percentage_of_eth", "txn_count"]
table = pd.read_csv("top_wallets.txt", delimiter="@", header=None)
table = table.iloc[:, 1:6]
table.columns = col_names
table.to_csv("data.csv", index=False)
print(table.head(10))
