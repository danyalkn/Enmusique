from django.shortcuts import render
# gives us access to http status codes which we will need for our responses
from rest_framework import generics, status 
from .serializers import RoomSerializer, CreateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response



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

# when we call our GetRoom, code will be our room name
class GetRoom(APIView): 
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'
    
    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None: 
            room = Room.objects.filter(code=code)
            if len(room) > 0:
                data = RoomSerializer(room[0]).data
                data['is_host'] = self.request.session.session_key == room[0].host
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Room Not Found:': 'Invalid Room Code.'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({'Bad Request': 'Code parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)


# APIView allows to override some default methods
class CreateRoomView(APIView): 
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        # If the user doesn't already have a session with us
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        # Gets the data makes it readable to python
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            """
            If the user already has an active room, instead of making a new one, it will
            grab the active one and just update the options of that. 
            """
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
            else: 
                room = Room(host=host, guest_can_pause=guest_can_pause, votes_to_skip=votes_to_skip)
                room.save()

        # .data will give us JSON formatted data
        return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)