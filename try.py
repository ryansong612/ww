import requests, urllib, json

api = "https://apis.tianapi.com/hotword/index"
params = {
    "key": "dd6ce62b329899bd5a40d8ffbb3e2ed1",
    "num": 5,
    "word": "一哥"
}
headers = {
    "Content-type": "application/x-www-form-urlencoded"
}

res = requests.get(api, params=params)
data = res.json()
print(data)