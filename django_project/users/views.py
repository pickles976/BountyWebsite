from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from users.models import Profile
import os

auth_url_discord = "https://discord.com/api/oauth2/authorize?client_id=1000844725445726270&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fdiscord-register-redirect&response_type=code&scope=identify"
CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET")

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,f"Your account has been created")
            return redirect("login")

    else:
        form = UserRegisterForm()
    return render(request,"users/register.html",{"form":form})

@login_required
def discord_register(request):
    return redirect(auth_url_discord)

@login_required
def discord_register_redirect(request):
    code = request.GET.get("code")
    user = exchange_code(code)

    profile = Profile.objects.get(user=request.user)
    profile.discordname = user["username"] + "#" + user["discriminator"]
    profile.discordid = user["id"]
    profile.verified = False
    profile.save()
    
    return redirect("profile")

@login_required
def profile(request):

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f"Your account has been updated")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "u_form": u_form,
        "p_form": p_form,
    }
    return render(request,"users/profile.html",context)

# MOVE THESE CREDENTIALS TO ENV
def exchange_code(code):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:8000/discord-register-redirect",
        "scope": "identify"
    }
    print(data)
    headers={
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post("https://discord.com/api/oauth2/token",data=data,headers=headers)
    credentials = response.json()
    access_token = credentials["access_token"]
    response = requests.get("https://discord.com/api/v6/users/@me", headers={"Authorization": f"Bearer {access_token}"})
    user = response.json()
    return user

