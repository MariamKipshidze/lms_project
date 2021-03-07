from django.db.models import Sum, Q

from .models import StudentProfile, Subject, LecturerProfile, Faculty, ChosenSubject
from .permissions import IsOwnerOrReadOnly, IsLecturer, IsStudent, IsFacultyLecturerOrReadOnly
from .serializers import StudentProfileSerializer, LecturerProfileSerializer
from .serializers import SubjectSerializer, FacultySerializer, ChosenSubjectSerializer

from rest_framework import generics, permissions
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response


class StudentChosenSubjectViewSets(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    serializer_class = ChosenSubjectSerializer

    def get_queryset(self):
        student = self.request.user.student_profile
        return ChosenSubject.objects.filter(student=student)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        current_score = serializer.validated_data["current_score"]
        if current_score > 90:
            serializer.validated_data["passed"] = True
            serializer.validated_data["grades"] = 1
        elif current_score > 80:
            serializer.validated_data["passed"] = True
            serializer.validated_data["grades"] = 2
        elif current_score > 70:
            serializer.validated_data["passed"] = True
            serializer.validated_data["grades"] = 3
        elif current_score > 60:
            serializer.validated_data["passed"] = True
            serializer.validated_data["grades"] = 4
        elif current_score > 50:
            serializer.validated_data["passed"] = True
            serializer.validated_data["grades"] = 5
        else:
            serializer.validated_data["passed"] = False
            serializer.validated_data["grades"] = 6

        self.perform_update(serializer)
        return Response(serializer.data)


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
