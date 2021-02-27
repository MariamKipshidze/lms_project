from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import StudentProfile
from .serializers import StudentProfileSerializer


@csrf_exempt
def student_profile_list(request):
    if request.method == 'GET':
        student_profile = StudentProfile.objects.all()
        serializer = StudentProfileSerializer(student_profile, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = StudentProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
