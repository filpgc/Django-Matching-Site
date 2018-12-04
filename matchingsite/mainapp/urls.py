from django.urls import include, path, views


app_name='mainapp'
urlpatterns = [
    path('', include('mainapp.urls')),

]



