from flask import Flask, render_template, request
import json
from inference import predict_topics
from plot import plot_topics

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

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

@app.route('/example', methods=['GET', 'POST'])
def example():
    if request.method == 'POST':
        example_text = "Recent methods for learning vector space representations of words have succeeded in capturing fine-grained semantic and syntactic regularities using vector arithmetic, but the origin of these regularities has remained opaque. We analyze and make explicit the model properties needed for such regularities to emerge in word vectors. The result is a new global logbilinear regression model that combines the advantages of the two major model families in the literature: global matrix factorization and local context window methods. Our model efficiently leverages statistical information by training only on the nonzero elements in a word-word cooccurrence matrix, rather than on the entire sparse matrix or on individual context windows in a large corpus. The model produces a vector space with meaningful substructure, as evidenced by its performance of 75% on a recent word analogy task. It also outperforms related models on similarity tasks and named entity recognition.Recent methods for learning vector space representations of words have succeeded in capturing fine-grained semantic and syntactic regularities using vector arithmetic, but the origin of these regularities has remained opaque. We analyze and make explicit the model properties needed for such regularities to emerge in word vectors. The result is a new global logbilinear regression model that combines the advantages of the two major model families in the literature: global matrix factorization and local context window methods. Our model efficiently leverages statistical information by training only on the nonzero elements in a word-word cooccurrence matrix, rather than on the entire sparse matrix or on individual context windows in a large corpus. The model produces a vector space with meaningful substructure, as evidenced by its performance of 75% on a recent word analogy task. It also outperforms related models on similarity tasks and named entity recognition."
        topic_preds = predict_topics(example_text) 
        chart_html = plot_topics(topic_preds)
        return render_template('topics.html', chart_html=chart_html)
    return render_template('topics.html')
