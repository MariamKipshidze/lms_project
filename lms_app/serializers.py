from django.core.validators import RegexValidator
from rest_framework import serializers
from .models import StudentProfile, LecturerProfile, Subject, Faculty, ChosenSubject
from users.views import user_registration_fun
from users.serializers import RegistrationSerializer


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ["name", "student"]

    
class StudentProfileSerializer(DynamicFieldsModelSerializer):
    user = RegistrationSerializer()
    total_credits = serializers.IntegerField()
    personal_id = serializers.CharField(validators=[RegexValidator(r'^[0-9]{11}',
                                        message='Personal ID must be 11 digits')])

    class Meta:
        model = StudentProfile
        fields = ["user", "faculty", "first_name", "last_name", "gpa",
                  "image", "mobile_number", "personal_id", "total_credits"]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = user_registration_fun(data=user_data)
        student = StudentProfile.objects.create(user=user, **validated_data)
        return student


class LecturerProfileSerializer(DynamicFieldsModelSerializer):
    user = RegistrationSerializer()
    personal_id = serializers.CharField(validators=[RegexValidator(r'^[0-9]{11}',
                                        message='Personal ID must be 11 digits')])

    class Meta:
        model = LecturerProfile
        fields = ["user", "faculty", "first_name", "last_name", "mobile_number", "personal_id"]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["name", "faculty", "credit_score", "lecturer"]


class UpdateChosenSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChosenSubject
        fields = ["current_score"]


class CreateChosenSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChosenSubject
        fields = ["subject"]


class ChosenSubjectSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()

    class Meta:
        model = ChosenSubject
        fields = ["student", "subject", "current_score", "passed", "grades"]
