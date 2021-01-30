from django.urls import path
from .views import index

#  We're doing this because django needs to know that this urls.py file belongs to the frontend app 
app_name = "frontend"

# This is where the main url is going to be sent when something is typed in

urlpatterns = [
    # Blank means any url that is sent, dispatch it and send it to our frontend homepage
    # Need formal names so when we call the redirect function we know which path to go to
    path('', index, name=""), 
    path('info', index),
    path('join', index),
    path('create', index),
    path('room/<str:roomCode>', index), 

]