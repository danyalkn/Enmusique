# This file will store all the urls, local to this app
from django.urls import path
from .views import RoomView, CreateRoomView, GetRoom, JoinRoom, UserInRoom, LeaveRoom, UpdateRoom


urlpatterns = [
    # If we get a url that is blank, that doesn't have anything on it, call the main 
    # function and do whatever it says
    path('room', RoomView.as_view()), 
    path('create-room', CreateRoomView.as_view()),
    path('get-room', GetRoom.as_view()),
    path('join-room', JoinRoom.as_view()),
    path('user-in-room', UserInRoom.as_view()),
    path('leave-room', LeaveRoom.as_view()),
    path('update-room', UpdateRoom.as_view())
]
