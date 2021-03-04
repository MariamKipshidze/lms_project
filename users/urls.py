from django.urls import path
from users import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "users"

urlpatterns = [
    path('users/', views.UserViewSet.as_view({'get': 'list'})),
    path('users/<int:pk>/', views.UserViewSet.as_view({'get': 'retrieve'})),
    path('users/update/<int:pk>/', views.UserViewSet.as_view({'post': 'update', 'get': 'retrieve'})),
    path('register/', views.user_registration),
]

urlpatterns = format_suffix_patterns(urlpatterns)
