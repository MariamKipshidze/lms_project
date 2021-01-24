from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# @admin.register(User)
# class UserModelAdmin(admin.ModelAdmin):
#     list_display = ["username", "status",]

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