from cgitb import text
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from requests import request
from .models import Bounty, Completion, Images, Acceptance, Message, War, Channel, BountyNotification
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import modelformset_factory
from django.contrib import messages
from .forms import ImageForm, BountyForm, CompletionForm, TextForm
from .filters import BountyFilter
import os
from django.core.paginator import Paginator
from bounty.utils import shouldSendNotif
from users.models import Profile, DailyVisit

BASE_URL = os.environ.get("BASE_URL")

def about(request):
    return render(request,"bounty/about.html",{"title": "About"})

# List view of Bounties
# class BountyListView(LoginRequiredMixin, ListView):
#     model = Bounty
#     template_name = "bounty/home.html"
#     context_object_name = "bounties"
#     ordering = ["-date_posted"]
#     paginate_by = 10

#     def get_queryset(self):

#         if not self.request.user.profile.verified:
#             messages.error(self.request,"You are unverified! Please verify to access the Bounty board!")
#             return Bounty.objects.none()

#         # filter bounties by user team
#         return Bounty.objects.filter(team=self.request.user.profile.team).prefetch_related("images_set","completion_set","acceptance_set").order_by("-date_posted")

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["filter"] = BountyFilter(self.request.GET, queryset=self.get_queryset())
#         return context

@login_required
def bountyListView(request):

    if not request.user.profile.verified:
        messages.error(request,"You are unverified! Please verify to access the Bounty board!")
        return redirect("bounty-about")

    context = {}

    filtered_bounties = BountyFilter()

    # initial page load
    if len(request.GET) == 0:
        filtered_bounties = BountyFilter(
            request.GET,
            queryset=Bounty.objects.filter(team=request.user.profile.team).filter(is_completed=False).prefetch_related("images_set","completion_set","acceptance_set").order_by("-date_posted")
        )
    else:
        filtered_bounties = BountyFilter(
            request.GET,
            queryset=Bounty.objects.filter(team=request.user.profile.team).prefetch_related("images_set","completion_set","acceptance_set").order_by("-date_posted")
        )


    context["filter"] = filtered_bounties

    paginated_filtered_persons = Paginator(filtered_bounties.qs, 10)

    page_number = request.GET.get("page")
    bounty_page_obj = paginated_filtered_persons.get_page(page_number)

    context["bounty_page_obj"] = bounty_page_obj

    return render(request,"bounty/home.html",context=context)



# List view of bounties for currently authenticated user
class UserBountyListView(LoginRequiredMixin, ListView):

    # model = Bounty
    template_name = "bounty/user_bounties.html" # <app>/<model>_<viewtype>.html
    context_object_name = "bounties"
    paginate_by = 10

    def get_queryset(self):

        if not self.request.user.profile.verified:
            messages.error(self.request,"You are unverified! Please verify to access the Bounty board!")
            return Bounty.objects.none()

        user = get_object_or_404(User,username=self.kwargs.get("username"))

        if not self.request.user.profile.team == user.profile.team:
            return Bounty.objects.none()


        bounties = Bounty.objects.filter(author=user).prefetch_related("images_set","completion_set","acceptance_set")
        completions = Completion.objects.filter(author=user).prefetch_related("images_set")
        combined = list(bounties) + list(completions)
        combined = sorted(combined,key=lambda x: x.date_posted)
        return combined

# view for creating bounties
@login_required
def postBountyView(request):

    if not request.user.profile.verified:
        messages.error(request,"You are unverified! Please verify to access the Bounty board!")
        return redirect("bounty-about")
 
    ImageFormSet = modelformset_factory(Images,
                                        form=ImageForm, extra=4)
    #'extra' means the number of photos that you can upload   ^
    if request.method == 'POST':
    
        bountyForm = BountyForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Images.objects.none())
    
    
        if bountyForm.is_valid() and formset.is_valid():

            post_form = bountyForm.save(commit=False)
            post_form.author = request.user
            post_form.team = request.user.profile.team
            post_form.war = War.objects.all().latest("pk")
            post_form.save()
    
            for form in formset.cleaned_data:
                #this helps to not crash if the user   
                #do not upload all the photos
                if form:
                    image = form['image']
                    photo = Images(bounty=post_form,image=image)
                    photo.save()

            # send messages to all subscribed channels
            all_channels = Channel.objects.all()

            for channel in all_channels.iterator():

                if channel.team == post_form.team and shouldSendNotif(post_form.jobtype,channel.types):
                    url = BASE_URL + reverse("bounty-detail",args=[post_form.pk])
                    notif = BountyNotification(channel=channel,text=f"{request.user.profile.discordname} posted a {post_form.jobtype} bounty: {url}")
                    notif.save()

            # use django messages framework
            messages.success(request,"Bounty created successfully")
            return redirect("bounty-detail",post_form.pk)
        else:
            print(bountyForm.errors, formset.errors)
    else:
        bountyForm = BountyForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'bounty/post_bounty_form.html',{'bountyForm': bountyForm, 'formset': formset})

# View for looking at a Bounty
class BountyDetailView(LoginRequiredMixin, DetailView):
    model = Bounty

    def get_context_data(self, **kwargs):

        if not self.request.user.profile.verified:
            messages.error(self.request,"You are unverified! Please verify to access the Bounty board!")
            return redirect("bounty-about")

        # user may not see other teams's bounty
        if not Bounty.objects.get(pk=self.kwargs.get('pk')).team == self.request.user.profile.team:
            return redirect("bounty-about")

        context = super().get_context_data(**kwargs)
        context['completions'] = Completion.objects.filter(bounty=self.object).prefetch_related("images_set")
        return context

#
class BountyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Bounty
    fields = ["title", "description","region","coordinates","jobtype"]

    def form_valid(self,form):

        if not self.request.user.profile.verified:
            messages.error(self.request,"You are unverified! Please verify to access the Bounty board!")
            return redirect("bounty-about")

        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        bounty = self.get_object()
        if self.request.user == bounty.author:
            return True
        return False

class BountyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Bounty
    success_url = "/"

    def test_func(self):

        if not self.request.user.profile.verified:
            messages.error(self.request,"You are unverified! Please verify to access the Bounty board!")
            return False

        bounty = self.get_object()
        if self.request.user == bounty.author:
            return True
        return False

# view for creating completions
@login_required
def postCompletionView(request,bounty):

    if not request.user.profile.verified:
        messages.error(request,"You are unverified! Please verify to access the Bounty board!")
        return redirect("bounty-about")

    # Only same team can post completions on other bounties
    if not Bounty.objects.get(pk=bounty).team == request.user.profile.team:
        return redirect("bounty-about")
 
    ImageFormSet = modelformset_factory(Images,
                                        form=ImageForm, extra=4)
    #'extra' means the number of photos that you can upload   ^
    if request.method == 'POST':

        if len(Completion.objects.filter(author=request.user).filter(bounty=bounty)) > 0:
            messages.error(request,"You have already created a completion for this bounty!")
            return redirect("bounty-detail",bounty)
    
        completionForm = CompletionForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Images.objects.none())
    
    
        if completionForm.is_valid() and formset.is_valid():
            bounty = Bounty.objects.get(pk=bounty)
            post_form = completionForm.save(commit=False)
            post_form.author = request.user
            post_form.bounty = bounty
            post_form.save()
    
            for form in formset.cleaned_data:
                #this helps to not crash if the user   
                #do not upload all the photos
                if form:
                    image = form['image']
                    photo = Images(completion=post_form,image=image)
                    photo.save()

            # Create message
            url = BASE_URL + reverse("completion-detail",args=[post_form.pk])
            m = Message(user=bounty.author,text=f"{request.user.profile.discordname} submitted a completion for your bounty: {url}")
            m.save()

            # use django messages framework
            messages.success(request,"Completion created successfully")
            return redirect("completion-detail",post_form.pk)
        else:
            print(completionForm.errors, formset.errors)
    else:
        completionForm = CompletionForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'bounty/post_completion_form.html',{'completionForm': completionForm, 'formset': formset})


class CompletionDetailView(LoginRequiredMixin, DetailView):

    model = Completion

    def get_context_data(self, **kwargs):

        if not self.request.user.profile.verified:
            messages.error(self.request,"You are unverified! Please verify to access the Bounty board!")
            return redirect("bounty-about")

        if not Completion.objects.get(pk=self.kwargs.get('pk')).bounty.team == self.request.user.profile.team:
            return redirect("bounty-about")
            
        context = super().get_context_data(**kwargs)
        return context

class CompletionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Completion
    success_url = "/"

    def test_func(self):

        if not self.request.user.profile.verified:
            messages.error(self.request,"You are unverified! Please verify to access the Bounty board!")
            return redirect("bounty-home")

        # Only the Completion creator can delete their own completion
        if not Completion.objects.get(pk=self.kwargs.get('pk')).author == self.request.user:
            return redirect("bounty-about")

        completion = self.get_object()
        if self.request.user == completion.author:
            return True
        return False

# View for accepting/rejecting a completion
@login_required
def completionAcceptView(request,pk,status):

    if not request.user.profile.verified:
        messages.error(request,"You are unverified! Please verify to access the Bounty board!")
        return redirect("bounty-about")

    # Only the Bounty originator can close out completions
    if not Completion.objects.get(pk=pk).bounty.author == request.user:
        return redirect("bounty-about")
    
    completion = Completion.objects.get(pk=pk)

    if status == "ACCEPTED":
        bounty = completion.bounty
        bounty.is_completed = True
        bounty.save()

        for comp in Completion.objects.filter(bounty=bounty):
            comp.is_completed = "REJECTED"
            comp.save()

        completion.is_completed = status
        completion.save()

        # Create message
        url = BASE_URL + reverse("completion-detail",args=[pk])
        m = Message(user=completion.author,text=f"{request.user.profile.discordname} accepted your completion: {url}")
        m.save()

        return redirect("bounty-detail",completion.bounty.pk)

    return redirect("rejection-reason",completion.pk)

@login_required
def rejectionReasonView(request,pk):

    completion = Completion.objects.get(pk=pk)

    if not request.user.profile.verified:
        messages.error(request,"You are unverified! Please verify to access the Bounty board!")
        return redirect("bounty-about")

    # Only the Bounty originator can close out completions
    if not completion.bounty.author == request.user:
        return redirect("bounty-about")

    if request.method == "POST":

        form = TextForm(request.POST)
        if form.is_valid():
            completion.rejection_reason = form.cleaned_data.get("text")
            completion.save()

        return redirect("bounty-detail",completion.bounty.pk)

    form = TextForm()
    return render(request, 'bounty/rejection_reason.html',{'form': form})

@login_required
def bountyAcceptView(request,pk):

    if not request.user.profile.verified:
        messages.error(request,"You are unverified! Please verify to access the Bounty board!")
        return redirect("bounty-about")

    # can only accept bounties on the same team
    if not Bounty.objects.get(pk=pk).team == request.user.profile.team:
        return redirect("bounty-about")

    if len(Acceptance.objects.filter(user=request.user).filter(bounty=pk)) > 0:
            messages.error(request,"You have already accepted this bounty!")
            return redirect("bounty-detail",pk)

    bounty = Bounty.objects.get(pk=pk)
    user = request.user

    acceptance = Acceptance(bounty=bounty,user=user)
    acceptance.save()

    # Create message
    url = BASE_URL + reverse("bounty-detail",args=[pk])
    m = Message(user=bounty.author,text=f"{user.profile.discordname} accepted your bounty: {url}")
    m.save()

    return redirect("bounty-detail",pk)

# get all current messages
def getMessages(request):

    # CHECK HEADERS
    if "secret" in request.headers and request.headers["secret"] == os.environ.get("MESSAGE_KEY"):

        # GET ALL MESSAGES FROM DB AND FORMAT INTO MESSAGES
        all_messages = Message.objects.all()

        message_dict = {}

        for message in all_messages.iterator():
            discordid = message.user.profile.discordid
            
            if message.user.profile.discordmessage:

                if discordid in message_dict:
                    message_dict[discordid] += "\n" + message.text
                else:
                    message_dict[discordid] = message.text

        channel_messages = BountyNotification.objects.all()

        channel_dict = {}

        for message in channel_messages.iterator():
            discordid = message.channel.discordid
            
            if discordid in channel_dict:
                channel_dict[discordid] += "\n" + message.text
            else:
                channel_dict[discordid] = message.text

        # RETURN MESSAGES
        data = { 
            "messages" : message_dict,
            "channel_messages" : channel_dict }

        all_messages.delete()
        channel_messages.delete()

        return JsonResponse(data=data)

    return redirect("bounty-detail")

# get all current messages
def getVerified(request):

    # CHECK HEADERS
    if "secret" in request.headers and request.headers["secret"] == os.environ.get("MESSAGE_KEY"):

        # GET ALL VERIFIED USERS
        p = Profile.objects.filter(verified=True)

        profiles = [profile.discordname for profile in p.iterator()]

        # RETURN MESSAGES
        data = { "verifiedUsers" : profiles }

        return JsonResponse(data=data)

    return redirect("bounty-detail")

# get all current messages
def getVisits(request):

    # CHECK HEADERS
    if "secret" in request.headers and request.headers["secret"] == os.environ.get("MESSAGE_KEY"):

        # GET ALL VERIFIED USERS
        visits = DailyVisit.objects.all()

        history = [str(visit) for visit in visits.iterator()]

        # RETURN MESSAGES
        data = { "visitHistory" : history }

        return JsonResponse(data=data)

    return redirect("bounty-detail")