from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.utils.timezone import make_aware
from django.conf import settings
from .models import Tweets
from .process_tweets import load_tweets
import pandas as pd

n_tweets = 100
# Create your views here.
def index(request):
    latest_tweets_list = Tweets.objects.order_by("-created_at")[:min(n_tweets, Tweets.objects.count())]
    num_tweets = len(latest_tweets_list)
    num_relevant = len([tweet for tweet in latest_tweets_list if tweet.is_relevant])
    context = {
        "latest_tweets_list":latest_tweets_list,
        "num_tweets" : num_tweets,
        "num_relevant" : num_relevant,
    }
    return render(request, "tweets/home.html", context)

def ajax_accept_request(request):
    try :
        Tweets.objects.all().delete() #hapus semua tweet lama
        df = load_tweets(n_tweets)
        instances = []
        for a,b,c,d,e,f in zip(df["created_at"],
                                df["tweet_id"],
                                df["tweet_text"],
                                df["screen_name"],
                                df["name"],
                                df["informativeness"]):
            new_tweet = Tweets(
                created_at = make_aware(a),
                tweet_id = b,
                tweet_text = c,
                screen_name = d,
                name = e,
                is_relevant = f,
            )
            instances.append(new_tweet)
        Tweets.objects.bulk_create(instances)
        return JsonResponse({"success": True})
    
    except Exception as e:
        return JsonResponse({"success": False})

 