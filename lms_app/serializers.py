from django.core.validators import RegexValidator
from django.db import transaction
from django.db.models import Sum, Q, ExpressionWrapper, DecimalField, F
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


class CampusOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class StudentProfileSerializer(DynamicFieldsModelSerializer):
    user = RegistrationSerializer()
    total_credits = serializers.IntegerField()
    personal_id = serializers.CharField(validators=[RegexValidator(r'^[0-9]{11}',
                                        message='Personal ID must be 11 digits')])
    subject_count = serializers.SerializerMethodField("get_subject_count")

    class Meta:
        model = StudentProfile
        fields = ["user", "faculty", "first_name", "last_name", "gpa",
                  "image", "mobile_number", "personal_id", "total_credits", "subject_count"]

    @staticmethod
    def get_subject_count(obj):
        return obj.subject.count()

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
    faculty = serializers.StringRelatedField()
    lecturer = serializers.StringRelatedField(many=True)

    class Meta:
        model = Subject
        fields = ["name", "faculty", "credit_score", "lecturer", "syllabus"]


class UpdateChosenSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChosenSubject
        fields = ["current_score"]

    def update(self, instance, validated_data):
        current_score = validated_data["current_score"]
        instance.current_score = current_score
        instance.passed = False
        instance.grades = 6

        if current_score > 90:
            instance.passed = True
            instance.grades = 1
        elif current_score > 80:
            instance.passed = True
            instance.grades = 2
        elif current_score > 70:
            instance.passed = True
            instance.grades = 3
        elif current_score > 60:
            instance.passed = True
            instance.grades = 4
        elif current_score > 50:
            instance.passed = True
            instance.grades = 5

        instance.save()

        processed_points = ExpressionWrapper(
            (F('current_score') - 50) * F("subject__credit_score"),
            output_field=DecimalField())

        gpa_info = ChosenSubject.objects.filter(Q(passed=True), Q(student=instance.student)) \
            .annotate(points=processed_points) \
            .aggregate(
            gpa=Sum('points'),
            score_sum=Sum("subject__credit_score"),
        )

        student = instance.student
        if gpa_info["score_sum"]:
            student.gpa = ((gpa_info["gpa"]) / gpa_info["score_sum"]) * 4 / 50
        student.save()
        return instance


class CreateChosenSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChosenSubject
        fields = ["subject"]


class ChosenSubjectSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()

    class Meta:
        model = ChosenSubject
        fields = ["student", "subject", "current_score", "passed", "grades"]
