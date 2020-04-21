from flask import Flask,render_template,jsonify,request,make_response,url_for,redirect
import numpy.random
application = Flask(__name__,template_folder='template',static_folder='static')
from json import dumps
from requests import post
import time
from cryptography.fernet import Fernet
#change this if more rooms added
numRooms=6

@application.route('/postdata', methods=['GET','POST'])
def create_row_in_gs():
    if request.method == 'GET':
        return "error"
    if request.method == 'POST':
        #RECOMMENDED generate a new key with key, use Fernet.generate_key() to get a random key
        #Note, key must match key in postscript.py
        key=("R4WBmuFIHoTaz9recdTsrMYETGhAYXuLXoOm-kVr2JE=".encode())
        cipher_suite = Fernet(key)
        print(request.json['data'])
        
        data = request.json['data']
        index = request.json['index']
        timeInt=int(time.time())
        decodedTime = cipher_suite.decrypt(request.json['time'].encode())
        decodedTime = decodedTime.decode("utf-8")
        if(abs(int(decodedTime)-timeInt) < 30):
            #if the message was received in the last 30 seconds, then
            #write the data
            fileData=""
            indexNum=0
            with open('data.txt','r') as openfileobject:
                for line in openfileobject:
                    if(indexNum==index):
                        fileData+=data
                        fileData+="\n"
                    else:
                        fileData+=line
                    indexNum+=1
            f=open("data.txt","w")
            f.write(fileData)
            f.close()
        
	
        return data
@application.route('/')
def hello_world():
    f = open("data.txt","r")
    populations = [0]*numRooms
    populations[0] = int(f.readline())
    for x in range(numRooms):
        populations[x] = populations[0]
        #change this line to populations[x] = int(f.readline())
        #and comment out the line above this for loop
        #if you want more than 1 room number displayed
	
    colors = ["green"]*6
    for i in range(len(populations)):
        if 0<=populations[i]<=5:
            colors[i] = "green"
        elif 0.5<populations[i]<=8:
            colors[i] = "yellow"
        else:
            colors[i] = "red"
    
    print(colors)
    return render_template("index.html",value = colors, data=populations)

if __name__ == '__main__':
    application.run(port=80)
