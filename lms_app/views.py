from django.db.models import Sum, Q, ExpressionWrapper, DecimalField, F
from django.shortcuts import get_object_or_404

from lms_app.models import StudentProfile, Subject, LecturerProfile, Faculty, ChosenSubject
from lms_app.permissions import IsLecturer, IsStudent, IsFacultyLecturerOrReadOnly
from lms_app.permissions import IsLecturerOrReadOnly
from lms_app.serializers import StudentProfileSerializer, LecturerProfileSerializer
from lms_app.serializers import SubjectSerializer, FacultySerializer, UpdateChosenSubjectSerializer
from lms_app.serializers import CreateChosenSubjectSerializer, ChosenSubjectSerializer

from rest_framework import generics, permissions
from rest_framework import viewsets
from rest_framework.filters import SearchFilter


class ChosenSubjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsLecturer]
    queryset = ChosenSubject.objects.all()
    serializer_class = ChosenSubjectSerializer
    serializer_per_action = {
        "update": UpdateChosenSubjectSerializer
    }

    def get_serializer_class(self):
        return self.serializer_per_action.get(
            getattr(self, 'action', None), self.serializer_class
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        current_score = instance.current_score
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
            (F('current_score') - 50)*F("subject__credit_score"),
            output_field=DecimalField())

        gpa_info = ChosenSubject.objects.filter(Q(passed=True), Q(student=instance.student)) \
            .annotate(points=processed_points) \
            .aggregate(
            gpa=Sum('points'),
            score_sum=Sum("subject__credit_score"),
        )

        student = instance.student
        student.gpa = ((gpa_info["gpa"])/gpa_info["score_sum"]) * 4 / 50
        student.save()


class StudentChosenSubjectViewSets(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    filter_backends = [SearchFilter]
    search_fields = ['subject__name']

    def get_serializer_class(self):
        action = getattr(self, "action", None)
        if action == "create":
            return CreateChosenSubjectSerializer
        return ChosenSubjectSerializer

    def get_queryset(self):
        return ChosenSubject.objects.filter(student=self.request.user.student_profile)

    def get_object(self):
        return get_object_or_404(ChosenSubject,
                                 student=self.request.user.student_profile,
                                 id=self.kwargs["pk"])


class StudentViewSets(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    filter_backends = [SearchFilter]
    search_fields = ['personal_id']
    serializer_per_action = {
        "list": {"faculty", "first_name", "last_name", "gpa",
                 "image", "mobile_number", "personal_id", "total_credits"},
        "update": {"image", "mobile_number"},
        "create": {"user", "faculty", "first_name", "last_name",
                   "image", "mobile_number", "personal_id"}
    }

    def get_serializer(self, *args, **kwargs):
        fields = self.serializer_per_action.get(
            getattr(self, "action", None)
        )
        if fields:
            kwargs["fields"] = fields
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        return StudentProfile.objects.annotate(
            total_credits=Sum('subject__subject__credit_score',
                              filter=Q(subject__passed=True))
        )


class LecturerViewSets(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = LecturerProfile.objects.all()
    serializer_class = LecturerProfileSerializer
    filter_backends = [SearchFilter]
    search_fields = ['personal_id']

    serializer_per_action = {
        "list": {"faculty", "first_name", "last_name", "mobile_number"},
        "update": {"mobile_number"},
        "create": {"user", "faculty", "first_name", "last_name",
                   "personal_id", "salary", "mobile_number"}
    }

    def get_serializer(self, *args, **kwargs):
        fields = self.serializer_per_action.get(
            getattr(self, "action", None)
        )
        if fields:
            kwargs["fields"] = fields
        return super().get_serializer(*args, **kwargs)


class SubjectViewSets(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsLecturerOrReadOnly]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class FacultyViewSets(viewsets.ModelViewSet):
    permission_classes = [IsFacultyLecturerOrReadOnly]
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class StudentFacultySubjectList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    serializer_class = SubjectSerializer

    def get_queryset(self):
        faculty = self.request.user.student_profile.faculty
        return Subject.objects.filter(faculty=faculty)
