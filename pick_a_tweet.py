import numpy as np
import gensim
from sklearn.metrics.pairwise import cosine_similarity
import random
from sklearn.preprocessing import normalize
import pandas as pd

from sklearn.externals import joblib
from sklearn.svm import LinearSVC


# load all the models 

model = gensim.models.KeyedVectors.load('models/tweet_w2v')  # word2vec embeddings
svm_polornot = joblib.load('models/svm_polORnot.pkl')  # SVM classifier of political vs not political

con_v = np.load('models/conservative_vecs.npy')  # embeddings of conservative ads 
lib_v = np.load('models/liberal_vecs.npy')  # embeddings of liberal ads 

df_lib = pd.read_csv('models/liberal_ads.csv' ,error_bad_lines=False)  # liberal ads 
df_con = pd.read_csv('models/conservative_ads.csv' ,error_bad_lines=False)  # conservative ads 


#compute vector representation of tweet by summing word vectors
def tweet2vec(tweet):
    vec = np.sum([model.wv[word] for word in tweet.split() if word in model.wv.vocab],axis=0)
    if vec.shape == ():
        vec = np.zeros(100)
    return vec

#function to select only tweets about the input topic. It computes cosine similarity with two given queries
#takes the maximum and returns: a list of distance > threshold, the index of one of the two closest tweets to the topic
#and the queries vectors
def relevant_tweets(tw_vec, topic, threshold):
    if topic == 'Healthcare':
        query_1 = np.sum([model.wv.get_vector(word) for word in 'healthcare'.split() if word in model.wv.vocab],axis=0)
        query_2 = np.sum([model.wv.get_vector(word) for word in 'obamacare affordable care act'.split() if word in model.wv.vocab],axis=0)
    elif topic == 'Climate change':
        query_1 = np.sum([model.wv.get_vector(word) for word in 'climate'.split() if word in model.wv.vocab],axis=0)
        query_2 = np.sum([model.wv.get_vector(word) for word in 'warming'.split() if word in model.wv.vocab],axis=0)
    elif topic == 'Immigration':
        query_1 = np.sum([model.wv.get_vector(word) for word in 'immigration'.split() if word in model.wv.vocab],axis=0)
        query_2 = np.sum([model.wv.get_vector(word) for word in 'immigrant'.split() if word in model.wv.vocab],axis=0)
    elif topic == 'Abortion':
        query_1 = np.sum([model.wv.get_vector(word) for word in 'abortion'.split() if word in model.wv.vocab],axis=0)
        query_2 = np.sum([model.wv.get_vector(word) for word in 'unborn'.split() if word in model.wv.vocab],axis=0)
    
    sim_1 = cosine_similarity(query_1.reshape(1, -1), tw_vec)
    sim_2 = cosine_similarity(query_2.reshape(1, -1), tw_vec)
    
    sim = np.maximum(sim_1[0], sim_2[0])
    
    best_index = random.choice((np.argsort(sim.ravel())[::-1]%len(tw_vec))[:2])
    return sim>threshold, best_index, query_1, query_2

#function to suggest a relevant advertisement. In input the alignment (score>0 corresponds to conservative) 
# and the vector representation of the best tweet as above. It returns the closest advertisement (random between top 2)
# from the opposite side
def best_ad(best_vec, alignment):
    if alignment < 0:
        sim = cosine_similarity(best_vec.reshape(1, -1), con_v)
        ad_index = random.choice((np.argsort(sim.ravel())[::-1]%len(con_v))[:2])
        return '<b>'+df_con['title'][ad_index]+'</b> '+ df_con['message'][ad_index], df_con['advertiser'][ad_index]
    
    else:
        sim = cosine_similarity(best_vec.reshape(1, -1), lib_v)
        ad_index = random.choice((np.argsort(sim.ravel())[::-1]%len(lib_v))[:3])
        return '<b>'+df_lib['title'][ad_index]+'</b> '+ df_lib['message'][ad_index], df_lib['advertiser'][ad_index]