from django.urls import path
from users import views

app_name = "users"

urlpatterns = [
    path('users/', views.UserViewSet.as_view({'get': 'list'})),
    path('users/<int:pk>/', views.UserViewSet.as_view({'get': 'retrieve'})),
    path('users/update/<int:pk>/', views.UserViewSet.as_view({'post': 'update', 'get': 'retrieve'})),
    path('register/', views.user_registration),
    path('lecturer/user/', views.LecturerUserList.as_view()),
    path('student/user/', views.StudentUserList.as_view()),
    path('user/detail/<int:pk>/', views.UserDetail.as_view()),
]
