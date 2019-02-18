# Twittance
## From Twitter utterance to political stance

[Twittance](http://www.twittance.com) is a tool that predicts whether a Twitter user has liberal or conservative views on a given
topic. It then suggests relevant ads based on the prediction. 
It uses two different vectorizations of tweets, one based on a custom word2vec, 
one on tf-idf. It was trained on a large dataset of tweets by politicians. 
Deployed through Flask, currently hosted on AWS. 

After the user inputs a Twitter handle and a topic the app downloads the latest ~1k tweets from that 
account using the Twitter API through Tweepy. The tweets are converted to vectors using word2vec embeddings 
and are classified are filtered by an SVM classifier to retain only those of political content. Cosine similarity
is then used to filter for only texts about the input topic. These remaining tweets are classified as either
liberal or conservative using tfidf representation + logistic regression classifier. So that the user's view 
on the topic can be assigned to one of those two sides. Finally an advertisement from the opposite side but close in content
is suggested.

The vector representations have been trained on a 1M+ dataset of tweets from US politicians.
The same dataset has been used to train the SVM classifier (using a hand labeled subset of ~1k tweets)
and the logistic regression model obtaining ~0.85 accuracy,
under the assumption each tweet from a user can be labeled as the user itself as either liberal or conservative 
(this works only on average). 
Cosine similarity is used for topic filtering and for selecting an advertisement from the propublica.org dataset
of Facebook political ads.
## Content


<b>twittance.py</b>: the main app code, which executes what described above

<b>clean_tweet.py</b>: function to prepare the tweets for vectorization (removing punctuation and stop words, lemmatizing) 

<b>get_tweets.py</b>: function that downloads the latest tweets from a given user through Twitter API + Tweepy

<b>party_predict.py</b>: function used for the liberal vs conservative classification (based on tfidf + logistic regression)

<b>pick_a_tweet.py</b>: contains the functions based on the word2vec representation. For noise and topic filtering 
on tweets (using SVM and cosine similarity respectively) and for suggesting a relevant ad from the opposite side (based on cosine similarity)

