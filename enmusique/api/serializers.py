from rest_framework import serializers
from .models import Room

""" 
What a serialized or does is it will take our model in this case, a room that has 
all of this Python related code. So it has actually, you know, code equals this host
equal this, whatever it is in Python. And it will translate this room into a JSON 
response. Take all the keys and turn them into strings
"""

class RoomSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Room
        # On each of our model we have a unique key
        fields = ('id', 'code', 'host', 'guest_can_pause', 'votes_to_skip', 'created_at')

class CreateRoomSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Room
        # Fields that we want to be sent as part of the post request
        # This is going to seriliaze a request, take the data from the request and make sure it's all correct
        fields = ('guest_can_pause', 'votes_to_skip')