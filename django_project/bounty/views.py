from django.shortcuts import render, get_object_or_404
from .models import Bounty, Completion
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def home(request):
    context = {
        "bounties" : Bounty.objects.all()
    }
    return render(request,"bounty/home.html",context)

def about(request):
    return render(request,"bounty/about.html",{"title": "About"})

class BountyListView(ListView):
    model = Bounty
    template_name = "bounty/home.html" # <app>/<model>_<viewtype>.html
    context_object_name = "bounties"
    ordering = ["-date_posted"]
    paginate_by = 10

class UserBountyListView(ListView):
    model = Bounty
    template_name = "bounty/user_bounties.html" # <app>/<model>_<viewtype>.html
    context_object_name = "bounties"
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get("username"))
        return Bounty.objects.filter(author=user).order_by("-date_posted")

class BountyCreateView(LoginRequiredMixin, CreateView):
    model = Bounty
    fields = ["title", "description", "price", "image"]

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BountyDetailView(DetailView):
    model = Bounty

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['completions'] = Completion.objects.filter(bounty=self.object)
        return context

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
    success_url = "/bounty/"

    def test_func(self):
        bounty = self.get_object()
        if self.request.user == bounty.author:
            return True
        return False

class CompletionCreateView(LoginRequiredMixin, CreateView):

    model = Completion
    fields = ["title", "description", "image"]

    def form_valid(self,form):
        form.instance.author = self.request.user
        form.instance.bounty = Bounty.objects.get(pk=self.kwargs["bounty"])
        return super().form_valid(form)

class CompletionDetailView(DetailView):
    model = Completion

class CompletionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Completion
    success_url = "completion"

    def test_func(self):
        completion = self.get_object()
        if self.request.user == completion.author:
            return True
        return False