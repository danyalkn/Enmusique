from django.urls import path
from .views import index

# This is where the main url is going to be sent when something is typed in

urlpatterns = [
    # Blank means any url that is sent, dispatch it and send it to our frontend homepage
    path('', index), 
    path('join', index),
    path('create', index)
]