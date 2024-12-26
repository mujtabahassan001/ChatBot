from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('enter_room')  
        else:
            return HttpResponse("Invalid email or password")
    return render(request, 'home/login.html')

def enter_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        if room_name:
            return redirect('chat', room_name=room_name)  
    return render(request, 'home/enter_room.html')

def logout_view(request):
    logout(request)
    return redirect('login') 

def chat(request, room_name):
    return render(request, 'home/chat.html', {
        'room_name': room_name
    })



