from django.http import HttpResponse, Http404
from django.shortcuts import render
# importing Tweet from one dir above - best practice
from .models import Tweet

# Create your views here.
def home_view(request, *args, **kwargs):
  return HttpResponse("<h1>HelloWorld</h1>")

# Dynamic url routing
def tweet_detail_view(request, tweet_id, *args, **kwargs):
  # We can retrieve a tweet only if it exsists in db. Otherwise error has occured with server
  try:
    obj = Tweet.objects.get(id=tweet_id)
  except: 
    raise Http404
  return HttpResponse(f"<h1>Hello {tweet_id} - {obj.content} </h1>")