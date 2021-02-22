from flask import Flask, render_template, request
import json
from inference import predict_topics

#from inference import ...

app = Flask(__name__)

@app.route('/ping', methods=['GET', 'POST'])
def ping():
    return json.dumps('STATUS 200 - OK')

@app.route('/topics', methods=['GET', 'POST'])
def topics():
    if request.method == 'POST':
        topic_preds = predict_topics(request.form['text']) 
        max_topic = topic_preds.idxmax(axis=1)[0]
        response = "The most likely topic is {}".format(max_topic)
        return response
    return render_template('topics.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)