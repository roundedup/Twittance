import os
import flask, flask.views
from flask import Markup, render_template
from flask import jsonify
from flask import request
import time
import random

from get_tweets import *
from clean_tweet import *
from party_predict import *
from pick_a_tweet import *
    
app = flask.Flask(__name__)

app.vars = {}

class Main(flask.views.MethodView):
    def get(self):
        return render_template('index.html')
 
app.add_url_rule('/',view_func=Main.as_view('main'), methods=["GET"])



placeholder_name = "LeoDiCaprio" # handle in case no input is given


@app.route('/_compute')
def compute():
    
    #retrieve input handle
    screen_name = str(request.args.get('s_handle')).replace('@','').replace(' ','').lower()
    
    #retrieve input topic
    topic = str(request.args.get('s_topic'))
    
    if screen_name == '':
        screen_name = placeholder_name
        
    tweets = get_tweets(screen_name, 1500)
    
    #remove retweets
    tweets = tweets[(~ tweets['text'].str.startswith('rt')) & (~ tweets['text'].str.startswith('RT'))].reset_index(drop=True)
    
    #return in case of account with less than 10 tweets
    if len(tweets)<10:
        return jsonify(result=0, prediction = 'Not enough tweets!', sample_tweet = '', handle='', ref= '', topic = topic, sample_pr = '', advertiser = '')
        
    
    #prepare tweets for vectorization
    clean_texts = np.array([clean_tweet(txt.decode("utf-8")) for txt in tweets['text']])
    
    #compute vector representations of tweets
    tw_vec = np.array([tweet2vec(tw) for tw in clean_texts])
    
    #predict whether tweets are political or not in content and select only the political ones
    y_pol = svm_polornot.predict(tw_vec)
    tw_vec = tw_vec[y_pol==1]
    tweets = tweets[y_pol==1].reset_index(drop=True)
    clean_texts = clean_texts[y_pol==1]
    
    #filter for topic (index is the index of a sample tweet on the topic)
    y_relevant, index, query_1, query_2 = relevant_tweets(tw_vec, topic, 0.6)
    
    relevant_texts = clean_texts[y_relevant]
    
    #predict the alignment. The score is between -100 and 100 (from liberal to conservative)
    #two different cases depending on whether the user has written about the topic or not
    if len(relevant_texts)>0:
        
        score = party_predict(relevant_texts)
        stance = 'Uncertain'
        best_vec = tw_vec[index]
        
        sample_text = tweets['text'][index].replace('  ',' ')
        sample_id = tweets['id'][index]
        sample_href= "<a style='font-size: 16px' href= https://twitter.com/"+screen_name+"/status/"+sample_id+">"+' @'+screen_name+"</a>"
        
        handle_out = '@'+screen_name
        
        
    else:
        score = min(party_predict(clean_texts),95)
        stance = 'Uncertain in general'
        best_vec = query_1 
        sample_text = "No tweets on the topic"
        sample_id = ""
        sample_href = ""
        
        handle_out = ''

                       
                       
    # add uncertainty range         
    if score>10:
        stance = stance.replace('Uncertain', 'Conservative')
    if score<-10:
        stance = stance.replace('Uncertain', 'Liberal')
    
    # find best ad from opposite side
    sample_ad_text, sample_ad_author = best_ad(best_vec, score)
    
    if screen_name == 'leodicaprio' and topic == 'Climate change':
        sample_ad_text = "Predicting climate temperatures isn't science - it's science fiction."
        sample_ad_author = 'PragerU'
        
    return jsonify(result=score, prediction = stance, sample_tweet = sample_text, handle=handle_out, ref= sample_href, topic = topic, sample_pr = sample_ad_text, advertiser = sample_ad_author)
    
    
    
    

# Default port:
if __name__ == '__main__':
    app.debug = True
    app.run()