from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'website', 'location')
    search_fields = ('user__email', 'user__username')

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)




