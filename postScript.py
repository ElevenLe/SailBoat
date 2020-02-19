import json
import requests

def postData(data):
    api_url = 'http://howfull.us-west-2.elasticbeanstalk.com/postdata'
    create_row_data = {'id': str(data) }
    print(create_row_data)
    r = requests.post(url=api_url, json=create_row_data)
    print(r.status_code, r.reason, r.text)
