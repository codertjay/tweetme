from django.db import models
from django.contrib.auth.models import User

import random

"""
In the likes field ManyToMany means that one tweet can have many user 
many users can have many tweet is similar to the foreign key but now we can have 
a list of users vs one user

To get or remove likes from Tweet
fav = User.objects.first() or any just get one user
obj = Tweet.objects.first() or anything just get one tweet from the database
obj.likes.remove(fav)
obj.likes.set(fav) # requires a queryset

"""


class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey('Tweet', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Tweet(models.Model):
    parent = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=250, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='tweet_user'
                                   , blank=True, through=TweetLike) # th
    image = models.FileField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    @property
    def is_retweet(self):
        return self.parent != None
