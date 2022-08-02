from distutils.log import info
from email import header, message
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
from .forms import ProfileImageForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from users.models import Profile, ProfileImage
import os
from django.forms import modelformset_factory
from django.utils import timezone
from users.utils import getUserInfoFromToken

sigil_url = "https://sigilhq.com/room-auth/check-is-verified/"
sigil_bot_url = "https://sigilhq.com/room-auth/check-is-verified-on-certified/"

auth_url_discord = "https://discord.com/api/oauth2/authorize?client_id=1000844725445726270&redirect_uri=https%3A%2F%2Fwww.foxholebounties.com%2Fdiscord-register-redirect&response_type=code&scope=guilds%20identify"
REDIRECT_URI = "https://www.foxholebounties.com/discord-register-redirect"

# LOCAL SETTINGS
if ("True" == os.environ.get("DJANGO_DEBUG")):
    # LOCAL
    auth_url_discord = "https://discord.com/api/oauth2/authorize?client_id=1000844725445726270&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fdiscord-register-redirect&response_type=code&scope=guilds%20identify"
    REDIRECT_URI = "http://localhost:8000/discord-register-redirect"

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
    infoDict = exchange_code(code)
    
    user = infoDict["user"]

    token = infoDict["access_token"]
    refresh_token = infoDict["refresh_token"]

    profile = Profile.objects.get(user=request.user)
    profile.discordname = user["username"] + "#" + user["discriminator"]
    profile.discordid = user["id"]
    profile.verified = False

    # refresh token
    profile.discordToken = token
    profile.refreshToken = refresh_token
    profile.dateAuthorized = timezone.now()
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

    # USER IS COLONIAL
    if request.user.profile.team.team == "COLONIAL":

        headers = {
            "token": SIGIL_TOKEN
        }
        
        endpoint = sigil_bot_url+request.user.profile.discordid
        guilds = getUserInfoFromToken(request.user.profile.discordToken)["guilds"]
        body = {}
        body["servers"] = [guild["id"] for guild in guilds]

        response = requests.post(endpoint,headers=headers,data=body)
        if response.status_code == 200:
            status = response.json()
            isVerified = status["isVerified"]
            isSigilVerified = status["isSigilVerified"]
            
            if isSigilVerified or isVerified:
                messages.success(request,"You are now verified!")
                request.user.profile.verified=True
                request.user.profile.save()
                return redirect("profile")
        else:
            messages.error(request,"Error connecting to SIGIL server")

        messages.error(request,"You are not verified on SIGIL or any SigilBot servers! Visit https://discord.gg/rRmkN6S to verify!")
        
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
        "redirect_uri": REDIRECT_URI,
        "scope": "identify guilds"
    }
    headers={
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post("https://discord.com/api/oauth2/token",data=data,headers=headers)
    credentials = response.json()

    print(credentials)

    access_token = credentials["access_token"]

    infoDict = getUserInfoFromToken(access_token)
    infoDict["refresh_token"] = credentials["refresh_token"]
    infoDict["access_token"] = access_token

    return infoDict