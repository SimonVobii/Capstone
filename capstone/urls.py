from django.conf.urls import url, include
from django.urls    import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from account import views as account_views
from service import views as service_views

urlpatterns = [
    path('', views.homeView.as_view(), name = 'webapp-home'),
    path('register/', account_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login_paul.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout_paul.html'), name='logout'),
    path('survey/', account_views.survey, name='survey'),
    path('select/', service_views.select, name='select'),
    path('backtest/', service_views.backtest, name='backtest'),
    path('better/', service_views.better, name='better'),
    path('betterRender/', service_views.betterRender, name='betterRender'),
    path('goal/', service_views.goal, name='goal'),
    path('goalRender/', service_views.goalRender, name='goalRender'),
    path('demo/', service_views.demo, name='demo'),
    path('portfolio/', service_views.portfolio, name='portfolio'),
    path('admin/', admin.site.urls),
]