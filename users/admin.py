from django.contrib import admin
from .models import User, StudentProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(StudentProfile)
class StudentProfileModelAdmin(admin.ModelAdmin):
    search_fields = ("user",)
    list_display = ["user", ]

class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'fields': ('email', 'username', 'status', 'password1', 'password2',)
        }),
        ('Permissions', {
            'fields': ('status',)
        })
    )
    fieldsets = (
        (None, {
            'fields': ('email', 'password',)
        }),
        ('Permissions', {
            'fields': ("status",)
        })
    )
    list_display = [ 'username', 'status',]
    search_fields = ( 'username',)

admin.site.register(User, UserAdmin)