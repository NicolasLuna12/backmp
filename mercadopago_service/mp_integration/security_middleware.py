"""
Middleware de seguridad personalizado para el microservicio MercadoPago
"""
from django.http import HttpResponseForbidden
from django.conf import settings
import logging
import time

logger = logging.getLogger(__name__)

class SecurityMiddleware:
    """
    Middleware que agrega capas adicionales de seguridad
    """
    
    ALLOWED_ORIGINS = [
        'https://ispcfood.netlify.app',
        'https://ispcfood.netlify.app/',
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Verificar origen en requests críticos
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            origin = request.META.get('HTTP_ORIGIN')
            referer = request.META.get('HTTP_REFERER')
            
            # En producción, ser más estricto
            if not settings.DEBUG:
                if origin and origin not in self.ALLOWED_ORIGINS:
                    logger.warning(f"Request rechazado - Origen no autorizado: {origin} desde IP: {self.get_client_ip(request)}")
                    return HttpResponseForbidden("Origen no autorizado")
                
                if referer and not any(referer.startswith(allowed) for allowed in self.ALLOWED_ORIGINS):
                    logger.warning(f"Request rechazado - Referer no autorizado: {referer} desde IP: {self.get_client_ip(request)}")
                    return HttpResponseForbidden("Referer no autorizado")
        
        response = self.get_response(request)
        
        # Agregar headers de seguridad adicionales
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'same-origin'
        # Content Security Policy para permitir MercadoPago .com y .com.ar
        response['Content-Security-Policy'] = (
            "frame-src 'self' https://www.mercadopago.com https://www.mercadopago.com.ar "
            "https://www.mercadolibre.com https://mpago.la https://translate.google.com https://www.gstatic.com;"
        )
        return response
    
    def get_client_ip(self, request):
        """Obtener la IP real del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RateLimitMiddleware:
    """
    Middleware simple de rate limiting por IP
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_requests = {}
    
    def __call__(self, request):
        if not settings.DEBUG:  # Solo en producción
            client_ip = self.get_client_ip(request)
            current_time = time.time()
            
            # Limpiar requests antiguos (más de 1 minuto)
            self.ip_requests = {
                ip: requests for ip, requests in self.ip_requests.items()
                if any(req_time > current_time - 60 for req_time in requests)
            }
            
            # Verificar rate limit (máximo 100 requests por minuto por IP)
            if client_ip in self.ip_requests:
                recent_requests = [
                    req_time for req_time in self.ip_requests[client_ip]
                    if req_time > current_time - 60
                ]
                
                if len(recent_requests) >= 100:
                    logger.warning(f"Rate limit excedido para IP: {client_ip}")
                    return HttpResponseForbidden("Rate limit excedido")
                
                self.ip_requests[client_ip] = recent_requests + [current_time]
            else:
                self.ip_requests[client_ip] = [current_time]
        
        return self.get_response(request)
    
    def get_client_ip(self, request):
        """Obtener la IP real del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
