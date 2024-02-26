from rest_framework.decorators import api_view
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        return Response({ "user": serializer.data })
    return Response(serializer.error, status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("user not found", status=status.HTTP_404_NOT_FOUND)
    serilizer = UserSerializer(user)
    return Response({ "user": serilizer.data })
