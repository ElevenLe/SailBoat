from cryptography.fernet import Fernet
import json
import requests
import time
def postData(data, index):
    #RECOMMENDED generate a new key with key, use Fernet.generate_key() to get a random key
    #Note, key must match key in app.py
    key=("R4WBmuFIHoTaz9recdTsrMYETGhAYXuLXoOm-kVr2JE=".encode())
    cipher_suite = Fernet(key)
    timeInt=int(time.time())
    timeEncBytes = cipher_suite.encrypt(str(timeInt).encode())
    timeEncStr = timeEncBytes.decode("utf-8")
    #Change this to whatever ip you want to send te data to
    api_url = 'http://localhost/postdata'
    create_row_data = {'data': str(data), 'time': timeEncStr, 'index': index }
    r = requests.post(url=api_url, json=create_row_data)
#usage: postData(data,index (must be in range 0-5))

postData(3,0)
