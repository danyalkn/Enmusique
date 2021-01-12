from django.shortcuts import render

#To be able to accept http responses
from django.http import HttpResponse
# All our endpoints will be, location of the web server

# Create your views here.
def main(request): 
    return HttpResponse("<h1>Hello</h1>")
