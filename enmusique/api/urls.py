# This file will store all the urls, local to this app
from django.urls import path
from .views import main


urlpatterns = [
    # If we get a url that is blank, that doesn't have anything on it, call the main 
    # function and do whatever it says
    path('home', main),
    path('', main)
]
