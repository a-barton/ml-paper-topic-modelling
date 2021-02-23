# %%

######################
## Import libraries ##
######################

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from PTWGuidedLatentDirichletAllocation import PTWGuidedLatentDirichletAllocation
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import matplotlib.pyplot as plt
import numpy as np
import os
import math
import joblib

# %%

###########################
## Ingest ML papers data ##
###########################

data_fname = '../../data/papers.csv'
data = pd.read_csv(data_fname)
data.dropna(subset=['full_text'], inplace=True)


# %%

####################################################################
## Ingest and incorporate custom data science specific stop words ##
####################################################################

stopwords_fname = '../../data/ml_stopwords.csv'
add_stop_words = pd.read_csv(stopwords_fname)
new_stop_word_list = ENGLISH_STOP_WORDS.union(add_stop_words.Stopword.values)


# %%

###############################################
## Ingest custom keyword lists for ML topics ##
###############################################

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


# %%

##############################
## Count Feature Extraction ##
##############################

count_vectorizer = CountVectorizer(max_df=0.80, min_df=2, stop_words=new_stop_word_list)
tf_features = count_vectorizer.fit_transform(data.full_text)


# %%

############################################################################################
## Build topic priors using positional indices of topic prior keywords within tf features ##
############################################################################################

def get_word_index(row, count_vectorizer):
    try:
        return list(count_vectorizer.get_feature_names()).index(row.Word)
    except:
        return np.nan

topic_df = topic_df.loc[[word for word in topic_df.index if word in count_vectorizer.get_feature_names()]]
topic_word_indices = topic_df.reset_index().apply(get_word_index, **{'count_vectorizer' : count_vectorizer}, axis=1)
topic_affinities_list = [list(row) for _, row in topic_df.iterrows()]
topic_priors = [(word_idx, affinities) for (word_idx, affinities) in zip(topic_word_indices, topic_affinities_list)]

# %%

#########
## LDA ##
#########

lda = PTWGuidedLatentDirichletAllocation(n_components=n_topics, n_jobs=-1, ptws=topic_priors)
lda.fit(tf_features)
preds = pd.DataFrame(lda.transform(tf_features))

# %%

####################
## Plot top words ##
####################

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

# %%

#######################################################
## Serialise model, count vectorizer and topic names ##
#######################################################

artifact_path = 'model/'
joblib.dump(lda, artifact_path + 'model.joblib')
joblib.dump(count_vectorizer, artifact_path + 'count_vectorizer.joblib')
joblib.dump(list(topic_names), artifact_path + 'topic_names.joblib')

