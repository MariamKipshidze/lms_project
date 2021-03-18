from django.core.validators import RegexValidator
from django.db import transaction
from rest_framework import serializers
from lms_app.models import StudentProfile, LecturerProfile, Subject, Faculty, ChosenSubject, Campus
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
        fields = ["name", "description", "price"]


class CampusSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(many=True)

    class Meta:
        model = Campus
        fields = ["location", "faculty"]

    def create(self, validated_data):
        with transaction.atomic():
            faculties = validated_data.pop('faculty')
            campus = Campus.objects.create(**validated_data)
            # faculty_list = []
            # for faculty in faculties:
            #     faculty_list.append(Faculty.objects.create(**faculty))
            faculty = [Faculty(**faculty) for faculty in faculties]
            faculty_list = Faculty.objects.bulk_create(faculty)
            campus.faculty.set(faculty_list)
        return campus


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
        with transaction.atomic():
            user_data = validated_data.pop('user')
            user = user_registration_fun(data=user_data)
            student = StudentProfile.objects.create(user=user, **validated_data)
        return student


class LecturerProfileSerializer(DynamicFieldsModelSerializer):
    user = RegistrationSerializer()
    personal_id = serializers.CharField(validators=[RegexValidator(r'^[0-9]{11}',
                                        message='Personal ID must be 11 digits')])

    # def to_representation(self, instance):
    #     return instance.email

    class Meta:
        model = LecturerProfile
        fields = ["user", "faculty", "first_name", "last_name", "personal_id", "mobile_number", "salary"]

    def create(self, validated_data):
        with transaction.atomic():
            user_data = validated_data.pop('user')
            user = user_registration_fun(data=user_data)
            lecturer = LecturerProfile.objects.create(user=user, **validated_data)
        return lecturer


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["name", "faculty", "credit_score", "lecturer", "syllabus"]


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


class CampusOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
