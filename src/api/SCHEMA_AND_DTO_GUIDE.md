"""
================================================================================
📋 DTOs (DATA TRANSFER OBJECTS) - VALIDACION DE DATOS
================================================================================

¿QUÉ ES UN DTO?
===============
DTO = Data Transfer Object (Objeto de Transferencia de Datos)

Es una clase que:
1. Define qué datos espera recibir
2. Valida que los datos sean correctos
3. Transforma datos brutos en objetos estructurados
4. Documenta la API (qué campos son requeridos)

VENTAJAS:
---------
✅ Una sola fuente de verdad para validación
✅ Reutilizable en múltiples rutas
✅ Mensajes de error consistentes
✅ Documentación automática
✅ Type hints (autocompletado en el editor)
✅ Fácil de testear


EJEMPLO 1: MANUAL (Función)
============================

# Forma antigua (función simple)
def validate_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None

def validate_user_data(data):
    errors = {}
    if not data.get('email'):
        errors['email'] = 'El email es obligatorio'
    elif not validate_email(data['email']):
        errors['email'] = 'Por favor, introduce un email válido'
    
    if errors:
        return None, errors
    return data, None

# Uso
data, errors = validate_user_data(request.get_json())
if errors:
    return jsonify(errors), 400


EJEMPLO 2: MODERNO (Dataclass)
===============================

# Forma moderna (dataclass + validación)
from dataclasses import dataclass
from typing import Optional

@dataclass
class UserLoginDTO:
    \"\"\"DTO para login de usuarios\"\"\"
    email: str
    password: str
    remember_me: Optional[bool] = False
    
    def validate(self) -> dict:
        \"\"\"Valida los datos y devuelve errores si hay\"\"\"
        errors = {}
        
        # Email
        if not self.email:
            errors['email'] = 'El email es obligatorio'
        elif not self._is_valid_email():
            errors['email'] = 'Email inválido'
        
        # Password
        if not self.password:
            errors['password'] = 'La contraseña es obligatoria'
        elif len(self.password) < 8:
            errors['password'] = 'La contraseña debe tener al menos 8 caracteres'
        
        return errors
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

# Uso
dto = UserLoginDTO(**request.get_json())
errors = dto.validate()
if errors:
    return jsonify(errors), 400

# Ahora puedes usar el DTO de forma segura
print(dto.email)  # ✅ Type hints funcionan
print(dto.remember_me)  # ✅ Valor por defecto


ESTRUCTURA RECOMENDADA
======================

schemas/
├── __init__.py
├── base_schema.py           # Clase base reutilizable
├── user_schemas.py          # DTOs de usuario
├── association_schemas.py   # DTOs de asociación
├── event_schemas.py         # DTOs de eventos
└── validators.py            # Funciones de validación reutilizables


ARCHIVO: base_schema.py (clase base)
=====================================
\"\"\"

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
import re

@dataclass
class BaseDTO:
    \"\"\"Clase base para todos los DTOs\"\"\"
    
    def validate(self) -> Dict[str, str]:
        \"\"\"Método que debe ser sobrescrito en subclases\"\"\"
        return {}
    
    def to_dict(self) -> Dict[str, Any]:
        \"\"\"Convierte el DTO a diccionario\"\"\"
        return asdict(self)
    
    @staticmethod
    def validate_email(email: str) -> bool:
        \"\"\"Valida formato de email\"\"\"
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_password(password: str, min_length: int = 8) -> bool:
        \"\"\"Valida contraseña\"\"\"
        if len(password) < min_length:
            return False
        has_letter = re.search(r'[A-Za-z]', password)
        has_number = re.search(r'\d', password)
        return bool(has_letter and has_number)
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        \"\"\"Valida número de teléfono español\"\"\"
        clean = re.sub(r'[\s\-\(\)]', '', phone)
        pattern = r'^(\+34)?[6789]\d{8}$'
        return bool(re.match(pattern, clean))


ARCHIVO: user_schemas.py
========================
\"\"\"

from dataclasses import dataclass
from typing import Optional
from .base_schema import BaseDTO

@dataclass
class UserRegistrationDTO(BaseDTO):
    \"\"\"DTO para registro de usuario\"\"\"
    email: str
    password: str
    name: str
    lastname: str
    phone: Optional[str] = None
    profile_image: Optional[str] = None
    
    def validate(self) -> dict:
        errors = {}
        
        # Email
        if not self.email or not self.email.strip():
            errors['email'] = 'El email es obligatorio'
        elif not self.validate_email(self.email):
            errors['email'] = 'Email inválido (ejemplo: usuario@ejemplo.com)'
        
        # Password
        if not self.password:
            errors['password'] = 'La contraseña es obligatoria'
        elif not self.validate_password(self.password):
            errors['password'] = 'La contraseña debe tener mínimo 8 caracteres, letras y números'
        
        # Name
        if not self.name or not self.name.strip():
            errors['name'] = 'El nombre es obligatorio'
        elif len(self.name) > 100:
            errors['name'] = 'El nombre máximo 100 caracteres'
        
        # Lastname
        if not self.lastname or not self.lastname.strip():
            errors['lastname'] = 'El apellido es obligatorio'
        elif len(self.lastname) > 100:
            errors['lastname'] = 'El apellido máximo 100 caracteres'
        
        # Phone (opcional)
        if self.phone and not self.validate_phone(self.phone):
            errors['phone'] = 'Número de teléfono inválido'
        
        return errors


@dataclass
class UserLoginDTO(BaseDTO):
    \"\"\"DTO para login\"\"\"
    email: str
    password: str
    
    def validate(self) -> dict:
        errors = {}
        
        if not self.email:
            errors['email'] = 'El email es obligatorio'
        elif not self.validate_email(self.email):
            errors['email'] = 'Email inválido'
        
        if not self.password:
            errors['password'] = 'La contraseña es obligatoria'
        
        return errors


@dataclass
class UserUpdateProfileDTO(BaseDTO):
    \"\"\"DTO para actualizar perfil de usuario\"\"\"
    name: Optional[str] = None
    lastname: Optional[str] = None
    phone: Optional[str] = None
    profile_image: Optional[str] = None
    
    def validate(self) -> dict:
        errors = {}
        
        if self.name and len(self.name) > 100:
            errors['name'] = 'El nombre máximo 100 caracteres'
        
        if self.lastname and len(self.lastname) > 100:
            errors['lastname'] = 'El apellido máximo 100 caracteres'
        
        if self.phone and not self.validate_phone(self.phone):
            errors['phone'] = 'Número de teléfono inválido'
        
        return errors


CÓMO USAR EN RUTAS
==================

# ANTES (forma antigua)
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validación manual
    if not data.get('email'):
        return jsonify({'error': 'Email obligatorio'}), 400
    if not data.get('password'):
        return jsonify({'error': 'Contraseña obligatoria'}), 400
    
    # Lógica (mezclada con validación)
    user = AuthService.get_user_by_email(data['email'])
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    return AuthController.login(data)


# DESPUÉS (forma moderna con DTO)
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Crear DTO (validación estructurada)
    dto = UserLoginDTO(**data)
    errors = dto.validate()
    
    if errors:
        return jsonify({'errors': errors}), 400
    
    # Lógica (sin validación)
    return AuthController.login(dto)


# En el controller
class AuthController:
    @staticmethod
    def login(dto: UserLoginDTO):
        # Los datos ya están validados
        user = AuthService.get_user_by_email(dto.email)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # ...


VENTAJAS DE ESTA ESTRUCTURA
============================

1. MANTENIBILIDAD
   ✅ Cambio la validación en un solo lugar
   ✅ Todas las rutas usan la misma validación

2. REUTILIZACIÓN
   ✅ UserLoginDTO se usa en /login y /validate-credentials
   ✅ UserRegistrationDTO se usa en /register y /admin-create-user

3. DOCUMENTACIÓN
   ✅ El DTO documenta qué campos acepta cada endpoint
   ✅ Type hints ayudan al desarrollador

4. TESTABILIDAD
   ✅ Fácil crear DTOs con datos de prueba
   ✅ Puedo testear validación sin la ruta HTTP

5. CONSISTENCIA
   ✅ Todos los errores de validación tienen el mismo formato
   ✅ Mensajes de error consistentes en toda la app


EJEMPLO DE TEST
===============

# test_user_schemas.py
import pytest
from src.api.schemas.user_schemas import UserRegistrationDTO

def test_user_registration_valid_data():
    dto = UserRegistrationDTO(
        email='user@example.com',
        password='ValidPass123',
        name='Juan',
        lastname='Pérez'
    )
    errors = dto.validate()
    assert errors == {}

def test_user_registration_invalid_email():
    dto = UserRegistrationDTO(
        email='invalid-email',
        password='ValidPass123',
        name='Juan',
        lastname='Pérez'
    )
    errors = dto.validate()
    assert 'email' in errors

def test_user_registration_weak_password():
    dto = UserRegistrationDTO(
        email='user@example.com',
        password='weak',  # Menos de 8 caracteres
        name='Juan',
        lastname='Pérez'
    )
    errors = dto.validate()
    assert 'password' in errors


NEXT STEPS
==========

1. Crear base_schema.py con la clase BaseDTO
2. Crear user_schemas.py, association_schemas.py, etc.
3. Actualizar rutas para usar los DTOs
4. Agregar tests para validación
5. Documentar en routes/__init__.py cómo crear nuevos DTOs

================================================================================
"""
