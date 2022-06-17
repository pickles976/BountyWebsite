from django.urls import path
from .views import ImageView,UserView,BountyView,CompletionView,BountySearchView,AllBountiesView
urlpatterns = [
    path("image", ImageView.as_view()),
    path("user", UserView.as_view()),
    path("bounty", BountyView.as_view()),
    path("bounty_list", AllBountiesView.as_view()),
    path("completion", CompletionView.as_view()),
    path("bounty_search",BountySearchView.as_view())
]