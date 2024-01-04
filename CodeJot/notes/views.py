from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt

from .models import User, Note


def index(request):
    if request.user.is_authenticated:
        notes = Note.objects.filter(notes_user=request.user)
        return render(request, "notes/index.html", {
            "notes": notes,
        })

    # else
    return HttpResponseRedirect(reverse("login"))


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("main"))

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
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("main"))
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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("main"))


@csrf_exempt
def add_note(request):
    if request.method != "POST" or request.user.is_authenticated is not True:
        return HttpResponseRedirect(reverse("main"))

    data = json.loads(request.body)
    print(data)
    note = Note(note_data=data, notes_user=request.user)
    note.save()
    return HttpResponse(status=204)


def main(request):
    return render(request, "notes/main.html")
