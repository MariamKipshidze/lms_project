from .serializers import UserSerializer
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User

from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def user_registration(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "Successfully registered"
            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
