from flask import Flask, render_template, request
import json

#from inference import ...

app = Flask(__name__)

@app.route('/ping', methods=['GET', 'POST'])
def ping():
    return json.dumps('STATUS 200 - OK')

@app.route('/topics', methods=['GET', 'POST'])
def topics():
    if request.method == 'POST':
        print(request.form['text'])
        return request.form['text']
    return render_template('topics.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)