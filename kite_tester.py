import logging
from kiteconnect import KiteConnect

logging.basicConfig(level=logging.DEBUG)

API_KEY = "6dlf37ff0429agtv"
API_SECRET = "h02vugjj3a32ydwerx6sp43hgkza8ksb"
kite = KiteConnect(api_key=API_KEY)
print kite.login_url()

request_token = "caerJf9QUquCVcTOPTaVP4Axp8AZtY9D"

data = kite.generate_session(request_token, api_secret=API_SECRET)
kite.set_access_token(data["access_token"])


print(data["user_id"], "has logged in")

# Get the list of positions.
print(kite.positions())

# Get instruments
a = kite.historical_data("3861249", "2018-02-01", "2018-02-05", "15 minute")
print(a)

