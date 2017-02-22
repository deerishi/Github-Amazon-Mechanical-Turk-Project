from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from try1 import views
from django.contrib.auth import views as auth_views

app_name='try1'

urlpatterns = [
    url(r'^$', views.homePage),
    url(r'^sentiments/$', views.Sentiment1List.as_view()),
    #url(r'^login/$', views.user_login, name='loginn'),
    url(r'^login/', auth_views.login, {'template_name': 'try1/login.html'}, name='login'),
    #url(r'^logout/$', auth_views.logout, name='logout'), 
    #url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    url(r'^users/', views.UserList.as_view()), 
    url(r'^main/', views.main, name='main'), 
    url(r'^(?P<comment_id>[0-9]+)/comment/', views.displayComment, name='dpc'), 
    url(r'^(?P<comment_id>[0-9]+)/markComment/$', views.processMarkedSentence, name='tabulateComments'), 
    url(r'^dummy/', views.dummy, name='dummy'), 
    url(r'^(?P<comment_id>[0-9]+)/displayErrorForCheckboxes/', views.displayErrorForCheckboxes, name='displayErrorForCheckboxes'), 
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^register/', views.register, name='register'), 
]

urlpatterns = format_suffix_patterns(urlpatterns)
