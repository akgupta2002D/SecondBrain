from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, InvitationKey, Profile
from .forms import CustomUserCreationForm


admin.site.register(InvitationKey)
admin.site.register(Profile)


class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the CustomUser model.

    Attributes:
        add_form (CustomUserCreationForm): The form used to create new users.
        model (CustomUser): The model registered with this admin.
        list_display (tuple): Fields to display in the list view.
        list_filter (tuple): Fields to filter by in the right sidebar.
        search_fields (tuple): Fields to search by.
        fieldsets (tuple): Fields to display in the detail view.
        add_fieldsets (tuple): Fields to display when adding a new user.
        prepopulated_fields (dict): Fields to prepopulate in the add form.
    """
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ('username', 'email', 'firstname',
                    'lastname', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'firstname', 'lastname')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('firstname', 'lastname',
                                      'email', 'phonenumber', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_staff',
                                    'is_active', 'groups', 'user_permissions')}),
        ('Role Info', {'fields': ('role',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'firstname', 'lastname', 'email', 'phonenumber', 'invitation_key', 'date_of_birth', 'role', 'is_staff', 'is_active')}
         ),
    )
    prepopulated_fields = {'email': ('firstname', 'lastname',)}


# Register the custom user admin class
admin.site.register(CustomUser, CustomUserAdmin)
"""
Admin configuration for the custom_auth app.

This module registers the models and configures the admin interface for the `custom_auth` app.
"""
