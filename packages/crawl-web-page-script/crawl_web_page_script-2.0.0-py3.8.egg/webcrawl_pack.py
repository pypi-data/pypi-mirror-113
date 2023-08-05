import requests
import sys
import json
import os

class Webcrawling():

    def __init__(self, username, password, endpoint='http://localhost:8000/'):
        self.username = username
        self.password = password
        self.endpoint = endpoint
        self.generate_access_token()

    def generate_access_token(self):
        params = {
            "username": self.username,
            "password": self.password
        }
        try:
            endpoint = os.path.join(self.endpoint,"api/token/")
            response = requests.post(endpoint, data=params)
            response = response.json()
            self.access_token = response['access']
            return self.access_token
        except Exception as E:
            print(f"An exception occurred {E}") 
        

    def create_webcrawl_url(self, url, interval):
        params = {
            "url": url,
            "schedule_interval": interval,
        }
        try:
            endpoint = os.path.join(self.endpoint,"submit_job/")
            response = requests.post(endpoint, data=json.dumps(params),
                                headers={'Content-Type':'application/json',
                                        'Authorization': 'Bearer {}'.format(self.access_token)})
            return response.json()
        except Exception as E:
            print(f"An exception occurred {E}") 
        
    def fetch_job(self):
        params = {
            "id": self.job_id,
        }
        try:
            endpoint = os.path.join(self.endpoint,"crawl_urls/")
            response = requests.get(endpoint, data=params, headers={'Content-Type':'application/json',
                                        'Authorization': 'Bearer {}'.format(self.access_token)})
            return response.json()
        except Exception as E:
            print(f"An exception occurred {E}") 
        
if __name__=='__main__':
    res = Webcrawling(username = "nami", password = "nami@123")
    url = sys.argv[1]
    interval = sys.argv[2]
    crawl_url_submit = res.create_webcrawl_url(url, interval)
    print(crawl_url_submit)



