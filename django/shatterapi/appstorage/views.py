from django.shortcuts import render
from django.http import Http404, HttpResponse
import json

from . import algorithms
from appstorage.models import Subreddit

# Create your views here.
def index(request):
    # Parse request
    print(request)
    jsonFile = json.loads(request.body)
    print(f"Json file: {jsonFile}")

    print(jsonFile["name"])

    # Check the DB
    related = Subreddit.objects.filter(name=jsonFile["name"])
    if related.count() == 1:
        return HttpResponse(json.dumps(x))
    

    # Call James's function
    returnData = algorithms.jamesAlgorithm(jsonFile['name'], jsonFile['id'])

    # Store return details in database
    newSubreddit = Subreddit(name=returnData['name'], id=jsonFile['id'], subs=returnData['subs'])
    newSubreddit.save()

    newSubSerialised = {"name" : returnData['name'], "id" : jsonFile['id'], "subs" : returnData['subs']}

    return HttpResponse(json.dumps(newSubSerialised))
