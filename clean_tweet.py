
# coding: utf-8

from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import re

stop = set(stopwords.words('english'))
lemma = WordNetLemmatizer()
exclude_tweet={'"','%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '[', '\\', 
         ']', '^', '_', '`', '{', '|', '}', '~'}

# clean tweets by lowering, lemmatizing, removing stop word and some punctuation 
def clean_tweet(doc):
    doc=' '.join(re.sub("(\w+:\/\/\S+)"," ",doc).lower().split())
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    stop_free=stop_free.replace('/',' ').replace('-',' ').replace('!',' ! ').replace('?',' ? ').replace('$',' $ ')
    punc_free = "".join(ch for ch in stop_free if ch not in exclude_tweet)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

