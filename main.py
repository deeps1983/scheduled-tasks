import os
from pathlib import Path
import requests
from twilio.rest import Client
from dotenv import load_dotenv

# Load .env from the same directory as this script, regardless of where it's run from
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

api_key = os.getenv("OWM_API_KEY")
own_endpoint= "https://api.openweathermap.org/data/2.5/forecast"
account_sid = os.getenv("TW_ACCOUNT_SID")
auth_token = os.getenv("TW_AUTH_TOKEN")
twilio_from = os.getenv("TW_FROM_NUMBER")
twilio_to = os.getenv("TW_TO_NUMBER")

# Validate before using any credentials
if not api_key or not auth_token or not account_sid or not twilio_from or not twilio_to:
    raise ValueError("Missing required environment variables: OWM_API_KEY, TW_ACCOUNT_SID, TW_AUTH_TOKEN, TW_FROM_NUMBER, TW_TO_NUMBER")

client = Client(account_sid, auth_token)

weather_param = {
 "lat" : "-26.120136",
 "lon" : "27.901464",
 "appid" : api_key, 
 "units" : "metric",
 "cnt" : "8"
}
    
#calling OpenWeatherMap API
response = requests.get(own_endpoint, params=weather_param)
print(f"response code={response.status_code}")  
#print(response.json())  
weather_data = response.json()

will_rain = False
for hour_data in weather_data['list']:
#     print(weather_data['list'][0]['weather'][0]['id'])
        print(hour_data['weather'][0]['id'])
        hour_data_id = hour_data['weather'][0]['id']
        if int(hour_data_id) < 700:
            will_rain = True

if will_rain:
    print("bring an umbrella")
    message = client.messages.create(
        body="It will rain today. Remember to bring an umbrella ☂️",
        from_=twilio_from,
        to=twilio_to
    )
else:
    print("no rain today")
    message = client.messages.create(
        body="no rain today🌞....enjoy your day!",
        from_=twilio_from,
        to=twilio_to
    )
    print(message.status)






    






    
