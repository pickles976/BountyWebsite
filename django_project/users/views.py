from email import message
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
from .forms import ProfileImageForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from users.models import Profile, ProfileImage
import os
from django.forms import modelformset_factory

sigil_url = "https://sigilhq.com/room-auth/check-is-verified/"

auth_url_discord = "https://discord.com/api/oauth2/authorize?client_id=1000844725445726270&redirect_uri=https%3A%2F%2Fwww.foxholebounties.com%2Fdiscord-register-redirect&response_type=code&scope=identify"

# HEROKU
if ("True" == os.environ.get("DJANGO_DEBUG")):
    # LOCAL
    auth_url_discord = "https://discord.com/api/oauth2/authorize?client_id=1000844725445726270&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fdiscord-register-redirect&response_type=code&scope=identify"


CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET")
SIGIL_TOKEN = os.environ.get("SIGIL_TOKEN")

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

    ImageFormSet = modelformset_factory(ProfileImage,
                                        form=ProfileImageForm)

    oldteam = request.user.profile.team

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        i_form = ImageFormSet(request.POST, request.FILES,
                               queryset=ProfileImage.objects.none())
                               
        if u_form.is_valid() and p_form.is_valid() and i_form.is_valid():

            if str(oldteam) != str(p_form.cleaned_data["team"]):
                request.user.profile.verified = False
                request.user.profile.save()

            u_form.save()
            p_form.save()

            for form in i_form.cleaned_data:
                #this helps to not crash if the user   
                #do not upload all the photos
                if form:
                    ProfileImage.objects.filter(profile=request.user.profile).delete()
                    image = form['image']
                    photo = ProfileImage(profile=request.user.profile,image=image)
                    photo.save()

            messages.success(request,f"Your account has been updated")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        i_form = ImageFormSet(queryset=ProfileImage.objects.none())

    context = {
        "u_form": u_form,
        "p_form": p_form,
        "i_form": i_form,
    }
    return render(request,"users/profile.html",context)

@login_required
def verify(request):

    if request.user.profile.team.team == "COLONIAL":

        headers = {
            "token": SIGIL_TOKEN
        }
        # send user ID to endpoint
        endpoint = sigil_url+request.user.profile.discordid
        response = requests.get(endpoint,headers=headers)
        if response.status_code == 200:

            status = response.json()

            if status["isVerified"] == True:
               messages.success(request,"You are now verified!")
               request.user.profile.verified=True
               request.user.profile.save()
            else:
                messages.error(request,"You are not verified on SIGIL!")

        else:
            messages.error(request,"Error connecting to SIGIL server")

        return redirect("profile")

    elif request.user.profile.team.team == "WARDEN":

        messages.error(request,"Wardens not yet supported, GTFO BLUEBERRIES!")
        return redirect("profile")

    messages.error(request,"You must join a team to be verified!")
    return redirect("profile")

def exchange_code(code):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://foxhole-bounties.herokuapp.com/discord-register-redirect",
        "scope": "identify"
    }
    headers={
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post("https://discord.com/api/oauth2/token",data=data,headers=headers)
    credentials = response.json()
    access_token = credentials["access_token"]
    response = requests.get("https://discord.com/api/v6/users/@me", headers={"Authorization": f"Bearer {access_token}"})
    user = response.json()
    return user