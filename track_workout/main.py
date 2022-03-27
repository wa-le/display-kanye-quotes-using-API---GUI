import requests
from datetime import datetime
import os

GENDER = "male"
WEIGHT_KG = "88"
HEIGHT_CM = "160"
AGE = 25

# Nutritionix API
APP_ID = os.environ.get('NUTRI_ID')
API_KEY = os.environ.get('NUTRI_API_KEY')

exercise_url = "https://trackapi.nutritionix.com/v2/natural/exercise"
headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    # "x-remote-user-id": 0
}

request_param = {
    "query": input("what did you do? "),
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(url=exercise_url, json=request_param, headers=headers)
response.raise_for_status()
print(response.json())
the_exercises = response.json()['exercises']

# sheety
sheet_endpoint = os.environ.get('SHEETY_ENDPOINT')
sheet_bearer = os.environ.get('SHEETY_BEARER_AUTH')
for exercise in the_exercises:
    today = datetime.now()
    bearer_headers = {
        "Authorization": f"Bearer {sheet_bearer}"
    }
    sheet_param = {
        "workout": {
            "date": today.strftime("%d/%m/%Y"),
            "time": today.strftime("%X"),
            "exercise": exercise['name'].title(),
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories']
        }
    }

    response2 = requests.post(url=sheet_endpoint, json=sheet_param, headers=bearer_headers)
    response2.raise_for_status()
    # print(response2.text)
