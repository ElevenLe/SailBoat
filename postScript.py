from cryptography.fernet import Fernet
import json
import requests
import time
def postData(data):
    key=("R4WBmuFIHoTaz9recdTsrMYETGhAYXuLXoOm-kVr2JE=".encode())
    cipher_suite = Fernet(key)
    timeInt=int(time.time())
    timeEncBytes = cipher_suite.encrypt(str(timeInt).encode())
    timeEncStr = timeEncBytes.decode("utf-8")
    api_url = 'http://127.0.0.1/postdata'
    create_row_data = {'data': str(data), 'time': timeEncStr }
    print(create_row_data)
    r = requests.post(url=api_url, json=create_row_data)
    print(r.status_code, r.reason, r.text)
