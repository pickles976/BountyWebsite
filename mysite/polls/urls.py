from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("create_user/",views.create_user, name="create_user"),
    path("user/<int:unique_id>/",views.user,name="user"),
    path("create_bounty/",views.create_bounty, name="create_bounty"),
    path("bounty/<int:unique_id>/",views.bounty,name="bounty"),
    path("create_completion/",views.create_completion, name="create_completion"),
    path("completion/<int:unique_id>/",views.completion,name="completion")
]