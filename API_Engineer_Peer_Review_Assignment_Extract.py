import requests
import pandas as pd
import json

url = "http://api.exchangeratesapi.io/v1/latest?base=EUR&access_key=8fb6da2eb33417470f5dce3491cb371a"
req = requests.get(url).text
currency=json.loads(req)
currList=list(currency['rates'].items())
df=pd.DataFrame(currList,columns=["Currency","Rates"])
df.set_index("Currency",inplace=True)
df.index.name=None
print(df.head())
df.to_csv("exchange_rates_1.csv")
