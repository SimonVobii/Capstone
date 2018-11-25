from django.conf.urls import url
from account import views
from django.contrib.auth import views as auth_views
from . import forms

app_name = 'account'

"""
urlpatterns = [
	url(r'^$', views.LoginView.as_view(), name='sign-up-login'),
    url(r'^user_login/$', views.LoginView.as_view(), name='user_login'),
    #LoginView.as_view(), name='user_login'),
]
"""
