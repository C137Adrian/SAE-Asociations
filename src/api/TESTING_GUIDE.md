"""
================================================================================
🧪 TESTING EN BACKEND - GUÍA COMPLETA
================================================================================

¿QUÉ ES UN TEST?
================
Un TEST es código que verifica que otro código funcione correctamente.

SIN TESTS:
```
def suma(a, b):
    return a + b

# ¿Funciona? No lo sé, espero que sí...
resultado = suma(2, 3)  # Devuelve 5... probablemente
```

CON TESTS:
```
def test_suma_dos_numeros():
    assert suma(2, 3) == 5  # ✅ Pasa
    assert suma(0, 0) == 0  # ✅ Pasa
    assert suma(-1, 1) == 0 # ✅ Pasa

# Corro: pytest
# Resultado: 3 tests pasados ✅
```


TIPOS DE TESTS
==============

1. UNITARIOS (Tests de unidad)
   ├─ Prueban UNA FUNCIÓN / MÉTODO en aislamiento
   ├─ No necesitan BD, ni API, ni otros servicios
   ├─ Muy rápidos (milisegundos)
   ├─ Ejemplo: ¿AuthService.verify_password() funciona?
   └─ Herramienta: pytest

2. INTEGRACIÓN (Tests de integración)
   ├─ Prueban VARIOS COMPONENTES juntos
   ├─ Pueden usar BD temporal (SQLite en memoria)
   ├─ Más lentos (segundos)
   ├─ Ejemplo: ¿POST /api/auth/register crea usuario + envía email?
   └─ Herramienta: pytest + fixtures de Flask

3. E2E (End to End)
   ├─ Prueban FLUJOS COMPLETOS desde el frontend
   ├─ Requieren servidor corriendo
   ├─ Muy lentos (minutos)
   ├─ Ejemplo: Usuario abre navegador, registra, logea, compra
   └─ Herramienta: Selenium, Cypress, Playwright

PARA ESTA FASE: Enfocamos en UNITARIOS + INTEGRACIÓN


ESTRUCTURA DE TESTS
===================

src/api/tests/
├── __init__.py
├── conftest.py              # Configuración compartida (fixtures)
├── test_models.py           # Tests de modelos
├── test_schemas.py          # Tests de validación (DTOs)
├── unit/
│   ├── __init__.py
│   ├── test_auth_service.py # Tests de AuthService
│   ├── test_donation_service.py
│   └── test_email_service.py
├── integration/
│   ├── __init__.py
│   ├── test_auth_routes.py  # Tests de rutas HTTP
│   ├── test_association_routes.py
│   └── test_donation_routes.py
└── fixtures/
    ├── __init__.py
    └── sample_data.py       # Datos de prueba


HERRAMIENTAS
============

pytest
------
- Framework de testing principal
- Sintaxis simple: def test_...()
- Fixtures (datos de prueba)
- Plugins (coverage, markers, etc)

# Instalar
pip install pytest pytest-cov

# Correr tests
pytest                    # Todos los tests
pytest tests/            # Solo carpeta tests
pytest -v               # Con más detalles
pytest --cov            # Con cobertura


EJEMPLO 1: TEST UNITARIO (Sin dependencias)
=============================================

# test_schemas.py
from src.api.schemas.user_schemas import UserLoginDTO

def test_user_login_valid_email_and_password():
    \"\"\"Verifica que UserLoginDTO acepta email y password válidos\"\"\"
    dto = UserLoginDTO(
        email='user@example.com',
        password='ValidPass123'
    )
    
    errors = dto.validate()
    
    # Assert: verificar que no hay errores
    assert errors == {}

def test_user_login_invalid_email():
    \"\"\"Verifica que UserLoginDTO rechaza email inválido\"\"\"
    dto = UserLoginDTO(
        email='not-an-email',
        password='ValidPass123'
    )
    
    errors = dto.validate()
    
    # Assert: verificar que hay error en email
    assert 'email' in errors
    assert 'inválido' in errors['email'].lower()

def test_user_login_empty_password():
    \"\"\"Verifica que UserLoginDTO rechaza contraseña vacía\"\"\"
    dto = UserLoginDTO(
        email='user@example.com',
        password=''
    )
    
    errors = dto.validate()
    
    assert 'password' in errors


# Ejecutar
pytest test_schemas.py -v
# Resultado:
# test_schemas.py::test_user_login_valid_email_and_password PASSED
# test_schemas.py::test_user_login_invalid_email PASSED
# test_schemas.py::test_user_login_empty_password PASSED
# ========================= 3 passed in 0.15s =========================


EJEMPLO 2: TEST DE SERVICIO (Con mocks)
========================================

# test_auth_service.py
import pytest
from unittest.mock import Mock, patch
from src.api.services.auth_service import AuthService
from src.api.models import User

def test_verify_password_correct():
    \"\"\"Verifica que verify_password devuelve True con contraseña correcta\"\"\"
    # Crear usuario mock
    user = Mock(spec=User)
    user.password_hash = b'hash_de_contrasena'
    
    # Mock de bcrypt.checkpw
    with patch('src.api.services.auth_service.bcrypt.checkpw') as mock_bcrypt:
        mock_bcrypt.return_value = True
        
        # Ejecutar
        result = AuthService.verify_password(user, 'mypassword')
        
        # Verificar
        assert result == True
        mock_bcrypt.assert_called_once()

def test_verify_password_incorrect():
    \"\"\"Verifica que verify_password devuelve False con contraseña incorrecta\"\"\"
    user = Mock(spec=User)
    user.password_hash = b'hash_de_contrasena'
    
    with patch('src.api.services.auth_service.bcrypt.checkpw') as mock_bcrypt:
        mock_bcrypt.return_value = False
        
        result = AuthService.verify_password(user, 'wrongpassword')
        
        assert result == False


# Ejecutar
pytest test_auth_service.py::test_verify_password_correct -v
# PASSED


EJEMPLO 3: TEST DE RUTA HTTP (Integración)
===========================================

# conftest.py - Configuración compartida
import pytest
from src.app import create_app
from src.api.models import db

@pytest.fixture
def app():
    \"\"\"Crea app Flask para tests\"\"\"
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    \"\"\"Cliente HTTP para hacer peticiones\"\"\"
    return app.test_client()

@pytest.fixture
def runner(app):
    \"\"\"Para ejecutar comandos CLI\"\"\"
    return app.test_cli_runner()


# test_auth_routes.py
import json

def test_register_user_success(client):
    \"\"\"Verifica que POST /api/auth/register/user crea usuario\"\"\"
    
    # Datos de prueba
    user_data = {
        'email': 'newuser@example.com',
        'password': 'ValidPass123',
        'name': 'Juan',
        'lastname': 'Pérez'
    }
    
    # Hacer petición
    response = client.post(
        '/api/auth/register/user',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    
    # Verificar respuesta
    assert response.status_code == 201  # Created
    data = json.loads(response.data)
    assert data['user']['email'] == 'newuser@example.com'
    assert 'access_token' in data
    assert 'refresh_token' in data

def test_register_user_email_already_exists(client):
    \"\"\"Verifica que no se puede registrar con email existente\"\"\"
    
    # Registrar primer usuario
    client.post(
        '/api/auth/register/user',
        data=json.dumps({
            'email': 'user@example.com',
            'password': 'ValidPass123',
            'name': 'Juan',
            'lastname': 'Pérez'
        }),
        content_type='application/json'
    )
    
    # Intentar registrar otro con el mismo email
    response = client.post(
        '/api/auth/register/user',
        data=json.dumps({
            'email': 'user@example.com',  # Email duplicado
            'password': 'DifferentPass123',
            'name': 'Carlos',
            'lastname': 'López'
        }),
        content_type='application/json'
    )
    
    # Debe fallar
    assert response.status_code == 409  # Conflict

def test_login_success(client):
    \"\"\"Verifica que POST /api/auth/login funciona\"\"\"
    
    # Registrar usuario primero
    client.post(
        '/api/auth/register/user',
        data=json.dumps({
            'email': 'user@example.com',
            'password': 'ValidPass123',
            'name': 'Juan',
            'lastname': 'Pérez'
        }),
        content_type='application/json'
    )
    
    # Logear
    response = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'user@example.com',
            'password': 'ValidPass123'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data

def test_login_invalid_credentials(client):
    \"\"\"Verifica que login falla con credenciales inválidas\"\"\"
    
    response = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'nonexistent@example.com',
            'password': 'AnyPassword'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 404  # Not found


# Ejecutar
pytest test_auth_routes.py -v
# test_auth_routes.py::test_register_user_success PASSED
# test_auth_routes.py::test_register_user_email_already_exists PASSED
# test_auth_routes.py::test_login_success PASSED
# test_auth_routes.py::test_login_invalid_credentials PASSED
# ========================= 4 passed in 0.45s =========================


MEJOR PRÁCTICA: AAA (Arrange, Act, Assert)
===========================================

def test_example():
    # ARRANGE: Preparar datos y contexto
    user_data = {'email': 'test@example.com', 'password': 'Pass123'}
    
    # ACT: Ejecutar la acción
    dto = UserLoginDTO(**user_data)
    errors = dto.validate()
    
    # ASSERT: Verificar resultado
    assert errors == {}


COVERAGE: ¿Cuánto código está testado?
=======================================

# Ejecutar con coverage
pytest --cov=src/api --cov-report=html

# Ver reporte
open htmlcov/index.html

# Ejemplo output:
# Name          Stmts   Miss  Cover
# ────────────────────────────────────
# auth.py         50      5    90%
# schemas.py      30      2    93%
# services.py    100     20    80%
# ────────────────────────────────────
# TOTAL          300     40    86%

# Objetivo: 80%+ coverage (no necesita ser 100%)


MARKERS: Ejecutar tipos de tests
=================================

# Agregar a conftest.py
pytest.ini

# test_example.py
@pytest.mark.unit
def test_verify_password():
    pass

@pytest.mark.integration
def test_register_user_http():
    pass

# Ejecutar
pytest -m unit         # Solo tests unitarios
pytest -m integration  # Solo tests de integración
pytest -m \"not integration\"  # Todo menos integración


CHECKLIST PARA TESTS
====================

✅ Cada función importante tiene al menos 1 test
✅ Tests cubren casos positivos Y negativos
✅ Tests son independientes (no se afectan mutuamente)
✅ Usar nombres claros: test_<función>_<caso>
✅ Usar fixtures para código repetido
✅ Usar mocks para dependencias externas
✅ Tests deben ser rápidos (< 1 segundo cada uno)
✅ Coverage >= 80%
✅ Todos los tests pasan antes de hacer commit
✅ Tests en CI/CD (ejecutarse automáticamente)


COMANDOS ÚTILES
===============

pytest                          # Correr todos
pytest -v                       # Verbose (más info)
pytest -x                       # Parar en primer error
pytest --lf                     # Last failed (último que falló)
pytest tests/test_auth.py       # Un archivo específico
pytest tests/test_auth.py::test_login_success  # Un test específico
pytest -k \"login\"              # Tests que contengan \"login\"
pytest --pdb                    # Debugger en error
pytest --cov --cov-report=term-missing  # Coverage detallado


NEXT STEPS
==========

1. Crear conftest.py con fixtures
2. Crear test_schemas.py para validación
3. Crear tests/unit/ para servicios
4. Crear tests/integration/ para rutas HTTP
5. Configurar pytest.ini
6. Agregar tests a GitHub Actions (CI/CD)
7. Mantener coverage >= 80%

================================================================================
"""
