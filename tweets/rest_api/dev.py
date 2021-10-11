from rest_framework import authentication, response
from django.contrib.auth import get_user_model

User = get_user_model()


class DevAuthentication(authentication.BasicAuthentication):

    def authenticate(self, request):
        qs = User.objects.filter(id=1)
        user = qs.first()
        print('The user:',user)
        return (user, None)
