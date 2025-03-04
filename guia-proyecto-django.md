# Guía de Implementación: Sistema de Gestión de Empresas con Django y Microservicios

## Descripción del Proyecto
Sistema Django con autenticación segura (allauth + Google) donde los usuarios pueden crear una cuenta, iniciar sesión, registrar su empresa con logo y añadir hasta 5 productos. La arquitectura estará basada en microservicios utilizando Docker.

## Estructura del Proyecto
- **Microservicio de Autenticación**: Gestión de usuarios y autenticación
- **Microservicio de Empresas y Productos**: Manejo de perfiles empresariales y productos
- **Microservicio de Base de Datos**: PostgreSQL

## 1. Configuración del Entorno

### 1.1 Preparación del Entorno
1. Instalar Python y pip
2. Instalar Docker y Docker Compose
3. Crear un directorio para el proyecto
4. Configurar un entorno virtual para desarrollar localmente:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
5. Instalar Django:
   ```
   pip install django
   ```

### 1.2 Crear el Proyecto Django Base
1. Crear el proyecto Django principal:
   ```
   django-admin startproject core .
   ```
2. Probar la instalación de Django:
   ```
   python manage.py runserver
   ```
3. Verificar funcionamiento visitando: http://127.0.0.1:8000/

## 2. Microservicio de Autenticación

### 2.1 Crear la Aplicación "autenticar"
1. Crear la app:
   ```
   python manage.py startapp autenticar
   ```
2. Añadir la app a INSTALLED_APPS en settings.py
3. Configurar la zona horaria y el idioma en settings.py

### 2.2 Configurar Django Allauth
1. Instalar django-allauth:
   ```
   pip install django-allauth
   ```
2. Añadir allauth y sus dependencias a INSTALLED_APPS
3. Configurar AUTHENTICATION_BACKENDS en settings.py
4. Configurar SITE_ID en settings.py
5. Añadir las URLs de allauth en urls.py
6. Configurar el tiempo de expiración de sesión (1 hora):
   ```
   SESSION_COOKIE_AGE = 3600  # 1 hora en segundos
   SESSION_EXPIRE_AT_BROWSER_CLOSE = True
   ```

### 2.3 Configurar Autenticación con Google
1. Crear un proyecto en Google Developer Console
2. Configurar OAuth credentials (Client ID y Secret)
3. Añadir los datos de Google OAuth en settings.py
4. Configurar los proveedores sociales en settings.py

### 2.4 Configurar Verificación por Email
1. Configurar el backend de email en settings.py
2. Crear plantillas de email personalizadas
3. Configurar ACCOUNT_EMAIL_VERIFICATION = "mandatory"

### 2.5 Crear Modelos y Migraciones
1. Definir el modelo de Usuario personalizado (si es necesario)
2. Ejecutar migraciones:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Verificar que la base de datos se ha actualizado correctamente

### 2.6 Crear Vistas, Plantillas y URLs
1. Crear las vistas de login, registro y verificación
2. Crear las plantillas de autenticación personalizadas
3. Configurar las URLs en autenticar/urls.py
4. Incluir las URLs de la app en el urls.py principal

### 2.7 Probar el Servicio de Autenticación
1. Ejecutar el servidor:
   ```
   python manage.py runserver
   ```
2. Verificar la creación de cuentas
3. Verificar el inicio de sesión con credenciales
4. Verificar el inicio de sesión con Google
5. Comprobar la funcionalidad de verificación por email
6. Verificar el cierre de sesión automático después de 1 hora

## 3. Microservicio de Empresas y Productos

### 3.1 Crear la Aplicación "empresarios"
1. Crear la app:
   ```
   python manage.py startapp empresarios
   ```
2. Añadir la app a INSTALLED_APPS en settings.py

### 3.2 Configurar Modelos
1. Crear el modelo Empresa con campos:
   - Usuario (ForeignKey al modelo de Usuario)
   - Nombre
   - Descripción
   - Logo (ImageField)
   - Fecha de creación
   - Información adicional

2. Crear el modelo Producto con campos:
   - Empresa (ForeignKey al modelo Empresa)
   - Nombre
   - Descripción
   - Precio
   - Imagen (opcional)
   - Fecha de creación
   - Información adicional

3. Ejecutar migraciones:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

### 3.3 Implementar Restricción de 5 Productos
1. Crear una validación en el modelo/vista para limitar a 5 productos por empresa
2. Añadir mensajes de error cuando se intente superar el límite

### 3.4 Crear Vistas, Plantillas y URLs
1. Crear vistas basadas en clases para:
   - Creación, edición y visualización de empresas
   - Creación, edición y visualización de productos
   - Dashboard principal para empresarios

2. Implementar decoradores de login_required en todas las vistas
3. Crear plantillas para todas las vistas
4. Configurar las URLs en empresarios/urls.py
5. Incluir las URLs de la app en el urls.py principal

### 3.5 Implementar Subida de Imágenes
1. Configurar MEDIA_ROOT y MEDIA_URL en settings.py
2. Crear formularios para subir logos e imágenes
3. Implementar validaciones para las imágenes (tamaño, formato)

### 3.6 Probar el Servicio de Empresas y Productos
1. Ejecutar el servidor:
   ```
   python manage.py runserver
   ```
2. Verificar la creación de perfiles de empresa
3. Verificar la subida de logos
4. Verificar la creación de productos (hasta 5)
5. Comprobar que solo usuarios autenticados pueden acceder
6. Verificar que después de 1 hora se cierra la sesión

## 4. Configuración de Docker y Microservicios

### 4.1 Diseñar la Arquitectura de Microservicios
1. Definir la estructura de directorios para cada microservicio:
   ```
   /proyecto
   ├── auth-service/
   │   ├── autenticar/
   │   ├── Dockerfile
   │   ├── manage.py
   │   ├── requirements.txt
   │   └── ...
   ├── business-service/
   │   ├── empresarios/
   │   ├── Dockerfile
   │   ├── manage.py
   │   ├── requirements.txt
   │   └── ...
   ├── postgres-service/
   │   └── ...
   └── docker-compose.yml
   ```

### 4.2 Crear Dockerfiles para Cada Servicio
1. Crear Dockerfile para el Servicio de Autenticación
2. Crear Dockerfile para el Servicio de Empresas y Productos
3. Configurar volúmenes para persistencia de datos

### 4.3 Configurar PostgreSQL
1. Crear servicio de PostgreSQL en docker-compose.yml
2. Configurar volúmenes para persistencia de datos
3. Establecer variables de entorno para usuario, contraseña y base de datos

### 4.4 Configurar Docker Compose
1. Crear archivo docker-compose.yml con los tres servicios
2. Configurar dependencias entre servicios
3. Configurar redes para comunicación entre servicios
4. Mapear puertos para acceso externo

### 4.5 Configurar Comunicación entre Microservicios
1. Implementar API REST para comunicación entre servicios
2. Configurar credenciales y seguridad para APIs internas
3. Implementar manejo de errores y reintentos

### 4.6 Probar la Arquitectura de Microservicios
1. Construir las imágenes:
   ```
   docker-compose build
   ```
2. Iniciar los servicios:
   ```
   docker-compose up
   ```
3. Verificar que todos los servicios se inicien correctamente
4. Probar la comunicación entre servicios
5. Verificar la persistencia de datos en PostgreSQL

## 5. Seguridad y Mantenimiento

### 5.1 Implementar Medidas de Seguridad Adicionales
1. Configurar CSRF, CORS y otras protecciones
2. Implementar limitación de peticiones (rate limiting)
3. Configurar HTTPS con certificados SSL
4. Revisar configuraciones de seguridad en settings.py

### 5.2 Crear Scripts de Mantenimiento
1. Crear scripts para respaldo de base de datos
2. Implementar monitoreo básico
3. Configurar rotación de logs

### 5.3 Preparar para Producción
1. Configurar settings.py para entorno de producción
2. Deshabilitar DEBUG
3. Configurar servidor web (Nginx, etc.)
4. Establecer variables de entorno sensibles

## 6. Pruebas Finales del Sistema

### 6.1 Pruebas de Integración
1. Verificar el flujo completo desde registro hasta creación de productos
2. Probar la autenticación con credenciales y Google
3. Verificar límite de 5 productos por empresa
4. Probar cierre automático de sesión después de 1 hora

### 6.2 Pruebas de Carga
1. Simular múltiples usuarios concurrentes
2. Verificar el rendimiento del sistema
3. Identificar y resolver cuellos de botella

### 6.3 Documentación Final
1. Documentar la arquitectura del sistema
2. Crear manual de usuario
3. Documentar procedimientos de mantenimiento y recuperación

## Notas Adicionales

- Recuerda ejecutar `makemigrations` y `migrate` después de cada cambio en los modelos
- Utiliza entornos virtuales para desarrollo local
- Mantén los requisitos actualizados en requirements.txt
- Considera implementar pruebas unitarias para validar la funcionalidad
- Implementa logging para facilitar la depuración
