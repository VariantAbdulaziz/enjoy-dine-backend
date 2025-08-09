from django.contrib import admin
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'email')
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff')
