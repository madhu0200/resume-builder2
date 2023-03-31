from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from .views import *
urlpatterns = [
    path('',register.as_view(),name="home"),
    path('register/',register.as_view(),name='register'),
    path('signin/',signin.as_view(),name='signin'),
    path('signout/',signout.as_view(),name='signout'),
    #path('activate/<uidb64>/<token>', activate, name='activate'),
    path('otp/',otp.as_view(),name='otp'),
    path('changepassword',changepassword.as_view(),name='changepassword'),
    path('forgotpassword',forgotpassword.as_view(),name='forgotpassword'),
    path('updatepassword',updatepassword.as_view(),name='updatepassword'),
    path('passwords',include('safepwds.urls'),name='passwords'),
]