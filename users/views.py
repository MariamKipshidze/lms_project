from django.db import transaction

from .serializers import UserSerializer, RegistrationSerializer
from .models import User
from .permissions import IsOwner
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets, generics
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter, OrderingFilter


@api_view(['POST'])
def user_registration(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if request.method == "POST":
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save()
                data['response'] = "Successfully registered"
                token = Token.objects.create(user=user).key
                data['token'] = token
        else:
            data = serializer.errors
    return Response(data)


def user_registration_fun(data):
    serializer = RegistrationSerializer(data=data)
    if serializer.is_valid():
        with transaction.atomic():
            user = serializer.save()
            var = Token.objects.create(user=user).key
    return user


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['email']


class LecturerUserList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.filter(status=1)
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', "last_name"]


class StudentUserList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.filter(status=2)
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name']
    pagination_class = []
