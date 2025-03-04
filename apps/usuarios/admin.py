# apps/usuarios/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin personalizado para el modelo de usuario personalizado."""
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_totp_enabled')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number')}),
        (_('Security'), {'fields': ('totp_secret', 'last_password_change', 'failed_login_attempts', 'lock_expiration', 'last_login_ip')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )

    def is_totp_enabled(self, obj):
        """Verifica si el usuario tiene TOTP activado."""
        return bool(obj.totp_secret)  # True si tiene una clave TOTP, False si no

    is_totp_enabled.boolean = True  # Muestra un checkbox en el panel de administración
    is_totp_enabled.short_description = "TOTP Activado"  # Etiqueta en el admin
