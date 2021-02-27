from django.urls import path
from student_app import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('student/profile/', views.student_profile_list),
    path('student/profile/<int:pk>/', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)