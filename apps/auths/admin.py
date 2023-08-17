from django.contrib import admin
from auths.models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('login', 'first_name','created_at', 'is_active', 'is_staff', 'chat_id')
    list_filter = ('is_active', 'is_staff', 'created_at')
    search_fields = ('login', 'first_name', 'chat_id')
    ordering = ('-created_at',)
    fieldsets = (
        ('User Information', {'fields': ('login', 'first_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    readonly_fields = ('created_at',)
