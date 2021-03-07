from rest_framework import serializers
from .models import StudentProfile, LecturerProfile, Subject, Faculty
from users.serializers import UserSerializer

    
class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    total_credits = serializers.IntegerField()

    class Meta:
        model = StudentProfile
        fields = ["user", "faculty", "first_name", "last_name", "gpa", 
                  "image", "mobile_number", "personal_id", "total_credits"]


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ["name", "student"]


class LecturerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturerProfile
        fields = ["user", "faculty", "first_name", "last_name", "mobile_number", "personal_id"]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["name", "faculty", "credit_score", "lecturer"]
        depth = 2
