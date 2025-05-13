# Documentación de Endpoints de Integración con Mercado Pago

## Información General

El microservicio de pagos proporciona dos endpoints principales que pueden ser consumidos por el frontend:

1. Endpoint para crear una preferencia de pago
2. Endpoint para recibir notificaciones de Mercado Pago (webhook)

### URL Base

```
https://tu-dominio.com
```

Reemplaza "tu-dominio.com" con el dominio donde esté desplegado el microservicio.

## Endpoints

### 1. Crear Preferencia de Pago

**Endpoint:** `/payment/create-preference/`
**Método:** POST
**Descripción:** Este endpoint se utiliza para crear una preferencia de pago en Mercado Pago. Recibe el token del usuario y opcionalmente su email, consulta el carrito del usuario en el backend principal, y genera una URL de pago.

#### Parámetros de Solicitud

```json
{
  "user_token": "token-del-usuario-obtenido-del-backend-principal",
  "email": "correo@ejemplo.com" // Opcional
}
```

#### Respuesta Exitosa (Código 201)

```json
{
  "init_point": "https://www.mercadopago.com.ar/checkout/v1/redirect?pref_id=123456789-abcdefgh-1234-abcd-1234-abcdefghijkl",
  "preference_id": "123456789-abcdefgh-1234-abcd-1234-abcdefghijkl",
  "payment_request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### Respuestas de Error

- **400 Bad Request**: Datos inválidos, carrito vacío o no disponible
```json
{
  "error": "No se pudo obtener el carrito o está vacío"
}
```

- **500 Internal Server Error**: Error al crear la preferencia
```json
{
  "error": "Error al crear la preferencia de pago"
}
```

#### Ejemplo de Uso (JavaScript)

```javascript
const createPayment = async (userToken) => {
  try {
    const response = await fetch('https://tu-dominio.com/payment/create-preference/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_token: userToken,
        email: 'usuario@ejemplo.com' // Opcional
      })
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Error al crear el pago');
    }
    
    const data = await response.json();
    
    // Redireccionar al usuario a la página de pago de Mercado Pago
    window.location.href = data.init_point;
    
    return data;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
};
```

### 2. Webhook para Notificaciones de Mercado Pago

**Endpoint:** `/payment/webhook/`
**Método:** POST
**Descripción:** Este endpoint es para uso exclusivo de Mercado Pago. No debe ser consumido directamente por el frontend. Mercado Pago envía notificaciones a este endpoint cuando el estado de un pago cambia.

> **Nota**: Este endpoint debe ser configurado en el panel de desarrolladores de Mercado Pago como URL de notificaciones (webhook).

## Flujo de Integración

1. El usuario selecciona productos en el frontend y los agrega al carrito.
2. Cuando el usuario está listo para pagar, el frontend:
   a. Solicita un token de acceso al backend principal (si aún no lo tiene).
   b. Envía una solicitud al endpoint `/payment/create-preference/` con el token del usuario.
   c. Recibe la URL de pago (`init_point`) y redirecciona al usuario a esa URL.
3. El usuario completa el pago en la plataforma de Mercado Pago.
4. Mercado Pago envía una notificación al webhook configurado.
5. El microservicio procesa la notificación y, si el pago fue aprobado, notifica al backend principal.
6. El backend principal confirma el pedido.

## Consideraciones de Seguridad

- El token de usuario debe ser enviado de forma segura.
- La comunicación debe realizarse a través de HTTPS.
- No almacene ni muestre el token de usuario en el frontend más tiempo del necesario.

## Endpoint de Estado del Servicio

**Endpoint:** `/health/`
**Método:** GET
**Descripción:** Este endpoint permite verificar si el servicio está en funcionamiento.

#### Respuesta Exitosa (Código 200)

```json
{
  "status": "ok", 
  "service": "mercadopago-integration"
}
```

#### Ejemplo de Uso (JavaScript)

```javascript
const checkServiceStatus = async () => {
  try {
    const response = await fetch('https://tu-dominio.com/health/');
    const data = await response.json();
    return data.status === 'ok';
  } catch (error) {
    console.error('Error al verificar el estado del servicio:', error);
    return false;
  }
};
```
