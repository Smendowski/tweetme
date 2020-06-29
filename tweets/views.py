import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
# importing Tweet from one dir above - best practice
from django.utils.http import is_safe_url

from .forms import TweetForm
from .models import Tweet
from .serializers import TweetSerializer

# Without it... csrf_token error or mismatch
from django.views.decorators.csrf import csrf_protect

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
  # Renderign template
  return render(request, "pages/home.html", context={}, status=200)

@csrf_protect
def tweet_create_view(request, *args, **kwargs):
  data = request.POST or None
  serializer = TweetSerializer(data)
  if serializer.is_valid():
    serializer.save()
  return JsonResponse({}, status=0)


@csrf_protect
def tweet_create_view_pure_django(request, *args, **kwargs):
  user = request.user
  if not request.user.is_authenticated:
    user = None
    if request.is_ajax():
      return JsonResponse({}, status=401)
    return redirect(settings.LOGIN_URL)
  #print('ajax:', request.is_ajax()) False
  # TweetForm class can be initialized with data or not (None)
  form = TweetForm(request.POST or None)
  #print('Post data is: ', request.POST)
  next_url = request.POST.get("next") or None
  print('next url: ', next_url)
  if form.is_valid():
    obj = form.save(commit=False)
    # None for annonymous user
    obj.user = user
    # do other form related logic
    # save to the database
    obj.save()
    if request.is_ajax():
      # created items status
      return JsonResponse(obj.serialize(), status=201)
    if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
      return redirect(next_url)
    form = TweetForm()
  if form.error:
    if request.is_ajax():
      return JsonResponse(form.error, status=400)
  return render(request, 'components/form.html', context={"form": form})


def tweet_list_view(request, *args, **kwargs):
  # RestAPI view
  qs = Tweet.objects.all()
  tweets_list = [x.serialize() for x in qs]
  data = {
    "isUser": False,
    "response": tweets_list
  }
  return JsonResponse(data)


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