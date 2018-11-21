from django.urls import include, path


app_name='mainapp'
urlpatterns = [
    path('', include('mainapp.urls')),
]




#    # ex: /polls/5/
# the 'name' value as called by the {% url %} template tag
# path('<int:question_id>/', views.detail, name='detail'),
# ex: /polls/5/results/
# path('<int:question_id>/results/', views.results, name='results'),
# ex: /polls/5/vote/
# path('<int:question_id>/vote/', views.vote, name='vote'),
