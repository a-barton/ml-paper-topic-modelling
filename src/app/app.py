from flask import Flask, render_template, request
import json
from inference import predict_topics
from plot import plot_topics

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('topics.html')

@app.route('/ping', methods=['GET', 'POST'])
def ping():
    return json.dumps('STATUS 200 - OK')

@app.route('/topics', methods=['GET', 'POST'])
def topics():
    if request.method == 'POST':
        topic_preds = predict_topics(request.form['text']) 
        chart_html = plot_topics(topic_preds)
        return render_template('topics.html', chart_html=chart_html)
    return render_template('topics.html')