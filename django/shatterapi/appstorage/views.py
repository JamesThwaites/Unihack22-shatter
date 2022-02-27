from django.shortcuts import render
from django.http import Http404
import json

from . import algorithms
from appstorage.models import Subreddit

def index(request):
    raise Http404("Page does not exist")

# Create your views here.
def client(request):
    # Parse request
    jsonFile = json.loads(request.body)
    
    # Check the DB
    related = Subreddit.objects.filter(name=jsonFile['name'])
    if related.count() == 1:
        return HttpResponse(json.dumps(x))
    

    # Call James's function
    returnData = algorithms.jamesAlgorithm(jsonFile['name'], jsonFile['id'])

    # Store return details in database
    newSubreddit = Subreddit(name=returnData['name'], id=returnData['id'])
    newSubreddit.save()

    return HttpResponse(json.dumps(newSubreddit))
