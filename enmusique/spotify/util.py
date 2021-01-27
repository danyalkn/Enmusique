from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from .credentials import CLIENT_ID, CLIENT_SECRET
from requests import post, put, get

BASE_URL = "https://api.spotify.com/v1/me/"

def get_user_tokens(session_id):
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    else: 
        return None


# This function is going to save our tokens
def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    tokens = get_user_tokens(session_id)
    """
    This is telling us that your token is going to expire in 3600 seconds which is one hour so what I'm
    going to do is convert this into a time stamp because i don't want to just store the seconds, i want 
    to store the time at which our token actually expires so i'm going to get the current time and then 
    add an hour to it and store that in the database so that way it's really easy for me to check if the 
    token's expired
    """
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens: 
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])
    else: 
        tokens = SpotifyToken(user=session_id, access_token=access_token, refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        tokens.save()

def is_spotify_authenticated(session_id):
    # if we don't have tokens, we are not authenticated
    tokens = get_user_tokens(session_id)
    if tokens: 
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(session_id)
        
        return True

    return False
    
def refresh_spotify_token(session_id):
    refresh_token = get_user_tokens(session_id).refresh_token

    response = post('https://accounts.spotify.com/api/token', data={
        # sending a refresh token
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in') 

    update_or_create_user_tokens(
        session_id, access_token, token_type, expires_in, refresh_token)

# We can use this function to send a request to any Spotify Endpoint
def execute_spotify_api_request(session_id, endpoint, post_=False, put_=False):
    tokens = get_user_tokens(session_id)
    # Need a "bearer" before sending token
    headers = {'Content-Type': 'application/json', 'Authorization': "Bearer " + tokens.access_token}
    
    if post_: 
        post(BASE_URL + endpoint, headers=headers)
    if put_: 
        put(BASE_URL + endpoint, headers=headers)

    # Sending empty dictionary because it's syntax for a get request
    response = get(BASE_URL + endpoint, {}, headers=headers)

    try: 
        return response.json()
    except:
        return {"Error": "Issue with request"}


def play_song(session_id):
    return execute_spotify_api_request(session_id, "player/play", put_=True)

def pause_song(session_id):
    return execute_spotify_api_request(session_id, "player/pause", put_=True)