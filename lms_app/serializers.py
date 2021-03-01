from rest_framework import serializers
from .models import StudentProfile, LecturerProfile, Subject, Faculty
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "status", "student_profile", "lecturer_profile"]

    
class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ["user", "faculty", "first_name", "last_name", "gpa", 
        "image", "mobile_number", "subject", "personal_id"]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["name", "faculty", "credit_score", "lecturer", "student_subject"]


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ["name", "student"]


class LecturerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturerProfile
        fields = ["user", "faculty", "first_name", "last_name", "mobile_number", "personal_id"]
