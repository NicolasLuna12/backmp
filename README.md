# Microservicio de Integración MercadoPago

Este microservicio permite la integración con la API de MercadoPago para la gestión de pagos, notificaciones y conciliación de transacciones. Está desarrollado en Django y pensado para ser desplegado fácilmente en entornos cloud (Heroku, AWS, etc).

## Características

- Creación y gestión de pagos a través de MercadoPago.
- Recepción y procesamiento de notificaciones de pago.
- Serialización y administración de modelos de pagos.
- API RESTful para interactuar con otros servicios.
- Configuración lista para producción (Procfile, settings, etc).

## Estructura del Proyecto

```
mercadopago_service/
│   manage.py
│   Procfile
│   requirements.txt
│
├── mp_integration/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── payment_service/
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── services.py
    ├── services_new.py
    ├── tests.py
    ├── urls.py
    └── views.py
```

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/NicolasLuna12/backmp.git
   cd backmp
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configura las variables de entorno necesarias en `mp_integration/settings.py` (API keys de MercadoPago, base de datos, etc).

## Ejecución

Para iniciar el servidor de desarrollo:

```bash
python mercadopago_service/manage.py runserver
```

## Despliegue

Incluye un `Procfile` para despliegue en Heroku u otros servicios compatibles con WSGI.

## Pruebas

Ejecuta los tests con:

```bash
python mercadopago_service/manage.py test
```

## Endpoints principales

- `/api/payments/` - Gestión de pagos.
- `/api/notifications/` - Recepción de notificaciones de MercadoPago.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request.

## Licencia

MIT
