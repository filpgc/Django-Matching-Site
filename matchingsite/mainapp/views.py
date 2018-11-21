from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import Http404
from django.http import HttpResponse
from django.template import loader
from django.template import RequestContext, loader
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.core import serializers

def index(request):
    return render(request, "mainapp/index.html")