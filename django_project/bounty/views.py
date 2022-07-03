from django.shortcuts import render, get_object_or_404, redirect
from .models import Bounty, Completion, Images
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import modelformset_factory
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import ImageForm, BountyForm, CompletionForm, TextForm
from django.db.models import Subquery, OuterRef

def about(request):
    return render(request,"bounty/about.html",{"title": "About"})

# List view of Bounties
class BountyListView(ListView):
    model = Bounty
    template_name = "bounty/home.html" # <app>/<model>_<viewtype>.html
    context_object_name = "bounties"
    ordering = ["-date_posted"]
    paginate_by = 10

    def get_queryset(self):

        status = self.kwargs.get("status")

        if status == "open":
            return Bounty.objects.filter(is_completed=False).prefetch_related("images_set").order_by("-date_posted")
        elif status == "closed":
            return Bounty.objects.filter(is_completed=True).prefetch_related("images_set").order_by("-date_posted")
        else:
            return Bounty.objects.all().prefetch_related("images_set").order_by("-date_posted")

# List view of bounties for currently authenticated user
class UserBountyListView(ListView):
    model = Bounty
    template_name = "bounty/user_bounties.html" # <app>/<model>_<viewtype>.html
    context_object_name = "bounties"
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get("username"))
        return Bounty.objects.filter(author=user).order_by("-date_posted")

# view for creating bounties
@login_required
def postBountyView(request):
 
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
            post_form.save()
    
            for form in formset.cleaned_data:
                #this helps to not crash if the user   
                #do not upload all the photos
                if form:
                    image = form['image']
                    photo = Images(bounty=post_form, image=image)
                    photo.save()

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
class BountyDetailView(DetailView):
    model = Bounty

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['completions'] = Completion.objects.filter(bounty=self.object)
        return context

#
class BountyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Bounty
    fields = ["title", "description", "image"]

    def form_valid(self,form):
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
        bounty = self.get_object()
        if self.request.user == bounty.author:
            return True
        return False

# view for creating completions
@login_required
def postCompletionView(request,bounty):
 
    ImageFormSet = modelformset_factory(Images,
                                        form=ImageForm, extra=4)
    #'extra' means the number of photos that you can upload   ^
    if request.method == 'POST':

        if len(Completion.objects.filter(author=request.user,bounty=bounty)) > 0:
            messages.error(request,"You have already created a completion for this bounty!")
            return redirect("bounty-detail",bounty)
    
        completionForm = CompletionForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Images.objects.none())
    
    
        if completionForm.is_valid() and formset.is_valid():
            post_form = completionForm.save(commit=False)
            post_form.author = request.user
            post_form.bounty = Bounty.objects.get(pk=bounty)
            post_form.save()
    
            for form in formset.cleaned_data:
                #this helps to not crash if the user   
                #do not upload all the photos
                if form:
                    image = form['image']
                    photo = Images(completion=post_form, image=image)
                    photo.save()

            # use django messages framework
            messages.success(request,"Completion created successfully")
            return redirect("completion-detail",post_form.pk)
        else:
            print(completionForm.errors, formset.errors)
    else:
        completionForm = CompletionForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'bounty/post_completion_form.html',{'completionForm': completionForm, 'formset': formset})


class CompletionDetailView(DetailView):
    model = Completion

class CompletionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Completion
    success_url = "/"

    def test_func(self):
        completion = self.get_object()
        if self.request.user == completion.author:
            return True
        return False

# View for accepting/rejecting a completion
def completionAcceptView(request,pk,status):
    
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

        return redirect("bounty-detail",completion.bounty.pk)

    return redirect("rejection-reason",completion.pk)

def rejectionReasonView(request,pk):

    completion = Completion.objects.get(pk=pk)

    if request.method == "POST":

        form = TextForm(request.POST)
        if form.is_valid():
            completion.rejection_reason = form.cleaned_data.get("text")
            completion.save()

        return redirect("bounty-detail",completion.bounty.pk)

    form = TextForm()
    return render(request, 'bounty/rejection_reason.html',{'form': form})
