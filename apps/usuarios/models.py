from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado con campos adicionales para seguridad
    """
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(_('phone number'), max_length=15, blank=True)
    is_email_verified = models.BooleanField(_('email verified'), default=False)
    is_2fa_enabled = models.BooleanField(_('2FA enabled'), default=False)
    failed_login_attempts = models.PositiveSmallIntegerField(_('failed login attempts'), default=0)
    last_login_ip = models.GenericIPAddressField(_('last login IP'), blank=True, null=True)
    last_login_user_agent = models.TextField(_('last login user agent'), blank=True)
    
    # Si un usuario está temporalmente bloqueado
    is_locked = models.BooleanField(_('account locked'), default=False)
    lock_expiration = models.DateTimeField(_('lock expiration'), blank=True, null=True)
    
    # Campo para almacenar la clave secreta de 2FA (estará encriptada)
    totp_secret = models.CharField(_('TOTP secret'), max_length=255, blank=True)
    
    # Registro de actividad del usuario
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    # Campos adicionales para control de acceso
    last_password_change = models.DateTimeField(_('last password change'), blank=True, null=True)
    require_password_change = models.BooleanField(_('require password change'), default=False)
    
    # Campo para forzar cierre de sesión en todos los dispositivos
    session_security_hash = models.CharField(_('session security hash'), max_length=64, blank=True)
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        permissions = [
            ('can_reset_2fa', _('Can reset 2FA for users')),
            ('can_unlock_accounts', _('Can unlock locked user accounts')),
            ('can_view_user_logs', _('Can view user activity logs')),
            ('can_export_user_data', _('Can export user data')),
        ]

    def __str__(self):
        return self.email


class UserRole(models.Model):
    """
    Modelo para roles dinámicos con jerarquía
    """
    name = models.CharField(_('role name'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True)
    permissions = models.ManyToManyField(
        Permission, 
        verbose_name=_('permissions'),
        blank=True,
    )
    parent_role = models.ForeignKey(
        'self',
        verbose_name=_('parent role'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='child_roles'
    )
    priority = models.PositiveSmallIntegerField(_('priority'), default=0)
    is_system_role = models.BooleanField(_('system role'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('user role')
        verbose_name_plural = _('user roles')
        ordering = ['priority']
    
    def __str__(self):
        return self.name
    
    def get_all_permissions(self):
        """
        Obtiene todos los permisos, incluyendo los heredados de roles padres
        """
        all_permissions = set(self.permissions.all())
        
        # Obtener permisos de roles padres recursivamente
        if self.parent_role:
            parent_permissions = self.parent_role.get_all_permissions()
            all_permissions.update(parent_permissions)
            
        return all_permissions


class UserRoleAssignment(models.Model):
    """
    Asignación de roles a usuarios
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='role_assignments'
    )
    role = models.ForeignKey(
        UserRole,
        on_delete=models.CASCADE,
        related_name='user_assignments'
    )
    assigned_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='role_assignments_given'
    )
    assigned_at = models.DateTimeField(_('assigned at'), auto_now_add=True)
    expires_at = models.DateTimeField(_('expires at'), null=True, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    
    class Meta:
        verbose_name = _('role assignment')
        verbose_name_plural = _('role assignments')
        unique_together = ('user', 'role')
    
    def __str__(self):
        return f"{self.user.username} - {self.role.name}"