from django.shortcuts import render

# Create your views here.
import smtplib
import ssl

from Tools.scripts import generate_token
from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from .models import *
from safepwds.models import *
import hashlib
from django.contrib.sites.shortcuts import get_current_site




class encpwd:


    def encpwd(self, s):

       return s.encode('utf_16','strict')

    def decpwd(self, s):
       return s.decode('utf_16','strict')

class usersession:
    def getuser(self,request):

        if request.session.has_key('email') :
            email=request.session['email']
            #print('------email---------',email)
            if email is not None:
                myuser=customer.objects.filter(email=email).first()
                #print(myuser)
                if myuser is not None:
                    return myuser
        return None

class classotp:
    def getOTP(self,email):
        import random
        otp=random.randint(100000,999999)
        userotp.objects.create(email=email,otp=otp)
        return otp


    def send_otp(self,request,email,myuser):
        smtp_server = "smtp.gmail.com"
        port = 587  # For starttls
        sender_email = "=@gmail.com"
        password = "password generated by google at 2 step verification"
        receiver_email = email
        current_site = get_current_site(request)
        notp=self.getOTP(email),
        message2 = render_to_string('email_confirmation.html', {
            'username': myuser.username,
            'name': myuser.first_name,
            'domain': current_site.domain,
            'otp': notp

        })
        # Create a secure SSL context
        context = ssl.create_default_context()

        # Try to log in to server and send email
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()  # Can be omitted
            server.starttls(context=context)  # Secure the connection
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            # TODO: Send email here
            server.sendmail(sender_email, receiver_email, message2)
            myuser.save()
            messages.success(request,'otp sent successfully')
            newotp=userotp.objects.create(email,notp)
            newotp.save()

        except Exception as e:
            return False
        finally:

            server.quit()
            return True




class register(View,usersession,classotp):



    def getdate(self):
        from datetime import date
        today = date.today()
        d1 = today.strftime("%d%m%Y")
        return d1

    def get(self,request):
        u=usersession()
        user=u.getuser(request)
        #print(user)
        if user:
            messages.success(request,'you are already signed in')
            pwd = pwds.objects.filter(email=user.email)
            e = encpwd()
            for i in pwd:
                # print(i.pwd)
                i.pwd = e.decpwd(i.pwd)
            return render(request,'dashboard.html',{'user':user,'passwords':pwd})
        else:
            return render(request,'register.html')



    def post(self,request):
        first_name=request.POST.get('first name')
        first_name=first_name.strip()
        last_name=request.POST.get('last name')
        last_name=last_name.strip()
        phone=request.POST.get('mobile_no')
        #print('phone',phone,first_name,last_name)
        email=request.POST.get('email')
        dob=request.POST.get('dob')
        password=request.POST.get('password')
        password2=request.POST.get('password2')
        username=first_name.lower()+last_name.lower()+phone[:5]+self.getdate()

        new_user=customer.objects.filter(email=email).first()
        if len(first_name) <3 or len(last_name)<3:
            messages.warning(request,'enter the valid name ')
            return redirect('register')

        if not first_name.isalpha() or not last_name.isalpha():
            messages.warning(request,'name must contain letters only ')
            return redirect('register')
        if new_user:
            messages.warning(request,'email already exist please login')
            return redirect('register')
        if len(phone) != 10:
            messages.warning(request,'enter valid mobile no ')
            return redirect('register')
        if password != password2:
            messages.warning(request,'passwords are not matching !')
            return redirect('register')



        #messages.warning()
        #myuser = User.objects.create_user(username,email,password)
        # myuser.first_name=first_name
        # myuser.last_name=last_name
        # myuser.email=email
        # myuser.is_active=False
        myuser=customer.objects.create(username=username,first_name=first_name,last_name=last_name,mobile=phone,is_active=False,dob=dob,password=password,email=email)


        notp=classotp()
        ###################################################################################################
        if notp.send_otp(request,email,myuser):
           # messages.success(request,'email sent successfully')
            return render(request,'emailsend.html',{'email':email})
        else:
            messages.warning(request,'some error occured !please try after some time ')
            return redirect('register')

class signin(View,usersession):

    def get(self,request):
        user = usersession().getuser(request)

        if user:
            pwd=pwds.objects.filter(email=user.email)
            e=encpwd()
            for i in pwd:
                #print(i.pwd)
                i.pwd=e.decpwd(i.pwd)

            return render(request, 'dashboard.html', {'user': user,'passwords':pwd,'no':len(pwd)})
        else:
            return render(request,'signin.html')
    def post(self,request):
        myuser = usersession().getuser(request)
        email = request.POST.get('email')
        password = request.POST.get('password')
        #print(email,password,myuser)
        if myuser is not None:
            u=customer.objects.filter(email=email).first()
            request.session['email']=email
            usersession().getuser(request)
            #print(myuser)
            pwd = pwds.objects.filter(email=email)
            e = encpwd()
            for i in pwd:
                #print(i.pwd)
                i.pwd = e.decpwd(i.pwd)
            return render(request,'dashboard.html',{'user':myuser,'passwords':pwd,'no':len(pwd)})


        #exist_user=authenticate(request,email=email,password=password)
        exist_user=customer.objects.filter(email=email).first()
        #print(exist_user)
        if exist_user is not None:
            #login(request,myuser)
            request.session['email'] = email
            pwd=pwds.objects.filter(email=email)
            e=encpwd()
            for i in pwd:
                i.pwd=e.decpwd(i.pwd)
                #print('dex')
            return render(request, 'dashboard.html', {'user': exist_user,'passwords':pwd})
        else:
            messages.warning(request,'wrong credentials')
            return redirect('signin')

    def decpwd(self,s):
        return hashlib.sha256(s.decode()).hexdigest()


class signout(View):
    def get(self,request):

        if request.session.has_key('email'):
            del request.session['email']
        return redirect('signin')
    def post(self,request):
        if request.session.has_key('username'):
            del request.session['username']
        return redirect('signin')


class otp(View):
    def get(self,request):
        return render(request,'emailsend.html')
    def post(self,request):
        email=request.POST.get('email')
        otp=request.POST.get('otp')
       # print(email,otp)
        otpuser=userotp.objects.filter(email=email).first()
        #print(otpuser.otp)
        if otpuser.otp==int(otp):
            otpuser.delete()
            myuser=customer.objects.filter(email=email).first()
            myuser.is_active=True
            myuser.save()
            request.session['email']=email
            return redirect('/signin')
        else:
            messages.warning(request,'enter correct otp')
            return render(request,'emailsend.html',{'email':email})

class changepassword(View):
    def get(self,request):
        return render(request,'changepassword.html')

    def post(self,request):
        myuser = usersession().getuser(request)
        if myuser is not None:
            email=myuser.email
            password=request.POST.get('password')
            password2=request.POST.get('password2')
            #print(password,password2)
            if password==password2:
                myuser=customer.objects.filter(email=email).first()
                myuser.password=password
                myuser.save()
                messages.success(request,'your password is success fully updated')
                return render(request, 'dashboard.html', {'user': myuser})
            else:
                messages.warning(request,'passwords are not matching ')
                return render(request,'signin.html',{'user':myuser})
        else:
            messages.warning(request,'some error occured ! login again to continue')
            return redirect('changepassword')

class forgotpassword(register):
    def get(self,request):
        return render(request,'emailsendforgotpassword.html')
    def post(self,request):
        email=request.POST.get('email')
        forgotmail=customer.objects.filter(email=email).first()
        if forgotmail is not None:
            r=register()
            if r.send_otp(request,email,forgotmail):
                messages.success(request,'otp is sent your mail address enter that otp ')
                return render(request,'emailsend2.html',{'email':email})
            else:
                messages.warning(request,'some error occured try again ')
                return redirect('forgotpassword')
        else:
            messages.warning(request,'enter valid mail id address! entered mail address is not in our records ')
            return redirect('forgotpassword')


class updatepassword(View):
    def get(self,request):
        email=request.GET.get('email')
        otp=request.GET.get('otp')

        emailuser=userotp.objects.filter(email=email).first()
        if emailuser.otp==int(otp):
            emailuser.delete()
            messages.success(request,'otp verified successfull')
            return render(request,'forgotpassword2.html',{'email':email})
        else:
            messages.warning(request,'enter correct otp')
            return render(request,'emailsend2.html',{'email':email})
    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        #print(password, password2)
        if password == password2:
            myuser = customer.objects.filter(email=email).first()
            myuser.password = password
            myuser.save()
            request.session['email']=email
            messages.success(request, 'your password is success fully updated')
            return render(request, 'dashboard.html', {'user': myuser})
        else:
            messages.warning(request, 'passwords are not matching ')
            return render(request, 'signin.html', {'user': email})









