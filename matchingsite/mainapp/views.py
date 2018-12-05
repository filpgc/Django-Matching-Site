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
from django.utils import timezone
from django.contrib.auth.hashers import make_password

#from mainapp.templatetags.extras import display_message

# datetime library to get time for setting cookie
import datetime as D
import sys


appname='matchingsite'

def loggedin(view):
    def mod_view(request):
        if 'username' in request.session:
            username = request.session['uname']
            try: user = Member.objects.get(username=username)
            except Member.DoesNotExist: raise Http404('Member does not exist')
            return view(request, user)
        else:
            return render(request,'mainapp/not-logged-in.html',{})
    return mod_view


def index(request):
    context = { 'appname': appname }
    return render(request,'mainapp/index.html',context)

def signup(request):
    context = { 'appname': appname }
    return render(request,'mainapp/signup.html',context)
def hobbies(request):
    total=Hobby.objects.all()
    outdoor=total.filter(category="Out")
    indoor =total.filter(category='In')
    dict = {
        'hobby': total,
        'outdoor' : outdoor,
        'indoor' : indoor
    }
    return render(request, "mainapp/signup.html", context = dict)


def register(request):
    if 'fname' in request.POST and 'uname' in request.POST and 'password' in request.POST:
        u = request.POST['uname']
        f = request.POST['fname']
        p = request.POST['password']
        e = request.POST['email']
        print(request.POST['hobby'])
        user = Member(first_name= f, username =u, password =p, email =e)
        try:
            user.set_password(p)
            user.save()
        except IntegrityError: raise Http404('Username '+u+' already taken: Usernames must be unique')
        context = {
            'appname' : "hobby",
            'username' : u
        }
        return render(request,'mainapp/user-registered.html',context)

def login(request):
    if not ('username' in request.POST and 'password' in request.POST):
        context = { 'appname': appname }
        return render(request,'mainapp/login.html',context)
    else:
        username = request.POST['username']
        password = request.POST['password']
        try: member = Member.objects.get(username=username)
        except Member.DoesNotExist: raise Http404('User does not exist')
        if member.check_password(password):
            # remember user in session variable
            request.session['username'] = username
            request.session['password'] = password
            context = {
               'appname': appname,
               'username': username,
               'loggedin': True
            }
            response = render(request, 'mainapp/login.html', context)
            # remember last login in cookie
            now = D.datetime.utcnow()
            max_age = 365 * 24 * 60 * 60  #one year
            delta = now + D.timedelta(seconds=max_age)
            format = "%a, %d-%b-%Y %H:%M:%S GMT"
            expires = D.datetime.strftime(delta, format)
            response.set_cookie('last_login',now,expires=expires)
            return response
        else:
            raise Http404('Wrong password')

@loggedin
def logout(request, user):
    request.session.flush()
    context = { 'appname': appname }
    return render(request,'mainapp/logout.html', context)



