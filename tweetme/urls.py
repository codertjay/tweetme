from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from tweets.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view, name='home'),
    path('react/',TemplateView.as_view(template_name='react_via_dj.html')),
    path('api/tweets/',include('tweets.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
