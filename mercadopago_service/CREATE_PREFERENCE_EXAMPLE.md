# Ejemplo de uso del endpoint /payment/create-preference/

## Descripción
Este endpoint te permite crear una preferencia de pago en Mercado Pago a partir del carrito de un usuario. Al llamar a este endpoint, obtendrás una URL de pago a la que puedes redirigir a tu usuario para completar la compra.

## URL
```
http://localhost:8000/payment/create-preference/
```

## Método
POST

## Encabezados (Headers)
```
Content-Type: application/json
```

## Cuerpo de la solicitud (Request Body)

### Campos obligatorios:
- `user_token`: Token de autenticación del usuario obtenido del backend principal

### Campos opcionales:
- `email`: Correo electrónico del usuario para personalizarlo en la página de pago de Mercado Pago

### Ejemplo:
```json
{
  "user_token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "email": "usuario@ejemplo.com"
}
```

## Respuesta exitosa

### Código: 201 Created

### Cuerpo de la respuesta:
```json
{
  "init_point": "https://www.mercadopago.com.ar/checkout/v1/redirect?pref_id=123456789-abcdefgh-1234-abcd-1234-abcdefghijkl",
  "preference_id": "123456789-abcdefgh-1234-abcd-1234-abcdefghijkl",
  "payment_request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Campos de la respuesta:
- `init_point`: URL a la que debes redirigir al usuario para que realice el pago
- `preference_id`: ID de la preferencia creada en Mercado Pago
- `payment_request_id`: ID de la solicitud de pago en el sistema

## Respuestas de error

### Código: 400 Bad Request
Si el token de usuario es inválido, el carrito no existe o está vacío:

```json
{
  "error": "No se pudo obtener el carrito o está vacío"
}
```

O

```json
{
  "error": "El carrito está vacío"
}
```

O

```json
{
  "error": "No se pudieron procesar los ítems del carrito"
}
```

### Código: 500 Internal Server Error
Si hay un problema al crear la preferencia en Mercado Pago:

```json
{
  "error": "Error al crear la preferencia de pago"
}
```

### Modo de prueba
En ambiente de desarrollo (cuando `DEBUG=True`), es posible usar un token de prueba para simular un carrito:

Si el token contiene la palabra `test`, el servicio generará un carrito de prueba automáticamente:

```json
{
  "user_token": "token_con_test_incluido",
  "email": "prueba@ejemplo.com"
}
```

Esto es útil para probar la integración sin necesidad de tener un carrito real en el backend principal.

## Ejemplo de implementación en JavaScript

```javascript
// Función para crear una preferencia de pago
async function crearPreferenciaDePago(userToken, email = null) {
  try {
    const url = 'http://localhost:8000/payment/create-preference/';
    
    // Preparar datos
    const data = {
      user_token: userToken
    };
    
    // Agregar email si está disponible
    if (email) {
      data.email = email;
    }
    
    // Hacer la petición
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    
    // Procesar la respuesta
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Error al crear la preferencia de pago');
    }
    
    const responseData = await response.json();
    
    // Redireccionar al usuario a la página de pago
    window.location.href = responseData.init_point;
    
    return responseData;
  } catch (error) {
    console.error('Error:', error);
    // Puedes mostrar un mensaje de error al usuario aquí
    throw error;
  }
}

// Uso de la función
document.getElementById('pagar-button').addEventListener('click', async () => {
  try {
    const userToken = 'tu-token-de-usuario'; // Reemplazar con el token real
    const email = 'usuario@ejemplo.com'; // Opcional
    
    // Mostrar un indicador de carga
    showLoadingIndicator();
    
    await crearPreferenciaDePago(userToken, email);
    
    // La redirección a Mercado Pago ocurrirá automáticamente
  } catch (error) {
    // Ocultar indicador de carga
    hideLoadingIndicator();
    
    // Mostrar error al usuario
    showErrorMessage('No se pudo procesar el pago. Por favor, intenta nuevamente.');
  }
});
```

## Notas importantes

1. El token de usuario debe ser válido y corresponder a un usuario registrado en el backend principal.

2. El carrito del usuario debe tener productos para poder crear una preferencia de pago.

3. Una vez que el usuario es redirigido a Mercado Pago, el proceso de pago ocurre en la plataforma de Mercado Pago.

4. Cuando el pago se completa (ya sea con éxito, rechazo o queda pendiente), Mercado Pago enviará una notificación al webhook configurado.

5. No es necesario manejar la respuesta del webhook desde el frontend, ya que la comunicación ocurre directamente entre el backend de Mercado Pago y este microservicio.

6. El microservicio se encargará de confirmar el pedido en el backend principal una vez que reciba la notificación de pago aprobado de Mercado Pago.
