from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from lms_app.models import StudentProfile, LecturerProfile, Subject, Faculty, ChosenSubject, Campus


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "first_name", "last_name", "gpa", "faculty"]


@admin.register(LecturerProfile)
class LecturerProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "first_name", "last_name", "faculty"]


@admin.register(Faculty)
class FacultyAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ["name", "price"]


@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ["id", "location"]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "faculty", "credit_score", "syllabus"]


@admin.register(ChosenSubject)
class ChosenSubjectAdmin(admin.ModelAdmin):
    list_display = ["id", "student", "subject", "current_score", "passed", "grades"]
