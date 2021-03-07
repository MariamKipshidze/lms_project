from rest_framework import permissions


class IsFacultyLecturerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.status == request.user.Status.lecturer.value:
            if request.user.lecturer_profile.faculty == obj:
                return True
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class IsLecturer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.status == request.user.Status.lecturer.value
        return False


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.status == request.user.Status.student.value
        return False
