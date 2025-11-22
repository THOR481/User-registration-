from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random
from .models import *
import os
import resend
# Create your views here.
def signup(request):

    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        username=request.POST.get('username')

        if User.objects.filter(email=email).exists():
            messages.error(request,'Email already in use!')
        elif User.objects.filter(username=username).exists():
            messages.error(request,'Username already in use!')       
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            # generate and send otp
            otp = send_otp(email)
            
            # create profile and save otp
            Profile.objects.create(
                user=user,
                otp=otp
            )

            messages.success(request,'User successfully registered.')
            return redirect('verify_otp')

        return redirect('signup')

    return render(request,'signup.html')



def send_otp(email):
    otp=str(random.randint(100000,111111))        
    resend.api_key = os.getenv("RESEND_API_KEY")

    resend.Emails.send({
        "from": "User Registration <onboarding@resend.dev>",
        "to": email,
        "subject": "Your Login OTP",
        "html": f"<p>Your OTP is <strong>{otp}</strong></p>",
    })

    return otp

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')

        try:
            profile = Profile.objects.get(otp=otp)
            profile.verified=True
            profile.save()
            user = profile.user

            # login success
            request.session['username'] = user.username
            return redirect('home')

        except Profile.DoesNotExist:
            messages.error(request, "Invalid OTP")
            return redirect('verify_otp')

    return render(request, 'verify_otp.html')

        
def signin(request):

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=User.objects.get(username=username)
        existing_user=Profile.objects.get(user=user)
        try:
            if user.check_password(password) and existing_user.verified==True:
                request.session['user_id']=user.id
                request.session['username']=user.username
                return redirect('home')
            else:
                messages.error(request,'incorrect password')
                return redirect('signup')

        except User.DoesNotExist:
            messages.error(request,'user not found !')
            return redirect('signup')
        
    return render(request,'signin.html')

def home(request):
    return render(request,'home.html',{'username':request.session.get('username')})

def logout(request):
    request.session.flush()
    return redirect('signup')

