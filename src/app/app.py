from flask import Flask, render_template, request
import json
from inference import predict_topics
from plot import plot_topics

#from inference import ...

app = Flask(__name__)

@app.route('/ping', methods=['GET', 'POST'])
def ping():
    return json.dumps('STATUS 200 - OK')

@app.route('/topics', methods=['GET', 'POST'])
def topics():
    if request.method == 'POST':
        topic_preds = predict_topics(request.form['text']) 
        response_html_fname = 'response.html'
        plot_topics(topic_preds, response_html_fname)
        return render_template(response_html_fname)
    return render_template('topics.html')

"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
"""