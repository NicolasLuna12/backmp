# Microservicio de Integración con Mercado Pago

Este microservicio proporciona una API para integrar un frontend con Mercado Pago, permitiendo crear preferencias de pago y recibir notificaciones de pago (webhooks). El servicio está diseñado para funcionar en conjunto con un backend principal que gestiona los carritos de compra y los pedidos.

## Características

- Crear preferencias de pago a partir del carrito del usuario
- Recibir y procesar notificaciones (webhooks) de Mercado Pago
- Confirmar pedidos en el backend principal cuando los pagos son aprobados
- Registro de todas las transacciones para auditoría

## Requisitos

- Python 3.9+
- Django 5.2+
- Django REST Framework
- MySQL/MariaDB
- Cuenta de Mercado Pago (Access Token)

## Instalación

1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/mercadopago-service.git
cd mercadopago-service
```

2. Crear un entorno virtual y activarlo

```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate
```

3. Instalar dependencias

```bash
pip install -r requirements.txt
```

4. Crear archivo .env en la raíz del proyecto

```
MERCADOPAGO_ACCESS_TOKEN=TU_ACCESS_TOKEN_DE_MERCADO_PAGO
MAIN_BACKEND_URL=URL_DEL_BACKEND_PRINCIPAL
DEBUG=True
SECRET_KEY=tu-clave-secreta-de-django
```

5. Configurar la base de datos en `mp_integration/settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tu_base_de_datos',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

6. Aplicar migraciones

```bash
python manage.py migrate
```

## Ejecución

Para ejecutar el servidor de desarrollo:

```bash
python manage.py runserver 0.0.0.0:8000
```

Para producción, se recomienda usar Gunicorn con Nginx:

```bash
gunicorn mp_integration.wsgi:application --bind 0.0.0.0:8000
```

## Endpoints API

Para una documentación detallada de los endpoints disponibles, consulta el archivo [API_DOCUMENTATION.md](./API_DOCUMENTATION.md).

## Flujo de Integración

1. El frontend obtiene un token de autenticación del backend principal
2. El frontend solicita una preferencia de pago al microservicio, enviando el token
3. El microservicio consulta el carrito del usuario en el backend principal
4. El microservicio crea una preferencia de pago en Mercado Pago
5. El frontend recibe la URL de pago y redirecciona al usuario
6. El usuario completa el pago en Mercado Pago
7. Mercado Pago envía una notificación al webhook del microservicio
8. Si el pago es aprobado, el microservicio notifica al backend principal

## Despliegue en Producción

Para el despliegue en producción:

1. Configurar un servidor web como Nginx como proxy inverso
2. Usar Gunicorn o uWSGI como servidor de aplicación
3. Configurar un certificado SSL
4. Asegurar que la URL del webhook sea accesible desde Internet
5. Configurar la URL del webhook en el panel de desarrolladores de Mercado Pago

## Solución de Problemas

- **Error al conectar con el backend principal**: Verificar que `MAIN_BACKEND_URL` en .env sea correcta
- **Error al crear preferencia de pago**: Verificar el Access Token de Mercado Pago
- **No se reciben notificaciones**: Verificar que la URL del webhook sea accesible desde Internet

## Logs

Los logs se guardan en el archivo `mp_integration.log` en la raíz del proyecto. En producción, se recomienda configurar un sistema de rotación de logs.

## Monitoreo

Para monitoreo en producción, se puede utilizar el endpoint `/health/` para verificar que el servicio esté funcionando correctamente.

## Contribuir

1. Haz un fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-feature`)
3. Haz commit de tus cambios (`git commit -am 'Añadir nueva feature'`)
4. Haz push a la rama (`git push origin feature/nueva-feature`)
5. Crea un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.
