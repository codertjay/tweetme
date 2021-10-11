from django.contrib import admin
from .models import Tweet, TweetLike


"""
what i did here is to connect the TweetLike to the Tweet for me to see the tweetlike
below the tweet that i am adding like to using inlines in tweet model
"""


class TweetLikeAdmin(admin.TabularInline):
    model = TweetLike


class TweetAdmin(admin.ModelAdmin):
    inlines = [TweetLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['content', 'user__username', 'user__email']

    class Meta:
        model = Tweet


admin.site.register(Tweet, TweetAdmin)
