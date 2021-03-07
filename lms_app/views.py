from .models import StudentProfile, Subject, LecturerProfile, Faculty
from .permissions import IsOwnerOrReadOnly, IsLecturer, IsStudent, IsFacultyLecturerOrReadOnly

from .serializers import StudentProfileSerializer, LecturerProfileSerializer
from .serializers import SubjectSerializer, FacultySerializer
from rest_framework import generics, permissions

from rest_framework import viewsets
from rest_framework.filters import SearchFilter


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
