# Machine Learning Academic Paper Topic Modelling

An exercise in **deploying** a machine learning model using a [Flask](https://flask.palletsprojects.com/) web server and a [Docker](https://www.docker.com) container.  
Topic modelling for ML academic papers using [Latent Dirichlet Allocation](https://scikit-learn.org/stable/modules/decomposition.html#latentdirichletallocation).
You can find an overview of the modelling approach itself below the following repository configuration info.

---

## Environment Setup & Development Workflow

This repository is **intended to be used in on a Unix system** (e.g. Ubuntu).
It includes a [Makefile](https://en.wikipedia.org/wiki/Makefile) with various targets (outlined below) that can be invoked from a terminal at the root of the repo.
Upon first cloning this repository, **you should change the APP_NAME variable within the Makefile** to some other project name of your choice.
You can then setup a new Conda virtual environment (with all required dependancies) by running the following command in terminal from the root of the repo:

```bash
make init
```

If you install any additional dependancies during the course of development work, you can re-export your Conda environment at any time using:

```bash
make environment.yaml
```

Tests in this project are implemented using [pytest](https://docs.pytest.org/en/stable/), and can be invoked via:

```bash
make tests
```

The Docker container that encapsulates the app can be built using:

```bash
make container
```

And then you can spin up the container locally (running the web app on localhost) using:

```bash
make local-serve
```

## Heroku Free Tier Cloud Deployment

Several Makefile targets are included for the purposes of deploying to the free tier of cloud hosting service [Heroku](https://www.heroku.com).  The general flow is as follows:

- Login to Heroku (requiring a Heroku account, naturally) via the Heroku CLI with `heroku-login` (this will open a login prompt in your browser)
- Create a new app in Heroku with `heroku-create` (the name will mirror the APP_NAME variable in the Makefile)
- Login to Heroku's container registry service with `heroku-container-login`
- Build and push the container to Heroku with `heroku-container-push`
- Release (deploy) the latest container image as a Heroku web app with `heroku-container-release`
- (Assuming you already have a Heroku app created, you can login, push and release the container all in the one `heroku-container-release` command)

---

## Modelling Approach

### Training Notes

The training dataset for this model is the [All NeurIPS (NIPS) Papers dataset](https://www.kaggle.com/rowhitswami/nips-papers-1987-2019-updated) as available on Kaggle.
Given the size, the dataset itself is not included in this repository, but if you would like to play with the model yourself, the training script expects the papers.csv file in a `data/` directory at the root of the repo.
The training process also expects a CSV list of Machine Learning specific stopwords (in the same `data/` directory), as well as a series of ML topic specific keyword list CSVs (for initialising the Bayesian priors of the model) within `data/topic_priors/`.

Training code is contained in train.py - this file is **written with `# %%` decorators that allow [Visual Studio Code](https://code.visualstudio.com/) to recognise distinct code cells and run them in an interactive Python session just like a Jupyter notebook**.
If you would like to play around with the model training, I highly recommend using Visual Studio Code to get the benefit of both a full featured IDE **as well as** the convenience of interactive Python code cells.

### Training Walkthrough

Library imports - self-explanatory:

```python
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from PTWGuidedLatentDirichletAllocation import PTWGuidedLatentDirichletAllocation # Customised sub-class of sklearn LDA
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import matplotlib.pyplot as plt
import numpy as np
import os
import math
import joblib
```

Ingest ML papers training data, custom ML specific stop words, and initial topic prior keyword lists:

```python
data_fname = '../../data/papers.csv'
data = pd.read_csv(data_fname)
data.dropna(subset=['full_text'], inplace=True)

stopwords_fname = '../../data/ml_stopwords.csv'
add_stop_words = pd.read_csv(stopwords_fname)
new_stop_word_list = ENGLISH_STOP_WORDS.union(add_stop_words.Stopword.values)

# Load all custom keyword lists for ML topics to use as topic priors in LDA
topic_priors_dir = os.fsencode('../../data/topic_priors/')
topic_priors_df_list = []
base_weight = 100
for f in os.listdir(topic_priors_dir):
    fname = '../../data/topic_priors/' + os.fsdecode(f)
    topic_name = os.fsdecode(f).split('.')[0]
    topic_words = pd.read_csv(open(fname))
    topic_words[topic_name] = base_weight
    topic_words.set_index('Word', inplace=True)
    topic_priors_df_list.append(topic_words)

n_topics = len(topic_priors_df_list)

topic_df = pd.concat(topic_priors_df_list, axis=1)
topic_df.index.name = 'Word'
topic_df.fillna(0., inplace=True)
```

Bag of words feature extraction of ML papers using Scikit-Learn's `CountVectorizer`:

```python
count_vectorizer = CountVectorizer(max_df=0.80, min_df=2, stop_words=new_stop_word_list)
tf_features = count_vectorizer.fit_transform(data.full_text)
```

Build topic prior keyword lists into specific format required for [custom LDA subclass](https://stackoverflow.com/questions/45170093/latent-dirichlet-allocation-with-prior-topic-words) (based on each word's positional index in the fitted `count_vectorizer`):

```python
def get_word_index(row, count_vectorizer):
    try:
        return list(count_vectorizer.get_feature_names()).index(row.Word)
    except:
        return np.nan

topic_df = topic_df.loc[[word for word in topic_df.index if word in count_vectorizer.get_feature_names()]]
topic_word_indices = topic_df.reset_index().apply(get_word_index, **{'count_vectorizer' : count_vectorizer}, axis=1)
topic_affinities_list = [list(row) for _, row in topic_df.iterrows()]
topic_priors = [(word_idx, affinities) for (word_idx, affinities) in zip(topic_word_indices, topic_affinities_list)]
```

Fit the LDA model (customised subclass of [Scikit-Learn's LDA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.LatentDirichletAllocation.html)):

```python
lda = PTWGuidedLatentDirichletAllocation(n_components=n_topics, n_jobs=-1, ptws=topic_priors)
lda.fit(tf_features)
preds = pd.DataFrame(lda.transform(tf_features))
```

Some additional utility code for inspecting the top words within each topic:

```python
def plot_top_words(model, feature_names, n_top_words, title, topic_names):
    fig, axes = plt.subplots(math.ceil(n_topics / 5.0), 5, figsize=(30, 15), sharex=True)
    axes = axes.flatten()
    for topic_idx, topic in enumerate(model.components_):
        top_features_ind = topic.argsort()[:-n_top_words - 1:-1]
        top_features = [feature_names[i] for i in top_features_ind]
        weights = topic[top_features_ind]

        ax = axes[topic_idx]
        ax.barh(top_features, weights, height=0.7)
        ax.set_title(f'Topic = {topic_names[topic_idx]}',
                     fontdict={'fontsize': 25})
        ax.invert_yaxis()
        ax.tick_params(axis='both', which='major', labelsize=20)
        for i in 'top right left'.split():
            ax.spines[i].set_visible(False)
        fig.suptitle(title, fontsize=40)

    plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)
    plt.show()

topic_names = topic_df.columns
topic_names = [name.title().replace("_", " ") for name in topic_names]
plot_top_words(lda, count_vectorizer.get_feature_names(), 20, 'Topics in LDA Model', topic_names)
```

And finally, serialise the modelling artifacts (fitted model itself, along with the count vectorizer and the established topic names) to use during inference in the actual web app deployment:

```python
artifact_path = 'model/'
joblib.dump(lda, artifact_path + 'model.joblib')
joblib.dump(count_vectorizer, artifact_path + 'count_vectorizer.joblib')
joblib.dump(topic_names, artifact_path + 'topic_names.joblib')
```
