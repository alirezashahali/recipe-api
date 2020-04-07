from django.shortcuts import render
from users.serializers import UserSerializer, AuthTokenSerializer
from rest_framework import generics

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
# Create your views here.

class CreateUserView(generics.CreateAPIView):
    """create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """create new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES