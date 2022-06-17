from rest_framework import serializers
from .models import Image, User, Bounty, Completion

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image # model to serialize
        fields = "__all__" # fields to serialize

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class BountySerializer(serializers.ModelSerializer):
    class Meta:
        model = Bounty
        fields = "__all__"

class CompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Completion
        fields = "__all__"

