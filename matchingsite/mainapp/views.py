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
from django.utils import timezone
from django.contrib.auth.hashers import make_password



#from mainapp.templatetags.extras import display_message

# datetime library to get time for setting cookie
import datetime as D
import sys


appname='matchingsite'



#decorator
def loggedin(view):
    def mod_view(request):
        if 'username' in request.session:
            username = request.session['username']
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
    total=Hobby.objects.all()       # Querydict all the hobbies
    outdoor=total.filter(category="Out")            # hobbies filtered by category outdoor
    indoor =total.filter(category='In')             # hobbies filtered by category indoor
    dict = {
        'hobby': total,
        'outdoor' : outdoor,
        'indoor' : indoor
    }
    return render(request, "mainapp/signup.html", context=dict)



def register(request):
    if 'fname' in request.POST and 'uname' in request.POST and 'password' in request.POST:
        dict = retrieve(request)
        user = Member(username = dict[0],  first_name = dict[1],  email= dict[3])
        try:
            user.set_password(dict[2])
            user.save()
        except IntegrityError: raise Http404('Username '+ dict[0]+' already taken: Usernames must be unique')
        context = {
            'appname' : "hobby",
            'username' : dict[0]
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

@loggedin
def profile(request, user):
    user1=Member.objects.filter(username = user)
    if request.POST:
        dict = retrieve(request)
        Member.objects.update( first_name = dict[1], password = dict[2], email= dict[3] )
        
    print(user1)
    dict = {
        'appname': appname,
        'email':user1[0].email,
        'password':user1[0].password,
        'loggedin': True
    }
    return render(request, 'mainapp/profile.html', context = dict)


def retrieve(request):
    u = request.POST['uname']
    f = request.POST['fname']
    p = request.POST['password']
    e = request.POST['email']   
    dict = [u,f,p,e]
    return dict

