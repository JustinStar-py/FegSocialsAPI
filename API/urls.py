from django.urls import path
from .views import twitter_get_data,insta_get_data

urlpatterns = [
    path('Twitter/<slug:slug>',twitter_get_data),
    path('Instagram/<slug:slug>',insta_get_data)
]
