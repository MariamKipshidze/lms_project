from .models import StudentProfile
from users.models import User
from .permissions import IsOwnerOrReadOnly

from .serializers import StudentProfileSerializer, UserSerializer
from rest_framework import generics
from rest_framework import permissions


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class StudentList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    