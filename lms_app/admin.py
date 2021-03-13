from django.contrib import admin
from lms_app.models import StudentProfile, LecturerProfile, Subject, Faculty, ChosenSubject


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "first_name", "last_name", "gpa", "faculty"]


@admin.register(LecturerProfile)
class LecturerProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "first_name", "last_name", "faculty"]


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "faculty", "credit_score", "syllabus"]


@admin.register(ChosenSubject)
class ChosenSubjectAdmin(admin.ModelAdmin):
    list_display = ["id", "student", "subject", "current_score", "passed", "grades"]
