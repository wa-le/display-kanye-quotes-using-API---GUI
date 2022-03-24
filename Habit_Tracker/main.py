import requests
from datetime import datetime

USERNAME = "zhuvi"
TOKEN = "ts2vuby9no4tbryt7"
GRAPH_ID = "graph1"

pixela_endpoint = "https://pixe.la/v1/users"

# pixela user creation details
user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}

# create User/account
# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

# config graph
graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_config = {
    "id": "graph1",
    "name": "Running",
    "unit": "Km",
    "type": "float",
    "color": "sora"
}

# header config with TOKEN
headers = {
    "X-USER-TOKEN": TOKEN,
}

#
# response2 = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(response2.text)

# https://pixe.la/v1/users/zhuvi/graphs/graph1.html to access graph

post_pixel_endpoint = f"{graph_endpoint}/{GRAPH_ID}"

# format date to fit post_pixel_config "date"
# today = datetime(2022, 3, 22) -> for another date

today = datetime.now()

post_pixel_config = {
    "date": today.strftime("%Y%m%d"),
    "quantity": input("How many Km did you cycle today? ")
}

response3 = requests.post(url=post_pixel_endpoint, json=post_pixel_config, headers=headers)
print(response3.text)

# use PUT to update pixel
update_pixel_endpoint = f"{post_pixel_endpoint}/20220323"

update_pixel_config = {
    "quantity": "12.0"
}

# response4 = requests.put(url=update_pixel_endpoint, json=update_pixel_config, headers=headers)
# print(response4.text)

# use DELETE to delete pixel
delete_pixel_endpoint = f"{post_pixel_endpoint}/20220322"
# response5 = requests.delete(url=delete_pixel_endpoint, headers=headers)
# print(response5.text)