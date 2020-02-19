from flask import Flask,render_template,jsonify,request,make_response,url_for,redirect
import random
application = Flask(__name__,template_folder='template',static_folder='static')
colors = ["red","yellow","blue","purple"]
from json import dumps
from requests import post
@application.route('/postdata', methods=['GET','POST'])
def create_row_in_gs():
    if request.method == 'GET':
        return "error"
    if request.method == 'POST':
        reqId = request.json['id']
        f= open("data.txt","w+")
        f.write(reqId)
	
        return reqId
@application.route('/')
def hello_world():
    i = random.randint(0,3)
    color = colors[i]
    f= open("data.txt","r")
    if f.mode == 'r':
        contents =f.read()
    print(contents)
    return render_template("index.html",value = color, data=contents)

if __name__ == '__main__':
    application.run(host="127.0.0.1", port=80)
