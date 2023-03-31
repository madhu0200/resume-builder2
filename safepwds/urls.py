from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from .views import *
urlpatterns = [
    path('passwords',addpassword.as_view(),name='passwords'),
    path('updatepwd',updatepwds.as_view(),name='updatepwd'),
]