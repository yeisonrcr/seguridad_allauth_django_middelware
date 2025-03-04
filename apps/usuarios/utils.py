from functools import wraps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse

User = get_user_model()

def has_role(user, role_name):
    """
    Verifica si un usuario tiene un rol específico
    """
    cache_key = f"user_roles_{user.id}"
    user_roles = cache.get(cache_key)
    
    if user_roles is None:
        # Si no está en caché, obtener roles de la base de datos
        user_roles = list(user.role_assignments.filter(
            is_active=True
        ).values_list('role__name', flat=True))
        
        # Guardar en caché para futuras consultas
        cache.set(cache_key, user_roles, timeout=3600)  # 1 hora
    
    return role_name in user_roles

def has_permission(user, permission_codename):
    """
    Verifica si un usuario tiene un permiso específico
    """
    # Verificar si el usuario es superusuario
    if user.is_superuser:
        return True
    
    # Primero verificar caché
    cache_key = f"user_permissions_{user.id}"
    user_permissions = cache.get(cache_key)
    
    if user_permissions is None:
        # Si no está en caché, calcular permisos
        user_permissions = set()
        
        # Obtener permisos directos del usuario
        direct_permissions = user.user_permissions.values_list('codename', flat=True)
        user_permissions.update(direct_permissions)
        
        # Obtener permisos a través de roles
        for assignment in user.role_assignments.filter(is_active=True):
            role_permissions = assignment.role.get_all_permissions()
            user_permissions.update([p.codename for p in role_permissions])
            
        # Convertir a lista para poder almacenar en caché
        user_permissions = list(user_permissions)
        
        # Guardar en caché
        cache.set(cache_key, user_permissions, timeout=3600)  # 1 hora
    
    return permission_codename in user_permissions

def role_required(role_name):
    """
    Decorador para requerir un rol específico para acceder a una vista
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(f"{reverse('account_login')}?next={request.path}")
            
            if not has_role(request.user, role_name):
                return HttpResponseForbidden("No tienes permiso para acceder a esta página")
                
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def permission_required(permission_codename):
    """
    Decorador para requerir un permiso específico para acceder a una vista
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(f"{reverse('account_login')}?next={request.path}")
            
            if not has_permission(request.user, permission_codename):
                return HttpResponseForbidden("No tienes permiso para acceder a esta página")
                
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def clear_user_permissions_cache(user_id):
    """
    Limpia la caché de permisos para un usuario específico
    """
    cache.delete(f"user_permissions_{user_id}")
    cache.delete(f"user_roles_{user_id}")