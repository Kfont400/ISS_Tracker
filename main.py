import requests
from datetime import datetime
import smtplib
from time import time, sleep


def is_close(iss_position,MY_LAT,MY_LONG):
    if (iss_position[0]-5 <= MY_LAT <= iss_position[0]+5 and iss_position[1]-5 <= MY_LONG <= iss_position[1]+5):
        return True
    return False


def iss_tracker():
    MY_LAT = 29.628839
    MY_LONG = -95.400978

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    iss_position = (iss_latitude,iss_longitude)

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

    time_now = datetime.now()
    time_now_hour = time_now.hour

    if is_close(iss_position,MY_LAT,MY_LONG) and sunset <= time_now_hour <= sunrise:
        my_email = "kai2flie@gmail.com"
        password = "INSERTPASSWORDHERE"
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email, 
                to_addrs='kfont400@gmail.com', 
                msg=f"Subject:LOOK UP!!\n\nThe ISS is right above you at: {iss_position}"
            )

while True:
    time.sleep(60)
    iss_tracker()




