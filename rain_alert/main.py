import requests
from twilio.rest import Client
import os

# for twilio
my_twilio_number = os.environ.get('MY_TWILIO_NUMBER')
receive_number = os.environ.get('MY_RECEIVE_NUMBER')
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

# for OpenWeather
api_key = os.environ.get('OPEN_WEATHER_API_KEY')
one_call_endpoint = "https://api.openweathermap.org/data/2.5/onecall"

brussels_lat = 50.8476
brussels_long = 4.3572
# kutaisi_lat = 42.266243
# kutaisi_long = 42.718002

check_for = {
    "lat": brussels_lat,
    "lon": brussels_long,
    "exclude": "current,minutely,daily",
    "appid": api_key
}

# OneCall API 48hrs forecast
response = requests.get(url=one_call_endpoint, params=check_for)
response.raise_for_status()

weather_data = response.json()
# print(weather_data)
weather_data_hourly = weather_data["hourly"]
weather_data_12_hrs = weather_data_hourly[:12]

# check if rain will fall
will_rain = False
for i in weather_data_12_hrs:
    # print(i)
    check_rain = i["weather"][0]["id"]
    # print(check_rain)
    if check_rain < 700:
        will_rain = True

# send sms notification if it will rain
if will_rain:
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body='Rain will fall in Brussels today. Remember to hold an umbrella ☂️',
        from_=my_twilio_number,
        to=receive_number
    )
else:
    print("no rain for the next 12 hours")
