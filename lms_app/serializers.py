from rest_framework import serializers
from .models import StudentProfile, LecturerProfile, Subject, Faculty, ChosenSubject
from users.serializers import UserSerializer


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
    user = UserSerializer()
    total_credits = serializers.IntegerField()

    class Meta:
        model = StudentProfile
        fields = ["user", "faculty", "first_name", "last_name", "gpa", 
                  "image", "mobile_number", "personal_id", "total_credits"]


class LecturerProfileSerializer(serializers.ModelSerializer):
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
        fields = ["student", "subject", "current_score"]


class CreateChosenSubjectSerializer(serializers.ModelSerializer):
    # def __init__(self, faculty, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['subject'].queryset = self.fields['subject'].queryset.filter(faculty=faculty)

    class Meta:
        model = ChosenSubject
        fields = ["subject"]


class ChosenSubjectSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()

    class Meta:
        model = ChosenSubject
        fields = ["student", "subject", "current_score", "passed", "grades"]
