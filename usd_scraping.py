import requests
import json

url = "https://api.travelex.net/salt/config/multi?key=Travelex&site=%2Fvirgin&options=abhikzl"
r = requests.get(url)
data = json.loads(r.text)
exchange_rates = data['rates']['rates']

for item in exchange_rates:
    print("{}, {}".format(item, exchange_rates[item]))