from django.shortcuts import render
from rest_framework import generics
from .serializers import RoomSerializer
from .models import Room

#To be able to accept http responses
# from django.http import HttpResponse
# All our endpoints will be, location of the web server

# Create your views here.

# Allow us to view all the rooms but also create a room
class RoomView(generics.ListAPIView):
    # What do we want to return? All the room objects
    queryset = Room.objects.all()
    # Room serliazer will make it readable
    serializer_class = RoomSerializer
