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

2. Crea un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno:
   - Copia el archivo `.env.example` a `.env` en la carpeta `mercadopago_service/`
   - Edita el archivo `.env` con tus credenciales reales
   ```bash
   cp .env.example mercadopago_service/.env
   ```

5. Ejecuta las migraciones:
   ```bash
   cd mercadopago_service
   python manage.py migrate
   ```

## Ejecución

Para iniciar el servidor de desarrollo:

```bash
cd mercadopago_service
python manage.py runserver
```

## Variables de Entorno

El proyecto utiliza variables de entorno para proteger las credenciales sensibles. Configura las siguientes variables en tu archivo `.env`:

- `DJANGO_SECRET_KEY`: Clave secreta de Django
- `DJANGO_DEBUG`: Modo debug (True/False)
- `DJANGO_ALLOWED_HOSTS`: Hosts permitidos separados por comas
- `DB_ENGINE`: Motor de base de datos
- `DB_NAME`: Nombre de la base de datos
- `DB_USER`: Usuario de la base de datos
- `DB_PASSWORD`: Contraseña de la base de datos
- `DB_HOST`: Host de la base de datos
- `DB_PORT`: Puerto de la base de datos
- `MERCADOPAGO_ACCESS_TOKEN`: Token de acceso de MercadoPago
- `MAIN_BACKEND_URL`: URL del backend principal

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

## Seguridad

- **Nunca** commitees el archivo `.env` al repositorio
- Usa el archivo `.env.example` como plantilla para nuevas configuraciones
- Cambia la `DJANGO_SECRET_KEY` en producción
- Asegúrate de configurar `DEBUG=False` en producción
- Restringe `ALLOWED_HOSTS` a los dominios específicos en producción

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request.

## Licencia

Nicolas Luna
