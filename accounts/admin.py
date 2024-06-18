from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'date_joined', 'pfp_thumbnail')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'pfp')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    readonly_fields = ('created_at',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

    def pfp_thumbnail(self, obj):
        if obj.pfp:
            return format_html('<a href= "{}" target="_blank"><img src="{}" width="30" height="30"/></a>', obj.pfp.url,obj.pfp.url)
        return ""
    pfp_thumbnail.short_description = 'Profile Picture'

    def date_joined(self, obj):
        return obj.created_at
    date_joined.short_description = 'Date Joined'
    date_joined.admin_order_field = 'created_at'

admin.site.register(CustomUser, CustomUserAdmin)