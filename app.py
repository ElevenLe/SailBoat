from flask import Flask,render_template,jsonify,request,make_response,url_for,redirect
import numpy.random
application = Flask(__name__,template_folder='template',static_folder='static')
from json import dumps
from requests import post
@application.route('/postdata', methods=['GET','POST'])
def create_row_in_gs():
    if request.method == 'GET':
        return "error"
    if request.method == 'POST':
        reqId = request.json['id']
        f= open("data.txt","w")
        f.write(reqId)
	
        return reqId
@application.route('/')
def hello_world():
    populations = numpy.random.uniform(0,10,6)
    colors = ["green"]*6
    for i in range(len(populations)):
        if 0<=populations[i]<=5:
            colors[i] = "green"
        elif 0.5<populations[i]<=8:
            colors[i] = "yellow"
        else:
            colors[i] = "red"
    f= open("data.txt","r")
    if f.mode == 'r':
        content =f.read().split(',')
        content = [int(item) for item in content]
    print(colors)
    return render_template("index.html",value = colors, data=populations)

if __name__ == '__main__':
    application.run()
