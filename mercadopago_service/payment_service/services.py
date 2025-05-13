import logging
import requests
import mercadopago
from django.conf import settings
from payment_service.models import PaymentRequest, PaymentNotification
from decimal import Decimal

logger = logging.getLogger('payment_service')

class CartService:
    """
    Servicio para interactuar con el carrito del usuario en el backend principal
    """
    @staticmethod
    def get_cart(user_token):
        """
        Obtiene el carrito del usuario desde el backend principal
        """
        try:
            url = f"{settings.MAIN_BACKEND_URL}/appCART/ver/"
            headers = {"Authorization": f"Token {user_token}"}
            
            logger.info(f"Consultando carrito en: {url} con token: {user_token[:5]}...")
            
            # Log más detallado de la petición
            logger.info(f"URL completa: {url}")
            logger.info(f"Headers: {headers}")
            
            response = requests.get(url, headers=headers, timeout=10)
            
            # Log detallado de la respuesta
            logger.info(f"Status code: {response.status_code}")
            logger.info(f"Response headers: {response.headers}")
            logger.info(f"Response content: {response.text[:200]}...")  # Primeros 200 caracteres
            
            if response.status_code == 200:
                cart_data = response.json()
                logger.info(f"Carrito obtenido correctamente. Productos: {len(cart_data.get('productos', []))}")
                return cart_data
            else:
                logger.error(f"Error al obtener el carrito: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.exception(f"Error al consultar el carrito: {str(e)}")
            return None
    
    @staticmethod
    def confirm_order(user_token, payment_id):
        """
        Confirma el pedido en el backend principal
        """
        try:
            url = f"{settings.MAIN_BACKEND_URL}/appCART/confirmar/"
            headers = {"Authorization": f"Token {user_token}"}
            data = {"payment_id": payment_id}
            
            logger.info(f"Confirmando pedido en: {url}")
            response = requests.post(url, json=data, headers=headers, timeout=10)
            
            if response.status_code in [200, 201]:
                return True, response.json()
            else:
                logger.error(f"Error al confirmar el pedido: {response.status_code} - {response.text}")
                return False, {"error": response.text}
        except Exception as e:
            logger.exception(f"Error al confirmar el pedido: {str(e)}")
            return False, {"error": str(e)}


class MercadoPagoService:
    """
    Servicio para interactuar con la API de Mercado Pago
    """
    
    def __init__(self):
        self.sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
    
    def create_preference(self, items, external_reference, payer_email=None, notification_url=None):
        """
        Crea una preferencia de pago en Mercado Pago
        """
        try:
            # Construir los datos de la preferencia
            preference_data = {
                "items": items,
                "external_reference": str(external_reference),
                "back_urls": {
                    "success": f"{settings.MAIN_BACKEND_URL}/payment/success",
                    "failure": f"{settings.MAIN_BACKEND_URL}/payment/failure",
                    "pending": f"{settings.MAIN_BACKEND_URL}/payment/pending"
                },
                "auto_return": "approved"
            }
            
            # Agregar URL de notificaciones (webhook) si está disponible
            if notification_url:
                preference_data["notification_url"] = notification_url
            
            # Agregar datos del comprador si están disponibles
            if payer_email:
                preference_data["payer"] = {
                    "email": payer_email
                }
            
            logger.info(f"Creando preferencia de pago: {preference_data}")
            preference_response = self.sdk.preference().create(preference_data)
            
            return preference_response["response"]
        except Exception as e:
            logger.exception(f"Error al crear preferencia de pago: {str(e)}")
            return None
    
    def process_cart_to_items(self, cart_data):
        """
        Procesa los datos del carrito y los convierte al formato requerido por Mercado Pago
        """
        try:
            if not cart_data or not isinstance(cart_data, dict):
                logger.error("Datos del carrito inválidos")
                return []
            
            # Validar el formato del carrito según la estructura del backend principal
            if "productos" not in cart_data:
                logger.error("El carrito no contiene productos")
                return []
            
            items = []
            for producto in cart_data.get("productos", []):
                # Adaptar esto según la estructura real del backend principal
                item = {
                    "id": str(producto.get("id")),
                    "title": producto.get("nombre", "Producto"),
                    "description": producto.get("descripcion", ""),
                    "quantity": int(producto.get("cantidad", 1)),
                    "unit_price": float(producto.get("precio", 0)),
                    "currency_id": "ARS"  # Ajustar según el país
                }
                items.append(item)
            
            return items
        except Exception as e:
            logger.exception(f"Error al procesar carrito a items: {str(e)}")
            return []
    
    def get_payment(self, payment_id):
        """
        Consulta el estado de un pago en Mercado Pago
        """
        try:
            logger.info(f"Consultando pago {payment_id}")
            payment_response = self.sdk.payment().get(payment_id)
            
            if payment_response["status"] == 200:
                return payment_response["response"]
            else:
                logger.error(f"Error al consultar pago: {payment_response['status']}")
                return None
        except Exception as e:
            logger.exception(f"Error al consultar pago: {str(e)}")
            return None
