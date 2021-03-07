from .models import StudentProfile, Faculty, Subject, LecturerProfile
from .permissions import IsOwnerOrReadOnly, IsLecturer, IsStudent

from .serializers import StudentProfileSerializer, LecturerProfileSerializer
from .serializers import SubjectSerializer, FacultySerializer
from rest_framework import generics, permissions, status

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([permissions.IsAuthenticated, IsLecturer])
def subject_detail(request, pk):
    try:
        subject = Subject.objects.get(pk=pk)
    except Subject.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SubjectSerializer(subject, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        operation = subject.delete()
        data = {}
        if operation:
            data["success"] = "Deleted Successfully"
        else:
            data["failure"] = "Delete Failed"
        return Response(data=data)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def faculty_detail(request, pk):
    try:
        faculty = Faculty.objects.get(pk=pk)
    except Faculty.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FacultySerializer(faculty)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = FacultySerializer(faculty, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        operation = faculty.delete()
        data = {}
        if operation:
            data["success"] = "Deleted Successfully"
        else:
            data["failure"] = "Delete Failed"
        return Response(data=data)


class SubjectList(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class StudentFacultySubjectList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    serializer_class = SubjectSerializer

    def get_queryset(self):
        faculty = self.request.user.student_profile.faculty
        return Subject.objects.filter(faculty=faculty)


class FacultyList(generics.ListAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']


class LecturerProfileList(generics.ListAPIView):
    queryset = LecturerProfile.objects.all()
    serializer_class = LecturerProfileSerializer


class StudentViewSets(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
