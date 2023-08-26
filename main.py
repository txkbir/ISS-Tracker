import os
import requests
from datetime import datetime, timezone
import smtplib
import time

MY_LAT = 34.119160
MY_LONG = -117.528130
PASSWORD = os.environ['PASSWORD']
EMAIL = 'takbirr04@gmail.com'

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

hour_now = datetime.now(timezone.utc).hour


while True:
    time.sleep(60)
    if (abs(iss_latitude - MY_LAT) <= 5 and abs(iss_longitude - MY_LONG) <= 5
            and (hour_now >= sunset or hour_now <= sunrise)):
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(to_addrs=EMAIL, from_addr=EMAIL, msg='Subject:Look up!\n\nISS overhead you!')
