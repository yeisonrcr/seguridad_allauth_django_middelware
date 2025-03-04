// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Mostrar mensajes solo por un tiempo limitado
    const messages = document.querySelectorAll('.message');
    if (messages.length > 0) {
        setTimeout(function() {
            messages.forEach(function(message) {
                message.style.opacity = '0';
                setTimeout(function() {
                    message.style.display = 'none';
                }, 500);
            });
        }, 5000);
    }
    
    // Mejorar seguridad en formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        // Prevenir múltiples envíos
        form.addEventListener('submit', function(e) {
            if (this.dataset.submitted === 'true') {
                e.preventDefault();
                return;
            }
            this.dataset.submitted = 'true';
            
            // Deshabilitar botones después del envío
            const buttons = this.querySelectorAll('button[type="submit"]');
            buttons.forEach(function(button) {
                button.disabled = true;
                button.innerText = 'Procesando...';
            });
        });
    });
    
    // Validación básica del lado del cliente
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            const value = this.value;
            
            // Verificar requisitos mínimos
            const hasMinLength = value.length >= 10;
            const hasUpperCase = /[A-Z]/.test(value);
            const hasLowerCase = /[a-z]/.test(value);
            const hasDigit = /\d/.test(value);
            const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(value);
            
            // Mostrar indicadores visuales
            this.classList.toggle('valid', hasMinLength && hasUpperCase && hasLowerCase && hasDigit && hasSpecial);
            this.classList.toggle('invalid', !(hasMinLength && hasUpperCase && hasLowerCase && hasDigit && hasSpecial));
        });
    });
});