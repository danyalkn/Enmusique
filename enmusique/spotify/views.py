from django.shortcuts import render, redirect
from .credentials import REDIRECT_URI, CLIENT_ID, CLIENT_SECRET
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .util import update_or_create_user_tokens, is_spotify_authenticated

# Create your views here.
class AuthURL(APIView):
    def get(self, request, format=None):
        # This scope is what information we're going to need access too
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'
        # Step 1 of spotify authorization https://developer.spotify.com/documentation/general/guides/authorization-guide/
        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            # reason for code is we are requesting a code back that will allow us to authenticate a user
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url
        return Response({'url': url}, status=status.HTTP_200_OK)
        """
        Will generate a url for us, the output of this will be a string
        Want to have the frontend get this url and send the request from there.
        This api endpoint is going to return a url that we can go to authenticate our spotify application
        """
    """
    From the front end I'm going to call this api endpoint. Then going to take the url that's returned to us and 
    going to redirect to that page. Then from there, that url once the user is done authorizing us, we'll redirect 
    to this function right here vvvv
    """
# Covering step 2 of spotify authorization https://developer.spotify.com/documentation/general/guides/authorization-guide/
def spotify_callback(request, format=None): 
    """
    Then from this function we'll send the request for the tokens. Store the tokens and then redirect back to our original 
    application so that's why i'm redirecting to frontend at the end of this function
    """
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code', 
        'code': code, 
        'redirect_uri': REDIRECT_URI, 
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    # After we get this response we want to get: 
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')
    # Looks to create session
    if not request.session.exists(request.session.session_key):
        request.session.create()
    update_or_create_user_tokens(request.session.session_key, access_token, token_type, expires_in, token_type)

    return redirect('frontend:')

class IsAuthenticated(APIView):
    def get(self, request, format=None): 
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        return Response({"status": is_authenticated}, status=status.HTTP_200_OK)