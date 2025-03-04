# apps/usuarios/signals.py
from django.contrib.auth import user_logged_in, user_login_failed
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import CustomUser


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    """
    Callback para cuando un usuario inicia sesión exitosamente.
    Resetea los intentos fallidos y registra la IP.
    """
    # Resetear los intentos fallidos
    user.failed_login_attempts = 0
    user.locked_until = None
    
    # Guardar la IP de inicio de sesión
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        user.last_login_ip = ip
    
    user.save(update_fields=['failed_login_attempts', 'locked_until', 'last_login_ip'])


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, request, **kwargs):
    """
    Callback para cuando falla un intento de inicio de sesión.
    Incrementa el contador de intentos fallidos y potencialmente bloquea la cuenta.
    """
    email = credentials.get('username', '').split()
    try:
        user = CustomUser.objects.get(email=email)
        user.failed_login_attempts += 1
        
        # Si hay 5 o más intentos fallidos, bloqueamos la cuenta por 5 minutos
        if user.failed_login_attempts >= 5:
            user.locked_until = timezone.now() + timezone.timedelta(minutes=5)
        
        user.save(update_fields=['failed_login_attempts', 'locked_until'])
    except CustomUser.DoesNotExist:
        # No revelar si el usuario existe o no
        pass


@receiver(post_save, sender=CustomUser)
def user_post_save(sender, instance, created, **kwargs):
    """
    Callback para después de guardar un usuario.
    """
    if created:
        # Lógica para usuarios recién creados
        pass