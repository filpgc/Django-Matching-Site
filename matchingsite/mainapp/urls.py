from django.urls import path

from mainapp import views


urlpatterns = [
    # welcome page
    path('', views.index, name='index'),
    # signup page
    path('signup/', views.hobbies, name='signup'),
    # register new user
    path('register/', views.register, name='register'),
    # login page
    path('login/', views.login, name='login'),
    # logout page
    path('logout/', views.logout, name='logout'),
    # selects the current hobbies
    path('hobby/', views.hobby, name='hobby'),
    # user profile edit page
    path('profile/', views.profile, name='profile'),

    # the user matches page
    path('mymatches/', views.mymatches, name='mymatches'),
    # homepage with all the available matches
    path('homepage/', views.homepage, name='homepage'),

    # Ajax: match with a member
    path('homepage/match/', views.match, name='match'),
    # Ajax: upload image
    path('profile/uploadimage/', views.upload_image, name='uploadimage'),
    # Ajax: filter available matches
    path('homepage/filtered/', views.filter, name='filteredage'),
    # Ajax: unmatch with a member
    path('mymatches/unmatch/', views.unmatch, name='unmatch'),

    # members page
    path('homepage/<str:username>/', views.users_profile, name='users_profile'),
    path('mymatches/<str:username>/', views.users_profile, name='users_profile'),


]










