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

## Configuración de Seguridad

### 🔒 Restricción de Dominio

El microservicio está configurado para **SOLO aceptar peticiones desde**:
- `https://ispcfood.netlify.app`

### 🛡️ Capas de Seguridad Implementadas

1. **CORS Restrictivo**: Solo permite requests desde el dominio autorizado
2. **Middleware de Seguridad**: Verifica origen y referer en requests críticos  
3. **Headers de Seguridad**: X-Content-Type-Options, X-Frame-Options, etc.
4. **Rate Limiting**: Máximo 100 requests por minuto por IP (en producción)
5. **Logging de Seguridad**: Registra intentos de acceso no autorizados

### ⚠️ Para Desarrollo Local

Si necesitas activar el modo debug para pruebas locales:

```bash
# Hacer backup de la configuración de producción
cp mercadopago_service/.env mercadopago_service/.env.production

# Usar configuración de desarrollo
cp .env.development mercadopago_service/.env

# Para volver a producción
cp mercadopago_service/.env.production mercadopago_service/.env
```

**¡IMPORTANTE!** Siempre verificar que estás en modo producción antes de desplegar:

```bash
# Verificar configuración actual
python security_check.py

# Verificar configuración de Django
cd mercadopago_service
python manage.py check --deploy
```

### 🔒 Verificación de Seguridad

Ejecuta el script de verificación de seguridad:

```bash
python security_check.py
```

✅ **ESTADO ACTUAL: CONFIGURACIÓN DE PRODUCCIÓN ACTIVA**

- ✅ SECRET_KEY segura generada
- ✅ DEBUG=False (modo producción)  
- ✅ CORS restringido solo a ispcfood.netlify.app
- ✅ Middleware de seguridad activo
- ✅ Headers de seguridad configurados

### 🛡️ Configuración Segura

#### Para Desarrollo:
- **Nunca** commitees el archivo `.env` al repositorio
- Usa el archivo `.env.example` como plantilla para nuevas configuraciones
- Mantén `DEBUG=True` solo en desarrollo local

#### Para Producción:
- Genera una nueva `DJANGO_SECRET_KEY` fuerte:
  ```python
  from django.core.management.utils import get_random_secret_key
  print(get_random_secret_key())
  ```
- Configura `DEBUG=False`
- Restringe `ALLOWED_HOSTS` a dominios específicos: `tu-dominio.com,www.tu-dominio.com`
- Configura CORS para dominios específicos: `CORS_ALLOW_ALL_ORIGINS=False`
- Usa certificados SSL/TLS (HTTPS)
- Implementa rate limiting y firewall

#### Variables de Entorno Críticas:

**⚠️ OBLIGATORIAS:**
- `DJANGO_SECRET_KEY`: Clave secreta única y segura
- `MERCADOPAGO_ACCESS_TOKEN`: Token de MercadoPago

**🔧 CONFIGURACIÓN:**
- `DJANGO_DEBUG`: `False` en producción
- `DJANGO_ALLOWED_HOSTS`: Hosts específicos en producción
- `CORS_ALLOW_ALL_ORIGINS`: `False` en producción
- `CORS_ALLOWED_ORIGINS`: Dominios permitidos específicos

**📊 BASE DE DATOS:**
- `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

### 📋 Checklist de Seguridad

- [ ] Archivo `.env` no está en git
- [ ] `SECRET_KEY` generada y segura
- [ ] `DEBUG=False` en producción
- [ ] `ALLOWED_HOSTS` restringido
- [ ] CORS configurado correctamente
- [ ] HTTPS habilitado
- [ ] Credenciales de BD seguras
- [ ] Token de MercadoPago válido

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request.

## Licencia

Nicolas Luna
