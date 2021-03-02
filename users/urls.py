from django.urls import path
from users import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "users"

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('user/<int:pk>/', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)


path('users/', views.UserList.as_view()),
path('user/<int:pk>/', views.UserDetail.as_view()),