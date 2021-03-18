import pandas as pd
import numpy as np
import re
import string
from keras.preprocessing.text import tokenizer_from_json
from keras.preprocessing.sequence import pad_sequences
from keras import models
import tweepy
import json

def clean_text(text):
  """
  fungsi untuk menghilangkan link, whitespace, melower case,
  dan menghapus tanda baca dan angka
  """
  #menghapus link
  text = re.sub("\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*", " ", text)
  #menghilangkan whitespace
  text = re.sub('\s+', ' ', text).strip()
  #menghapus tanda baca
  text = text.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
  #menjadikan huruf kecil
  text = text.lower()
  #menghapus angka
  text = re.sub(r'\d+', '', text)
  return text

def load_tweets(n):
    ### SCRAPE TWEETS ###
    access_token = 
    access_token_secret = 
    consumer_key = 
    consumer_secret =

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    tweets = []
    for tweet in tweepy.Cursor(api.search, q="earthquake", lang="en").items(n):
        try: 
            data = [tweet.created_at,
                     tweet.id, tweet.text, 
                     tweet.user._json['screen_name'], 
                     tweet.user._json['name'], 
                     tweet.user._json['created_at'], 
                     tweet.entities['urls']]
            data = tuple(data)
            tweets.append(data)
        except tweepy.TweepError as e:
            print(e.reason)
            continue
        except StopIteration:
            break
    print("Loaded tweets from twitter")

    ### CLEAN TWEETS TEXT ###
    df = pd.DataFrame(tweets, 
                  columns = ['created_at','tweet_id', 
                             'tweet_text', 'screen_name', 
                             'name', 'account_creation_date', 
                             'urls'])
    X_test = df["tweet_text"].apply(lambda x:clean_text(x))
    
    with open('tweets/tokenizer.json') as f:
        data = json.load(f)
        tokenizer = tokenizer_from_json(data)

    X_test = tokenizer.texts_to_sequences(X_test)
    X_test = pad_sequences(X_test, maxlen=30)
    print("Cleaned tweets")

    ### CLASSIFY THE TWEETS ###
    # load json and create model
    path = "tweets/"
    json_file = open(path+'model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = models.model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(path+"model.h5")
    print("Loaded model from disk")

    y_preds = (loaded_model.predict(X_test) > 0.5).astype("int32")
    y_preds = [True if val==1 else False for val in y_preds ]
    df["informativeness"] = y_preds
    print("Finished prediction")
    return df

