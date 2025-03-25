import requests
import os

class MemeDbApiAdaptor:
    def __init__(self, api_key, base_url="https://apis.tianapi.com/"):
        # self.api_key = api_key or os.getenv("TIANAPI_KEY")
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"Content-type": "application/x-www-form-urlencoded"}

    def get_hotwords(self, word, num=5):
        url = self.base_url + "hotword/index"
        params = {"key": self.api_key, 
                  "num": num,
                  "word": word}
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_badboywords(self):
        url = self.base_url + "zhanan/index"
        params = {"key": self.api_key}
        try:
            response = requests.post(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

if __name__ == "__main__":
    api_key = "dd6ce62b329899bd5a40d8ffbb3e2ed1"
    adaptor = MemeDbApiAdaptor(api_key)
    print(adaptor.get_hotwords("鸡你太美"))
    print(adaptor.get_badboywords())
