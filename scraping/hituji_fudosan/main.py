import csv
import time

import requests
from bs4 import BeautifulSoup

def base(filename):
    with open(filename + ".html") as myfile:
        soup = BeautifulSoup(myfile, "html.parser")

    elem = soup.select(
        ".comret-follow-component>div>a"
    )

    house_list = [house.attrs["href"] for house in elem]

    result = []

    for url in house_list:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        district = soup.select("#breadcrumb > li:nth-child(3) > a > span")[0].get_text()
        station = soup.select("#breadcrumb > li:nth-child(4) > a > span")[0].get_text()
        prices = soup.select(".roomPrice__value")
        rent = prices[0].get_text()
        fee = prices[1].get_text()
        result.append([url, district, station, rent, fee])
        print(f'finished {len(result)} / {len(house_list)}')
        time.sleep(3)

    f = open(filename + '.csv', 'w', newline='')
    writer = csv.writer(f)
    writer.writerows(result)
    f.close()

    print("Done")

"""
https://www.hituji.jp/comret/info/tokyo
https://www.hituji.jp/comret/info/kanagawa
https://www.hituji.jp/comret/info/saitama
https://www.hituji.jp/comret/info/chiba
"""
