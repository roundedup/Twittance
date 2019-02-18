
import numpy as np
from scipy.sparse import *
from random import shuffle
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.externals import joblib
from sklearn import linear_model


# load tfidf vectorizer and logistic regression classifier
tfidf = joblib.load('models/tweet_tfidf.pkl') 
lr = joblib.load('models/logistic_reg_LvsC.pkl') 


# compute probabilities of a tweet being conservative
# the total score is the mean
def party_predict(texts):
    x=tfidf.transform(texts)
    prediction=lr.predict_proba(x)
    score=np.mean(prediction[:,1])
    return score
