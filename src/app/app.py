from flask import Flask, render_template, request
import json

#from inference import ...

app = Flask(__name__)

@app.route('/ping', methods=['GET', 'POST'])
def ping():
    return json.dumps('STATUS 200 - OK')

@app.route('/topics', methods=['GET', 'POST'])
def topics():
    return json.dumps('TODO')