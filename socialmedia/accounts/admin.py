from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # Import UserAdmin here
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Define the fields to display in the admin list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'bio', 'profile_pic', 'is_staff', 'is_active')
    
    # Define the fields to display in the form for creating/editing a user
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'bio', 'profile_pic')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Define the fields to be included in the add user form
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'bio', 'profile_pic')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )

    # Add search functionality by username or email
    search_fields = ('username', 'email')
    
    # Add filter options for the admin list view
    list_filter = ('is_active', 'is_staff')

    # Define the form to use when creating/editing a user
    ordering = ('username',)

# Register the CustomUser model and CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)
