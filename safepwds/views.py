from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import *
from django.shortcuts import redirect
from cryptography.fernet import Fernet
# Create your views here.

class encpwd:


    def encpwd(self, s):

       return s.encode('utf_16','strict')

    def decpwd(self, s):
       return s.decode('utf_16','strict')
class addpassword(View,encpwd):
    def get(self,request):
        if request.session.has_key('email'):
            email=request.session['email']
        return render(request,'addpassword.html',{'email':email})

    def post(self,request):


        email=request.POST.get('email')
        field=request.POST.get('field')
        password=request.POST.get('password')
        e=encpwd()
        password=e.encpwd(password)
        #print(email,field,password)
        new_pwd=pwds.objects.create(email=email,field=field,pwd=password)
        #new_pwd.save()
        return redirect('signin')

class updatepwds(View,encpwd):
    def get(self,request):
        return render(request,'updatepwd.html')

    def post(self,request):
        if request.session.has_key('email'):
            email=request.session['email']
            userpwds=pwds.objects.filter(email=email)
            field=request.POST.get('field')
            for i in userpwds:
                if i.field ==field:
                    password=request.POST.get('password')
                    #print(field,password)
                    i.pwd=encpwd().encpwd(password)
                    i.save()
                    messages.success(request,'updated successfully')
                    return redirect('signin')
            messages.warning(request,'you have no password in field of ',field)
            return redirect('updatepwd')
        else:
            messages.warning(request,'some error occured !please login to continue ')
            return redirect('signin')
            pass

