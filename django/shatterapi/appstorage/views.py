from django.shortcuts import render
from django.http import Http404
import json

from . import algorithms

def index(request):
    raise Http404("Page does not exist")

# Create your views here.
def client(request):
    # Parse request
    jsonFile = json.loads(request.body)

    # Call James's function
    returnData = algorithms.jamesAlgorithm(jsonFile['name'], jsonFile['id'])

    # Store return details in database

    if request.method == 'GET':
        # Will actually spit out the return value
    #

    return HttpResponse("hello world")
