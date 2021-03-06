from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import Http404
from mainapp.models import Member, Hobby, User
from django.db import IntegrityError
from django.http import HttpResponse
from django.http import JsonResponse
import json
from datetime import date
from django.utils.timezone import now

from django.core import serializers

# datetime library to get time for setting cookie
import datetime as D
from django.core.mail import EmailMessage

appname = 'matchingsite'


# decorator
def loggedin(view):
    def mod_view(request):
        if 'username' in request.session:
            username = request.session['username']
            try:
                user = Member.objects.get(username=username)
            except Member.DoesNotExist:
                raise Http404('Member does not exist')
            return view(request, user)
        else:
            return render(request, 'mainapp/not-logged-in.html', {})

    return mod_view

 # view for index/, shows to the user the index page where they can select to register or login
def index(request):
    context = {'appname': appname}
    return render(request, 'mainapp/index.html', context)


def signup(request):
    context = {'appname': appname}
    return render(request, 'mainapp/signup.html', context)


def hobbies(request):
    total = Hobby.objects.all()  # Querydict all the hobbies
    outdoor = total.filter(category="Out")  # hobbies filtered by category outdoor
    indoor = total.filter(category='In')  # hobbies filtered by category indoor
    dict = {
        'hobby': total,
        'outdoor': outdoor,
        'indoor': indoor
    }
    return render(request, "mainapp/signup.html", context=dict)

 # register view, is called by the signup page and registers the user with the information entered on the html form
def register(request):
    condition = register
    if 'fname' in request.POST and 'uname' in request.POST and 'password' in request.POST:
        dict = retrieve(request, condition)
        user = Member(username=dict[0], first_name=dict[1], email=dict[2], dob=dict[4], gender=dict[5],image=dict[6])
        try:
            user.set_password(dict[7])
            user.save()
            for hobby in dict[3]:  # dict[3] is the list of hobbies
                hob, _ = Hobby.objects.get_or_create(name=hobby)
                user.hobby.add(hob)
        except IntegrityError:
            raise Http404('Username ' + dict[0] + ' already taken: Usernames must be unique')
        email = EmailMessage('Hobmatch: Thanks for signing up!', 'Thank you for signing up '+ dict[0] + ' please access the hobmatch to get on matching!', to=[dict[2]])
        email.send()
        context = {
            'appname': "hobby",
            'username': dict[0],
            'image': user.image  # lets user select his image to add to his profile
        }
        return render(request, 'mainapp/user-registered.html', context)


def calculate_age(dob): #view that returns the age from the dob of the user.
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def agerange(min_age, max_age):#view that returns a filtered list of members that have their age within the age range given by the arguments the function takes
    current = now().date()
    min_date = date(current.year - min_age, current.month, current.day)
    max_date = date(current.year - max_age, current.month, current.day)
    (Member.objects.filter(dob__lt=min_date, dob__gt=max_date))
    return Member.objects.filter(dob__lt=min_date, dob__gt=max_date)


def login(request):#is used to login the user
    if not ('username' in request.POST and 'password' in request.POST):
        context = {'appname': appname}
        return render(request, 'mainapp/login.html', context)
    else:
        username = request.POST['username']
        password = request.POST['password']
        try:
            member = Member.objects.get(username=username)
        except Member.DoesNotExist:
            raise Http404('User does not exist')
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
            max_age = 365 * 24 * 60 * 60  # one year
            delta = now + D.timedelta(seconds=max_age)
            format = "%a, %d-%b-%Y %H:%M:%S GMT"
            expires = D.datetime.strftime(delta, format)
            response.set_cookie('last_login', now, expires=expires)
            return response
        else:
            raise Http404('Wrong password')


@loggedin#decorator that verifies the user is logged in. if he is, the following view can be called
def logout(request, user):  # view for logout/, flushes the session and logs out the user
    request.session.flush()
    context = {'appname': appname}
    return render(request, 'mainapp/logout.html', context)


@loggedin
def profile(request, user):#view that will allow the user to edit his profile
    user1 = Member.objects.filter(username=user)  # QuerySet object
    condition = profile
    if request.POST:
        dict = retrieve(request, condition)
        user1.update(first_name=dict[1], email=dict[2], dob=dict[4])  # updates the fullname and email
        user.hobby.clear()  # clears hobby
        for hobby in dict[3]:  # dict[4] is the list of hobbies
            hob, _ = Hobby.objects.get_or_create(name=hobby)
            user.hobby.add(hob)
    total = Hobby.objects.all()  # Queryset, all the hobbies
    outdoor = total.filter(category="Out")  # hobbies filtered by category outdoor
    indoor = total.filter(category='In')  # hobbies filtered by category indoor
    dict = {
        'appname': appname,
        'email': user1[0].email,
        'password': user1[0].password,
        'username': user1[0].username,
        'fullname': user1[0].first_name,
        'loggedin': True,
        'age': calculate_age(user1[0].dob),
        'outdoor': outdoor,
        'indoor': indoor,
        'image': user1[0].image,
        'gender': user1[0].gender,
        'dob': user1[0].dob
    }
    return render(request, 'mainapp/profile.html', context=dict)


@loggedin
def upload_image(request, user):  # view of uploadimage/, allows user to upload the image on his profile by using ajax
    user1 = Member.objects.filter(username=user)
    if 'img_file' in request.FILES:
        image_file = request.FILES['img_file']
        user.image = image_file
        user.save()
        return HttpResponse(user.image.url)
    else:
        raise Http404('Image file not received')


# retrieve all the fields passed in the request
def retrieve(request, condition):
    u = request.POST['uname']
    f = request.POST['fname']
    e = request.POST['email']
    g = request.POST['gender']
    h = request.POST.getlist('hobby')
    d = request.POST['dob']
    i = request.FILES.get('img_file',False)
    dict = [u, f, e, h, d, g, i]  # creates an array containing all the fields
    if condition == register:
        p = request.POST['password']
        dict.append(p)
    return dict


@loggedin
def hobby(request, user):
    hobby = user.hobby.all()
    context = serializers.serialize('json', hobby)
    return JsonResponse(context, safe=False)


def sorting(members, user): # sorts the user in regards to how many hobbies they have in common
    count = {}
    current = 0
    user_hobbies = user.hobby.all()
    members = members.exclude(username=user.username)
    for x in members:
        for y in user_hobbies:
            for z in x.hobby.all():
                if y == z:
                    current = current + 1
        count[str(x)] = current
        current = 0
    return sorted(count.items(), key=lambda x: x[1], reverse=True)


@loggedin
def filter(request, user): # view for the filters, both age and gender. does not return anything. the filtering is done with an ajax call.
    val = request.POST.get('val')
    gender = request.POST.get('gender')
    filtered = Member.objects.all()
    if val == '0':
        filtered = agerange(0, 30)
    elif val == '1':
        filtered = agerange(30, 50)
    elif val == '2':
        filtered = agerange(50, 100)
    if gender == 'M':
        filtered = filtered.filter(gender='M')
    elif gender == 'F':
        filtered = filtered.filter(gender='F')
    members = filtered
    members = excludematched(members, user)
    sort = sorting(members, user)
    context = json.dumps(sort)

    return JsonResponse(context, safe=False)


@loggedin
def homepage(request, user):# view of the homepage. 
    members = Member.objects.all()
    members = excludematched(members, user)#excludes matched users from the list of users that will be presented to the logged in user
    sort = sorting(members, user)#sorts the remaining list of users and saves it in sort.
    context = {
        "members": sort, #passes the sorted list of users in the context
        "loggedin":True
    }
    return render(request, 'mainapp/homepage.html', context)#renders the sorted list of users that the logged in user is not matched with.


# exclude already matched memebrs, in order to show only the unmatched available ones
def excludematched(members, user):
    for match in user.match.all():
        members = members.exclude(username=match)
    return members


@loggedin
def match(request, user):#view that lets users match with the match button. is used by an ajax call
    name = request.POST['username']
    matched = Member.objects.get(username=name)
    email = EmailMessage('Hobmatch: You have been matched', ' Congratulations '+ matched.username + ' You have been matched on hobmatch by ' + user.username + ' Make sure to keep in touch! Here, you can contact him via his email address :) ' + user.email, to=[matched.email]) #fills the email to be sent to the user that has been matched. Check settings.py for the email properties
    email.send()#sends the email
    user.match.add(matched)
    matches = user.match.all()
    context = serializers.serialize('json', matches)
    return JsonResponse(context, safe=False)


@loggedin
def unmatch(request, user):#view that is used in ajax, allows users to unmatch on the mymatches page with the unmatch button
    name = request.POST['username']
    matched = Member.objects.get(username=name)
    email = EmailMessage('Hobmatch: You have been unmatched', 'Bummer '+ matched.username + ' You have been unmatched on hobmatch.. by ' + user.username+' Better luck next time', to=[matched.email])
    email.send()
    user.match.remove(matched)
    matches = user.match.all()
    context = serializers.serialize('json', matches)
    return JsonResponse(context, safe=False)


@loggedin
def mymatches(request, user):#view of the my matches page. Sorts users of hobmatch and checks that they are matched to the logged in users
    matches = user.match.all()
    count = {}
    dict = []
    for x in matches:
        for y in user.hobby.all():
            for z in x.hobby.all():
                if y == z:
                    dict.append(y)
        count[str(x)] = dict
        dict = []
    sort = sorted(count.items(), key=lambda x: len(x[1]), reverse=True)

    context = {
        "match": sort,
        "loggedin": True
    }
    return render(request, 'mainapp/mymatches.html', context)


# profile of the selected user
def users_profile(request, username):
    profile = Member.objects.get(username=username)
    context = {
        "fullname": profile.first_name,
        "age": calculate_age(profile.dob),
        "email": profile.email,
        "username": profile.username,
        "gender": profile.gender,
        "image": profile.image,
        "loggedin":True, #fixes users having to login again when looking at a different user's profile
        "hobbies": profile.hobby.all()
    }
    return render(request, 'mainapp/view_profile.html', context)
