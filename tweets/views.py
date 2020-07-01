import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
# importing Tweet from one dir above - best practice
from django.utils.http import is_safe_url
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .forms import TweetForm
from .models import Tweet
from .serializers import TweetSerializer, TweetActionSerializer

# Without it... csrf_token error or mismatch
from django.views.decorators.csrf import csrf_protect

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
  # Renderign template
  return render(request, "pages/home.html", context={}, status=200)


# pass methods we want to support
@api_view(['POST']) # http method the client === POST
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
  data = request.POST or None
  serializer = TweetSerializer(data = request.POST)
  if serializer.is_valid(raise_exception=True):
    serializer.save(user = request.user)
    return Response(serializer.data, status=201)
  return Response({}, status=400)

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
  qs = Tweet.objects.all()
  serializer = TweetSerializer(qs, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
  qs = Tweet.objects.filter(id=tweet_id)
  if not qs.exists():
    return Response({}, status=404)
  obj = qs.first()
  serializer = TweetSerializer(obj)
  return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request,  *args, **kwargs):
  '''
  id is required.
  Action options are:
  like, unlike, retweet
  '''
  serializer = TweetActionSerializer(data=request.POST)
  if serializer.is_valid(raise_exception=true):
    data = serializer.validated_data
    # Mapowanie pól z serializera 
    tweet_id = data.get("id")
    action = data.get("action")
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
      return Response({}, status=404)
    obj = qs.first()
    
    if action == "like":
      obj.likes.add(request.user)
    elif action == "unlike":
      obj.likes.remove(request.user)
    elif action == "retweet":
      # to do 
      pass

  return Response({"message":"Tweet removed"}, status=200)


@api_view(['GET', 'DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
  qs = Tweet.objects.filter(id=tweet_id)
  if not qs.exists():
    return Response({}, status=404)
  qs = qs.filter(user = request.user)
  if not qs.exists():
    return Response({"message": "You cannot delete this tweet"}, status=404)
  obj = qs.first()
  obj.delete()
  return Response({"message":"Tweet removed"}, status=200)


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


def tweet_list_view_pure_django(request, *args, **kwargs):
  # RestAPI view
  qs = Tweet.objects.all()
  tweets_list = [x.serialize() for x in qs]
  data = {
    "isUser": False,
    "response": tweets_list
  }
  return JsonResponse(data)


# Dynamic url routing
def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
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