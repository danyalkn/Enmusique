from django.shortcuts import render
# gives us access to http status codes which we will need for our responses
from rest_framework import generics, status 
from .serializers import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse



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

# We're going to use post request instead of get because we're going to post that we got into the room
class JoinRoom(APIView):
    lookup_url_kwarg = 'code'
    def post(self, request, format=None): 
         # If the user doesn't already have a session with us
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        # with post request we can use data
        code = request.data.get(self.lookup_url_kwarg)
        if code != None: 
            room_result = Room.objects.filter(code=code)
            if len(room_result) > 0: 
                room = room_result[0]
                # With session we are able to store information relative to individual user/session
                # Storing this information in user session
                self.request.session['room_code'] = code
                return Response({'message': 'Room Joined!'}, status=status.HTTP_200_OK)
            
            return Response({'Bad Request': 'Invalid Room Code'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'Bad Request': 'Invalid post data, did not find a code key'}, status=status.HTTP_400_BAD_REQUEST)

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
                self.request.session['room_code'] = room.code
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            else:
                room = Room(host=host, guest_can_pause=guest_can_pause,
                            votes_to_skip=votes_to_skip)
                room.save()
                self.request.session['room_code'] = room.code
                return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)

        # .data will give us JSON formatted data
        return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)

# Send a get request and check if person is a room
"""
Going to return a JSON response. What this does is take a Python dictionary and serialize it, 
using a Jason serializer and then sends that information back to the front-end or sends it 
in the request. Similar to our room serializer. It's the exact same thing, except we're just 
going to take an arbitrary Python dictionary rather than a Python object, like a room or, you
know, like database models that we have.
"""
class UserInRoom(APIView): 
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        data = {
            'code': self.request.session.get('room_code')
        }

        return JsonResponse(data, status=status.HTTP_200_OK)

"""
I'm making this a post request because we're changing information on the server. We're going to 
be removing the information from the room code in the user session. So it makes sense to make that
a post request because posts usually means you're updating or adding or doing something on the 
server changing information.
"""
class LeaveRoom(APIView):
    def post(self, request, format=None):
        if 'room_code' in self.request.session:
            self.request.session.pop('room_code')
            host_id = self.request.session.session_key
            room_results = Room.objects.filter(host=host_id)
            if len(room_results) > 0: 
                room  = room_results[0]
                room.delete()
        return Response({'Message': 'Success'}, status=status.HTTP_200_OK)

class UpdateRoom(APIView):
    serializer_class = UpdateRoomSerializer
    # Patch is another word for updating. Just updating room
    def patch(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            code = serializer.data.get('code')

            queryset = Room.objects.filter(code=code)
            if not queryset.exists():
                return Response({'msg': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)
            room = queryset[0]
            user_id = self.request.session.session_key
            if room.host != user_id:
                return Response({'msg': 'You are not the host of this room'}, status=status.HTTP_403_FORBIDDEN)

            room.guest_can_pause = guest_can_pause
            room.votes_to_skip = votes_to_skip
            room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)

        return Response({'Bad Request': "Invalid Data..."}, status=status.HTTP_400_BAD_REQUEST)