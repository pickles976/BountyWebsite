from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .forms import UserForm, BountyForm, CompletionForm
from .models import User, Bounty, Completion


def index(request):
    return HttpResponse("Hello")

# USER
def create_user(request):
    context = {}
    form = UserForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        new_user = form.save()
        return HttpResponseRedirect(f"/polls/user/{new_user.pk}/")

    context["form"] = form
    return render(request,"polls/create_user.html",context) # need a template for this

def user(request,unique_id):

    return HttpResponse(User.objects.get(pk=unique_id))

# BOUNTY
def create_bounty(request):
    context = {}
    form = BountyForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        new_bounty = form.save()
        return HttpResponseRedirect(f"/polls/bounty/{new_bounty.pk}/")

    context["form"] = form
    return render(request,"polls/create_bounty.html",context) # need a template for this

def bounty(request,unique_id):

    return HttpResponse(Bounty.objects.get(pk=unique_id))

# COMPLETION
def create_completion(request):
    context = {}
    form = CompletionForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        new_completion = form.save()
        return HttpResponseRedirect(f"/polls/completion/{new_completion.pk}/")

    context["form"] = form
    return render(request,"polls/create_completion.html",context) # need a template for this

def completion(request,unique_id):

    return HttpResponse(Completion.objects.get(pk=unique_id))

