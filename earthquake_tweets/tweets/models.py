from django.db import models

# Create your models here.
class Tweets(models.Model):
    created_at = models.DateTimeField()
    tweet_id = models.CharField(max_length=50)
    tweet_text = models.CharField(max_length=300)
    screen_name = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    is_relevant = models.BooleanField(default=False)
