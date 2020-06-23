from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render
# importing Tweet from one dir above - best practice
from .models import Tweet

# Create your views here.
def home_view(request, *args, **kwargs):
  # Renderign template
  return render(request, "pages/home.html", context={}, status=200)

# Dynamic url routing
def tweet_detail_view(request, tweet_id, *args, **kwargs):
  # We can retrieve a tweet only if it exsists in db. Otherwise error has occured with server
  # RestAPI view - return json data
  # consume by JS, Swift itd..
  data = {
    "id": tweet_id,
    #"image_path": obj.image.url
  }
  status = 200
  try:
    obj = Tweet.objects.get(id=tweet_id)
    data['content'] = obj.content
  except: 
    data['message'] = "Not found"
    status = 404
  
  
  # rest API view
  return JsonResponse(data, status=status)