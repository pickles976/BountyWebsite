from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ImageSerializer, UserSerializer, BountySerializer, CompletionSerializer
from .models import Image, User, Bounty, Completion

# Create your views here.
# generics.ListAPIView
class ImageView(generics.CreateAPIView):
    queryset = Image.objects.all() # what objects to get
    serializer_class = ImageSerializer # what serializer to use

class UserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BountyView(generics.CreateAPIView):
    queryset = Bounty.objects.all()
    serializer_class = BountySerializer

class AllBountiesView(generics.ListAPIView):
    queryset = Bounty.objects.all()
    serializer_class = BountySerializer

class CompletionView(generics.CreateAPIView):
    queryset = Completion.objects.all()
    serializer_class = CompletionSerializer

# Basic Bounty Search
class BountySearchView(APIView):

    # date posted?
    # bounty amount?
    # difficulty?

    def get(self,request,format=None):
        bounties = [[bounty.description,bounty.unique_id] for bounty in Bounty.objects.filter(description=request.GET["description"],is_completed=False)]
        return Response(bounties)
    