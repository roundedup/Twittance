# Twittance
## From Twitter utterance to political stance

[Twittance](http://www.twittance.com) 

is a tool that predicts whether a Twitter user has liberal or conservative views on a given
topic. It then suggests relevant ads based on the prediction. 
It uses two different vectorizations of tweets, one based on a custom word2vec, 
one on tf-idf. It was trained on a large dataset of tweets by politicians. 
Deployed through Flask, currently hosted on AWS. 
