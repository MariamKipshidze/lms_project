from django.db.models import Sum, Q

from .models import StudentProfile, Subject, LecturerProfile, Faculty, ChosenSubject
from .permissions import IsOwnerOrReadOnly, IsLecturer, IsStudent, IsFacultyLecturerOrReadOnly
from .serializers import StudentProfileSerializer, LecturerProfileSerializer
from .serializers import SubjectSerializer, FacultySerializer, ChosenSubjectSerializer

from rest_framework import generics, permissions
from rest_framework import viewsets
from rest_framework.filters import SearchFilter


class StudentChosenSubjectViewSets(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChosenSubjectSerializer

    def get_queryset(self):
        student = self.request.user.student_profile
        return ChosenSubject.objects.filter(student=student)

    def perform_update(self, serializer):
        instance = serializer.save()
        current_score = instance.current_score

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
        else:
            instance.passed = True
            instance.grades = 6


class StudentFacultySubjectList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    serializer_class = SubjectSerializer

    def get_queryset(self):
        faculty = self.request.user.student_profile.faculty
        return Subject.objects.filter(faculty=faculty)


class LecturerProfileList(generics.ListAPIView):
    queryset = LecturerProfile.objects.all()
    serializer_class = LecturerProfileSerializer
    filter_backends = [SearchFilter]
    search_fields = ["first_name", "last_name"]


class StudentViewSets(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly, IsLecturer]
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    filter_backends = [SearchFilter]
    search_fields = ['personal_id']

    def get_queryset(self):
        return StudentProfile.objects.annotate(
            total_credits=Sum('subject__subject__credit_score', filter=Q(subject__passed=True))
        )


class SubjectViewSets(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class FacultyViewSets(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsFacultyLecturerOrReadOnly]
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
