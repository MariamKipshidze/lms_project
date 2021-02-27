from .models import StudentProfile
from .serializers import StudentProfileSerializer
from rest_framework import mixins
from rest_framework import generics


class StudentList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class StudentDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    