from django.urls import path
from users import views

app_name = "users"

urlpatterns = [
    path('users/', views.UserViewSet.as_view({'get': 'list'})),
    path('users/detail/<int:pk>/', views.UserViewSet.as_view({'get': 'retrieve', 'post': 'update'})),
    path('register/', views.user_registration),
    path('lecturer/user/', views.LecturerUserList.as_view()),
    path('student/user/', views.StudentUserList.as_view()),
]
