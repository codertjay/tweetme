from django.test import TestCase
from .models import Tweet
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()  # active user in this project


class TweetTestCase(TestCase):
    def setUp(self):
        """ this is the database so right now the files i create here
         are the once that are in the database"""
        self.user = User.objects.create_user(username='fav', password='thankgod12')
        self.userB = User.objects.create_user(username='fav-2', password='thankgod12')
        Tweet.objects.create(content='my tweet 1', user=self.user)
        Tweet.objects.create(content='my tweet 2', user=self.user)
        Tweet.objects.create(content='my tweet 3', user=self.user)
        self.currentCount = Tweet.objects.all().count()

    def test_user_created(self):
        self.assertEqual(self.user.username, 'fav')

    def test_tweet_created(self):
        tweet_obj = Tweet.objects.create(content='my tweet 4', user=self.user)
        self.assertEqual(tweet_obj.id, 4)
        self.assertEqual(tweet_obj.user, self.user)

    # logging in with this client
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password="thankgod12")
        return client

    def test_tweet_list_api_view(self):
        client = self.get_client()
        response = client.get("/api/tweets/")
        self.assertEqual(response.status_code, 200)
        print(response.json())
        self.assertEqual(len(response.json()), 3)

    def test_action_like_api_view(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/",
                               {"id": 1, "action": "like"})
        print(response.status_code)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 1)

    def test_action_Unlike_api_view(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/",
                               {"id": 2, "action": "like"})
        like_count = response.json().get("likes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(like_count, 1)
        response = client.post("/api/tweets/action/", {'id': 2, "action": "unlike"})
        like_count = response.json().get("unlike")
        self.assertEqual(like_count, None)

    def test_action_retweet_api_view(self):
        client = self.get_client()
        current_count = self.currentCount
        response = client.post("/api/tweets/action/",
                               {"id": 2, "action": "retweet"})
        action = response.json().get("retweet")
        print(response.status_code)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_tweet_id = data.get('id')
        self.assertNotEqual(2, new_tweet_id)
        self.assertEqual(current_count + 1, new_tweet_id)

    def test_tweet_create_api_view(self):
        client = self.get_client()
        user = self.userB
        current_count = self.currentCount
        response = client.post("/api/tweets/create/",
                               {"id": 4, "content": "my current", "user": user})
        count = response.json().get("id")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(current_count + 1, count)

    def test_tweet_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/tweets/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        id = data.get("id")
        self.assertEqual(id, 1)

    # i am having error in here solve it later
    def test_tweet_delete_api_view(self):
        client = self.get_client()
        response = client.delete("/api/tweets/2/delete/")
        print('response.status_code', response.data)
        self.assertEqual(response.status_code, 200)
        client = self.get_client()
        response = client.delete("/api/tweets/1/delete/")
        self.assertEqual(response.status_code, 404)
        response = client.delete("/api/tweets/3/delete/")
        self.assertEqual(response.status_code, 404)
