from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import hashlib

def homepage(request):
    return render(request, 'index.html')

def game(request):
    return render(request, 'game.html')

def aboutme(request):
    return render(request, 'aboutme.html')

def signup(request):
    if request.method == "GET":
        return render(request, "signup.html")
    elif request.method == "POST":
        email = request.POST.get("email")
        try:
            if User.objects.filter(email=email).exists():
                return render(request, "existingaccount.html")
            password = request.POST.get("password")
            password1 = request.POST.get("pasword")
            if password != password1:
                return render(request, "invalidpassword.html")
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()
            return render(request, "successfulsignup.html")
        except:
            return render(request, 'index.html')
        
def Login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        try:    
            username = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, "successfullogin.html")
            else:
                return render(request, "unsuccessfullogin.html")
        except:
            return render(request, 'index.html')
