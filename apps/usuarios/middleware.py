from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone

class SecurityMiddleware:
    """
    Middleware para verificar aspectos de seguridad en cada solicitud
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Si el usuario está autenticado, realizar verificaciones de seguridad
        if request.user.is_authenticated:
            user = request.user
            
            # Verificar si la cuenta está bloqueada
            if user.is_locked:
                # Si el bloqueo ha expirado, desbloquear
                if user.lock_expiration and timezone.now() > user.lock_expiration:
                    user.is_locked = False
                    user.lock_expiration = None
                    user.failed_login_attempts = 0
                    user.save(update_fields=['is_locked', 'lock_expiration', 'failed_login_attempts'])
                else:
                    # Si sigue bloqueada, cerrar sesión
                    logout(request)
                    return redirect(reverse('account_login'))
            
            # Verificar si se requiere cambio de contraseña
            if user.require_password_change:
                # Permitir acceso solo a la página de cambio de contraseña
                if not request.path == reverse('account_change_password'):
                    return redirect(reverse('account_change_password'))
            
            # Verificar si la sesión tiene el hash de seguridad correcto
            session_hash = request.session.get('security_hash')
            if session_hash != user.session_security_hash:
                # Hash no coincide, posible sesión inválida
                logout(request)
                return redirect(reverse('account_login'))
                
            # Actualizar last_activity en la sesión
            request.session['last_activity'] = timezone.now().isoformat()
            
        response = self.get_response(request)
        return response

class InactivitySessionMiddleware:
    """
    Middleware para verificar la inactividad de la sesión
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            
            if last_activity:
                # Convertir a objeto datetime
                last_activity = timezone.datetime.fromisoformat(last_activity)
                
                # Verificar tiempo de inactividad
                inactivity_period = timezone.now() - last_activity
                max_inactivity = timezone.timedelta(minutes=settings.SESSION_IDLE_TIMEOUT)
                
                if inactivity_period > max_inactivity:
                    # Sesión inactiva, cerrar sesión
                    logout(request)
                    return redirect(reverse('account_login'))
            
            # Actualizar timestamp de última actividad
            request.session['last_activity'] = timezone.now().isoformat()
            
        response = self.get_response(request)
        return response