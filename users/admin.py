from django.contrib import admin
from .models import CustomUser, Profile
from django.contrib.auth.admin import UserAdmin

class CustomAdmin(UserAdmin):
    
    search_fields = ('email', 'username')
    list_filter = ('email', 'username', 'is_active', 'is_staff')
    ordering = ('-joined_on',)
    list_display = ('email', 'username', 'is_active', 'is_staff')
    
    fieldsets = (
        (None, {'fields': ('email', 'username')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff')}),
    )

admin.site.register(CustomUser, CustomAdmin)  
admin.site.register(Profile)
