from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from .credentials import CLIENT_ID, CLIENT_SECRET
from requests import post

def get_user_tokens(session_id):
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exist():
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

    response = post("'https://accounts.spotify.com/api/token", data={
        # sending a refresh token
        'grant_type': 'refresh_token', 
        'refresh_token': refresh_token, 
        'cliend_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    refresh_token = response.get('refresh_token')

    update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token)