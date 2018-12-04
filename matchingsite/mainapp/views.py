from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import Http404
from mainapp.models import Member,Hobby, User
from django.db import IntegrityError

from django.http import HttpResponse
from django.template import loader
from django.template import RequestContext, loader
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.core import serializers

from .forms import RegistrationForm


def index(request):
    total=Hobby.objects.all()
    outdoor=total.filter(category="Out")
    indoor =total.filter(category='In')
    dict = {
        'hobby': total,
        'outdoor' : outdoor,
        'indoor' : indoor
    }
    return render(request, "mainapp/index.html", context = dict)


def register(request):
    if 'fname' in request.POST and 'uname' in request.POST and 'password' in request.POST:
        u = request.POST['uname']
        f = request.POST['fname']
        p = request.POST['password']
        e = request.POST['email']
        print(request.POST['hobby'])
        user = Member(first_name= f, username =u, password =p, email =e)
        try: user.save()
        except IntegrityError: raise Http404('Username '+u+' already taken: Usernames must be unique')
        context = {
            'appname' : "hobby",
            'username' : u
        }
        return render(request,'mainapp/index.html',context)


