"""
================================================================================
📋 GUÍA DE ESTRUCTURA DE RUTAS Y BLUEPRINTS
================================================================================

¿QUÉ ES ESTO?
=============
Este archivo explica cómo está organizada la estructura de rutas en el backend
y cómo agregar nuevas rutas de forma profesional.

ESTRUCTURA ACTUAL
=================
La aplicación usa BLUEPRINTS, que son módulos de Flask que agrupan rutas
relacionadas bajo un mismo prefijo de URL.

src/api/
├── app.py                          (Inicialización de la app)
├── routes/
│   ├── __init__.py                 (Carga los blueprints - punto de entrada)
│   ├── auth_routes.py              (Rutas de autenticación)
│   ├── user_routes.py              (Rutas de usuarios)
│   ├── association_routes.py       (Rutas de asociaciones)
│   ├── events_routes.py            (Rutas de eventos)
│   ├── donation_routes.py          (Rutas de donaciones)
│   ├── rating_routes.py            (Rutas de calificaciones)
│   ├── volunteers_routes.py        (Rutas de voluntarios)
│   └── password_reset_routes.py    (Rutas de reset de contraseña)
│
├── controllers/
│   ├── auth_controller.py          (Lógica de autenticación)
│   ├── association_controller.py   (Lógica de asociaciones)
│   └── rating_controller.py        (Lógica de calificaciones)
│
├── services/
│   ├── auth_service.py             (Servicios de autenticación)
│   ├── donation_service.py         (Integración con Stripe)
│   ├── email_service.py            (Integración con SendGrid)
│   └── rating_service.py           (Lógica de ratings)
│
├── models/
│   ├── user.py                     (Modelo de Usuario)
│   ├── association.py              (Modelo de Asociación)
│   ├── events.py                   (Modelo de Eventos)
│   ├── donation.py                 (Modelo de Donaciones)
│   └── rating.py                   (Modelo de Ratings)
│
├── schemas/
│   ├── user_schema.py              (Validación de datos de usuario)
│   ├── association_schema.py       (Validación de datos de asociación)
│   └── event_schema.py             (Validación de datos de evento)
│
└── tests/                          (Tests unitarios e integración)
    └── [vacío - por llenar]


CÓMO FUNCIONAN LOS BLUEPRINTS
=============================

1. DEFINICIÓN (En cada archivo de rutas, ej: auth_routes.py)
   -------
   from flask import Blueprint
   
   auth_bp = Blueprint('auth', __name__)
   
   @auth_bp.route('/register/user', methods=['POST'])
   def register_user():
       # Lógica aquí
       pass

2. REGISTRO (En routes/__init__.py)
   -------
   from .auth_routes import auth_bp
   
   api = Blueprint('api', __name__)
   api.register_blueprint(auth_bp, url_prefix='/auth')

3. RESULTADO EN LA APP
   -------
   Cuando registramos así, la ruta completa es:
   POST /api/auth/register/user
                ↑     ↑
          api prefix  blueprint prefix


FLUJO DE UNA PETICIÓN HTTP
============================

Cliente                 Routes                Controllers           Services
   │                       │                        │                    │
   │  POST /api/auth/login │                        │                    │
   ├──────────────────────>│                        │                    │
   │                       │  Validar datos         │                    │
   │                       │  (DTOs/schemas)        │                    │
   │                       │                        │                    │
   │                       │  AuthController        │                    │
   │                       │  .login(data)          │                    │
   │                       ├──────────────────────>│                    │
   │                       │                        │  AuthService       │
   │                       │                        │  .verify_password() │
   │                       │                        ├──────────────────>│
   │                       │                        │   (búsqueda en DB) │
   │                       │                        │<──────────────────┤
   │                       │                        │                    │
   │                       │                        │  .generate_token() │
   │                       │                        ├──────────────────>│
   │                       │<───── resultado ─────┤                    │
   │<──── JSON response ──┤                        │                    │
   │  (token + user data) │                        │                    │
   
   
SEPARACIÓN DE RESPONSABILIDADES
================================

┌──────────────────────────────────────────────────────────┐
│ ROUTES (auth_routes.py)                                  │
│ ──────────────────────────                               │
│ - Define endpoints (URLs)                                │
│ - Valida formato de entrada (JSON válido)                │
│ - Llama a controllers                                    │
│ - Devuelve respuestas HTTP (JSON, status code)          │
│ NUNCA: Lógica de negocio, acceso a BD, criptografía    │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ CONTROLLERS (auth_controller.py)                         │
│ ────────────────────────                                 │
│ - Lógica central de la feature                           │
│ - Validación de reglas de negocio (¿email existe?)       │
│ - Orquestación (qué pasos ejecutar)                      │
│ - Prepara respuestas para devolver                       │
│ NUNCA: Queries SQL directas, logística de email/SMS      │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ SERVICES (auth_service.py)                               │
│ ──────────────────────                                   │
│ - Funciones reutilizables                                │
│ - Integraciones externas (BD, email, pagos)              │
│ - Lógica compleja (hashing, tokens, criptografía)        │
│ NUNCA: Validación HTTP, devolución de respuestas         │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ SCHEMAS/DTOs (user_schema.py)                            │
│ ──────────────────────────                               │
│ - Definen qué datos se esperan en cada endpoint          │
│ - Validan tipos de datos (string, int, email)            │
│ - Validan reglas (email con @ , contraseña mín 8 chars)  │
│ - Documentan la API (qué campos son requeridos)          │
└──────────────────────────────────────────────────────────┘


EJEMPLO REAL: LOGIN
===================

1. FRONTEND ENVÍA:
   POST /api/auth/login
   Body: { "email": "user@example.com", "password": "123456" }

2. ROUTE (auth_routes.py):
   @auth_bp.route('/login', methods=['POST'])
   def login():
       data = request.get_json()
       # Validar estructura: ¿tiene email y password?
       return AuthController.login(data)
   
3. CONTROLLER (auth_controller.py):
   @staticmethod
   def login(data):
       # ¿El email está registrado?
       user = AuthService.get_user_by_email(data['email'])
       if not user:
           return {"error": "Usuario no encontrado"}, 404
       
       # ¿La contraseña es correcta?
       if not AuthService.verify_password(user, data['password']):
           return {"error": "Contraseña incorrecta"}, 401
       
       # Generar token y devolver
       tokens = AuthService.generate_token(user)
       return {"user": user, "token": tokens}, 200

4. SERVICES (auth_service.py):
   @staticmethod
   def verify_password(user, password):
       return bcrypt.checkpw(password, user.password_hash)
   
   @staticmethod
   def generate_token(user):
       access_token = create_access_token(identity=user.id)
       return access_token


AGREGANDO UNA NUEVA RUTA
========================

Si necesitas agregar una ruta nueva, sigue estos pasos:

PASO 1: Define la ruta (rutas/mi_feature_routes.py)
───────────────────────────────────────────────────
from flask import Blueprint, request, jsonify
from ..controllers.mi_feature_controller import MiFeatureController

mi_feature_bp = Blueprint('mi_feature', __name__)

@mi_feature_bp.route('/nuevo-endpoint', methods=['POST'])
def nuevo_endpoint():
    data = request.get_json()
    # Validar datos con schema
    return MiFeatureController.metodo(data)


PASO 2: Registra el blueprint (routes/__init__.py)
──────────────────────────────────────────────────
from .mi_feature_routes import mi_feature_bp

api.register_blueprint(mi_feature_bp, url_prefix='/mi-feature')


PASO 3: Crea el controller (controllers/mi_feature_controller.py)
────────────────────────────────────────────────────────────────
from ..services.mi_feature_service import MiFeatureService

class MiFeatureController:
    @staticmethod
    def metodo(data):
        # Lógica de negocio
        resultado = MiFeatureService.hacer_algo(data)
        return {"success": True, "data": resultado}, 200


PASO 4: Crea el service (services/mi_feature_service.py)
─────────────────────────────────────────────────────────
from ..models import db, MiModelo

class MiFeatureService:
    @staticmethod
    def hacer_algo(data):
        # Queries a BD, integraciones
        objeto = MiModelo(...)
        db.session.add(objeto)
        db.session.commit()
        return objeto


PASO 5: Crea el schema (schemas/mi_feature_schema.py)
──────────────────────────────────────────────────────
def validar_datos(data):
    """Valida estructura de datos para mi_feature"""
    if 'nombre' not in data:
        return {"error": "Campo 'nombre' requerido"}, 400
    if not isinstance(data['nombre'], str):
        return {"error": "Campo 'nombre' debe ser string"}, 400
    return None


PASO 6: Usa en la ruta (rutas/mi_feature_routes.py)
───────────────────────────────────────────────────
from ..schemas.mi_feature_schema import validar_datos

@mi_feature_bp.route('/nuevo-endpoint', methods=['POST'])
def nuevo_endpoint():
    data = request.get_json()
    
    # Validar
    error = validar_datos(data)
    if error:
        return error
    
    # Procesar
    return MiFeatureController.metodo(data)


MEJORES PRÁCTICAS
=================

✅ HAZE:
  - Aislar lógica en services
  - Reutilizar código en controllers
  - Validar entrada en schemas
  - Usar nombres descriptivos
  - Documentar con docstrings
  - Mantener las funciones cortas
  - Usar excepciones para errores

❌ NO HAGAS:
  - SQL directo en routes
  - Lógica compleja en controllers
  - Validación de BD en routes
  - Responder directamente desde services
  - Importaciones circulares
  - Funciones de 100+ líneas
  - Ignorar excepciones


================================================================================
"""
