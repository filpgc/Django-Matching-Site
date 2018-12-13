from django.urls import path

from mainapp import views


urlpatterns = [
	# main page
    path('', views.index, name='index'),
    # signup page
    path('signup/', views.hobbies, name='signup'),
    # register new user
	path('register/', views.register, name='register'),
    # login page
    path('login/', views.login, name='login'),
    # logout page
    path('logout/', views.logout, name='logout'),
    #selects the current hobbies
    path('hobby/', views.hobby, name='hobby'),
    # members page
    #path('members/', views.members, name='members'),
    # friends page
    #path('friends/', views.friends, name='friends'),
    # user profile edit page
    path('profile/', views.profile, name='profile'),
    # messages page    # Ajax: check if user exists
    #path('checkuser/', views.checkuser, name='checkuser'),
    # Ajax: post a new message
    # Ajax: delete a message
    # Ajax: upload new profile image
    #path('uploadimage/', views.upload_image, name='uploadimage'),
    path('agerange/', views.agerange, name='agerange'),
    path('homepage/', views.homepage, name='homepage'),
    path('homepage/match/', views.match, name='match'),
    path('homepage/filteredage/', views.filter, name='filteredage'),
    path('mymatches/',views.mymatches, name ='mymatches'),
    path('mymatches/unmatch/', views.unmatch, name='unmatch'),
    path('homepage/<str:username>/',views.users_profile,name='users_profile')

]






