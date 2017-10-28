from kiteconnect import KiteConnect
import json
from datetime import datetime

startDate = datetime.strptime("2017-04-01", '%Y-%m-%d')
endDate = datetime.strptime("2017-04-02", '%Y-%m-%d')
print startDate,endDate,""

kite = KiteConnect(api_key="ptj1cmagfr8rqmxe")
print "Open url and paste request_token after login flow"
print kite.login_url()
request_token = raw_input("Paste request_token :- \n");
try:
    user = kite.request_access_token(request_token=request_token,
                                     secret="xixh8g2mb6hagnye8jre5of2e2c12zbm")
    kite.set_access_token(user["access_token"])
except Exception as e:
    print("Authentication failed", str(e))
    raise
token = None
for instrument in kite.instruments():
	token = instrument["instrument_token"]
print kite.historical(token,startDate,endDate,"day");