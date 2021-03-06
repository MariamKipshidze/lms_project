from django.db import transaction

from .serializers import UserSerializer, RegistrationSerializer
from .models import User
from .permissions import IsOwnerOrReadOnly

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets, generics
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter


@api_view(['POST'])
def user_registration(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save()
                data['response'] = "Successfully registered"
                token = Token.objects.create(user=user).key
                data['token'] = token
        else:
            data = serializer.errors
    return Response(data)


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['email']


class LecturerUserList(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.filter(status=1)
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', "last_name"]


class StudentUserList(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.filter(status=2)
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name']
    pagination_class = []


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = UserSerializer
    queryset = User.objects.filter()
