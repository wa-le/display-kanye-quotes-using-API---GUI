# Script Goal #
# If the ISS is close to my current position
# And it is currently dark
# Then email me to look up.
# Run the code every 60 seconds.

import time
import requests
from datetime import datetime
import smtplib

MY_LAT = 51.0517339
MY_LONG = 4.1032755

# gets ISS location
response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()

# gets the longitude and latitude of the ISS
data = response.json()
iss_longitude = float(data['iss_position']['longitude'])
iss_latitude = float(data['iss_position']['latitude'])


# --Your position is within +5 or -5 degrees of the ISS position.--

# sunrise/sunset get api
# put parameters to add to an api get in a dictionary, especially the 'Required' ones
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response_2 = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response_2.raise_for_status()
data = response_2.json()
# get sunrise and sunset
sunrise = data["results"]["sunrise"]
sunset = data["results"]["sunset"]
sunrise_hr = int(sunrise.split("T")[1].split(":")[0])
sunset_hr = int(sunset.split("T")[1].split(":")[0])

time_now = datetime.now()
hour_now = time_now.hour


# check proximity of ISS to home
def iss_to_home(iss_long, iss_lat):
    if int(iss_long) in range(int(MY_LONG-5), int(MY_LONG+5)) and int(iss_lat) in range(int(MY_LAT-5), int(MY_LAT+5)):
        return True
    else:
        return False


confirm_proximity = iss_to_home(iss_longitude, iss_latitude)


# check if its sunset
def its_dark(curr_hour, s_rise, s_set):
    # or do "if 'time_now > sunset and < sunrise"
    if curr_hour in range(0, s_rise) or curr_hour in range(s_set, 24):
        return True
    else:
        return False


confirm_darkness = its_dark(hour_now, sunrise_hr, sunset_hr)

my_email = "mainstopstore@gmail.com"
my_email_pass = "upperECHELON03"
recipient_email = "rajahquan@gmail.com"
the_msg = f"Subject:ISS Hover Alert\n\nLook Up and Behold the ISS"

# when the ISS and my home's coordinates are close and its dark, send an email for me to look up
# the time module is used to make the code run for 60secs - every 60sec(using the while loop)


while True:
    time.sleep(2)
    if confirm_proximity and confirm_darkness:
        # connect to "your" email server
        with smtplib.SMTP("smtp.gmail.com", port=587) as new_connect:
            # secure the connection
            new_connect.starttls()

            new_connect.login(user=my_email, password=my_email_pass)
            new_connect.sendmail(from_addr=my_email, to_addrs=recipient_email, msg=the_msg)


