from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, InvitationKey, Profile
from .forms import CustomUserCreationForm
# Register your models here.

admin.site.register(InvitationKey)
admin.site.register(Profile)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    # Fields to display in the list view
    list_display = ('username', 'email', 'firstname',
                    'lastname', 'role', 'is_staff', 'is_active')
    # Fields to filter by in the right sidebar
    list_filter = ('role', 'is_staff', 'is_active')
    # Fields to search by
    search_fields = ('username', 'email', 'firstname', 'lastname')
    # Fields to display in the detail view
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('firstname', 'lastname',
         'email', 'phonenumber', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_staff',
         'is_active', 'groups', 'user_permissions')}),
        ('Role Info', {'fields': ('role',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # Fields to display when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'firstname', 'lastname', 'email', 'phonenumber', 'invitation_key', 'date_of_birth', 'role', 'is_staff', 'is_active')}
         ),
    )
    # Fields to prepopulate in the add form
    prepopulated_fields = {'email': ('firstname', 'lastname',)}


# Register the custom user admin class
admin.site.register(CustomUser, CustomUserAdmin)
