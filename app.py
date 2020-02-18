from flask import Flask,render_template
import random
app = Flask(__name__,template_folder='template',static_folder='static')
colors = ["red","yellow","blue","purple"]

@app.route('/')
def hello_world():
    i = random.randint(0,3)
    color = colors[i]
    return render_template("index.html",value = color)

if __name__ == '__main__':
    app.run()