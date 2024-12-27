from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import CustomUser

import random
from django.core.mail import send_mail
from django.conf import settings

otp_storage = {}

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user:
            otp = random.randint(100000, 999999)
            otp_storage[email] = otp

            send_mail(
                'Your OTP for Login',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            request.session['temp_email'] = email
            request.session['temp_password'] = password

            return redirect('otp_verify')  
        else:
            return HttpResponse("Invalid email or password")
    return render(request, 'home/login.html')


def otp_verify(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        email = request.session.get('temp_email')

        if email and otp_storage.get(email) == int(otp):
            del otp_storage[email] 
            user = authenticate(request, email=email, password=request.session['temp_password'])
            if user:
                login(request, user)
                request.session['success_message'] = f'({email}) logged in successfully'
                return redirect('enter_room')  
        else:
            return render(request, 'home/otp.html', {'error': 'Invalid OTP. Please try again.'})
    
    return render(request, 'home/otp.html')


def user_signup(request):
    if request.method == 'POST':
        name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'home/signup.html', {'error': 'Passwords do not match.'})

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'home/signup.html', {'error': 'Email is already registered.'})

        user = CustomUser.objects.create_user(email=email, password=password, first_name=name, last_name=last_name)
        user.save()
        return redirect('login')

    return render(request, 'home/signup.html')


def enter_room(request):
    success_message = request.session.get('success_message', None)
    if success_message:
        del request.session['success_message']  
    
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        if room_name:
            return redirect('chat', room_name=room_name)  
    return render(request, 'home/enter_room.html', {'success': success_message})

def logout_view(request):
    logout(request)
    return redirect('login') 

def chat(request, room_name):
    return render(request, 'home/chat.html', {
        'room_name': room_name
    })



