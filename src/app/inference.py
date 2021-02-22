import joblib
import pandas as pd

def predict_topics(text):
    lda, count_vectorizer, topic_names = load_model()
    features = count_vectorizer.transform([text])
    preds = pd.DataFrame(lda.transform(features), columns=topic_names)
    return preds

def load_model():
    lda = joblib.load('model/model.joblib')
    count_vectorizer = joblib.load('model/count_vectorizer.joblib')
    topic_names = joblib.load('model/topic_names.joblib')
    return lda, count_vectorizer, topic_names
