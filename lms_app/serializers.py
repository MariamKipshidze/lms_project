from rest_framework import serializers
from .models import StudentProfile
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "status"]


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StudentProfile
        fields = ["user", "first_name", "last_name", "gpa", "image"]
        