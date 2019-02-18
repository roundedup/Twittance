
# coding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import os
from clean_tweet import *
import pandas as pd

#Twitter API credentials
consumer_key = 'xyz'
consumer_secret = 'xyz'
access_key = 'xyz'
access_secret = 'xyz'

def get_tweets(screen_name, n_tweets):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    #authorize twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #tweets list
    all_tweets = []

    #initial request for most recent tweets (200 max allowed)
    try:
        new_tweets = api.user_timeline(screen_name = str(screen_name), count=20, tweet_mode="extended")

        #append tweets
        all_tweets.extend(new_tweets)

        #checkpoint
        checkpoint = all_tweets[-1].id - 1

        #keep grabbing tweets until n_tweets are grabbed or none left
        while (len(new_tweets) > 0) and (len(all_tweets) < n_tweets):

            #subsiquent requests use max_id to prevent duplicates
            new_tweets = api.user_timeline(screen_name = screen_name, count=200, max_id=checkpoint, tweet_mode="extended")

            #save most recent tweets
            all_tweets.extend(new_tweets)

            #update the id of the oldest tweet less one
            checkpoint = all_tweets[-1].id - 1

        #transform the tweepy tweets into a 2D array that will populate the dataframe
        out_tweets = [[tweet.id_str, tweet.created_at, tweet.full_text.encode("utf-8")] for tweet in all_tweets]
        out_tweets = out_tweets[:min(n_tweets,len(out_tweets))]

    except:
        out_tweets = {'c1' : [], 'c2' : [], 'c3' : []}

    return pd.DataFrame(out_tweets, columns = ['id', 'date', 'text'])
