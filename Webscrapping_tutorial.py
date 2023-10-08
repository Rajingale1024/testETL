from bs4 import BeautifulSoup
import html5lib
import requests
import pandas as pd
import json


url="https://web.archive.org/web/20200318083015/https://en.wikipedia.org/wiki/List_of_largest_banks"
r = requests.get(url)
table_data=[]
   
soup = BeautifulSoup(r.text, 'lxml')
        #print(soup)
banks_table=soup.find_all("table")
for row in banks_table[2].find_all('tr'):
    row_data = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
    table_data.append(row_data[1:])
data = pd.DataFrame(table_data,columns=["Name", "Market Cap (US$ Billion)"])
data.to_json("bank_market_cap.json")
