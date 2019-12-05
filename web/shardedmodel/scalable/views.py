from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("This page should list mapping from logical shard to physical shard.")
    
