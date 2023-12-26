from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Note

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        notes = Note.objects.filter(notes_user=request.user)
        return render(request, "notes/index.html", {
            "notes": notes,
        })

    # else
    return HttpResponseRedirect(reverse("login"))

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "notes/login.html", {
                "message": "Invalid username and/or password."
            })
    
    # else
        
    return render(request, "notes/login.html")


def signup(request):
    if request.method == "POST":
        print('posted')
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password_confirm = request.POST["password_confirm"]
        
        if password != password_confirm:
            return render(request, "notes/signup.html", {
                "message": "Passwords must match."
            })

        # else
        if User.objects.filter(username=username).exists():
            return render(request, "notes/signup.html", {
                "message": "Username already taken."
                })
            
        user = User.objects.create_user(username, email, password)
        user.save()
        login(request, user)
        
        return HttpResponseRedirect(reverse("index"))

        
    # else
    return render(request, "notes/signup.html")


def logout(request):
    logout(request)

def add_note(request):
    pass