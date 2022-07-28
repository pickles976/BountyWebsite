from django.contrib import admin
from django.urls import path
from .views import ( BountyListView, 
                        BountyDetailView, 
                        UserBountyListView, 
                        BountyUpdateView, 
                        BountyDeleteView, 
                        CompletionDetailView,
                        CompletionDeleteView,
                        postBountyView,
                        postCompletionView,
                        bountyAcceptView )
from . import views

urlpatterns = [
    path('', BountyListView.as_view(),name="bounty-home"),
    path('<str:status>/', BountyListView.as_view(),name="bounty-home"),
    path("about", views.about, name="bounty-about"),
    path('user/<str:username>/', UserBountyListView.as_view(),name="user-bounties"),
    path("bounty/new/", postBountyView,name="bounty-create"),
    path("bounty/<int:pk>/", BountyDetailView.as_view(),name="bounty-detail"),
    path("bounty/<int:pk>/update/", BountyUpdateView.as_view(),name="bounty-update"),
    path("bounty/<int:pk>/delete/", BountyDeleteView.as_view(),name="bounty-delete"),
    path("completion/new/<int:bounty>/", postCompletionView,name="completion-create"),
    path("completion/<int:pk>/", CompletionDetailView.as_view(),name="completion-detail"),
    path("delete/completion/<int:pk>", CompletionDeleteView.as_view(),name="completion-delete"),
    path("completion/<int:pk>/<str:status>/", views.completionAcceptView,name="completion-accept"),
    path("reject/<int:pk>/", views.rejectionReasonView,name="rejection-reason"),
    path("accept/<int:pk>/", bountyAcceptView,name="bounty-accept"),
]