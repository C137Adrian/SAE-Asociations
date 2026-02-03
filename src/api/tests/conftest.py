"""
conftest.py - Configuración centralizada para pytest

Este archivo contiene:
- Fixtures compartidas (datos reutilizables)
- Configuración de la app de prueba
- Configuración de base de datos temporal
- Hooks de pytest

Se ejecuta automáticamente antes de los tests.
"""

import pytest
import sys
import os
from pathlib import Path

# Agregar src al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.app import app as flask_app
from src.api.models import db, User, Association


class Config:
    """Configuración para tests"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "test-secret-key-for-testing-only"
    SECRET_KEY = "test-secret-key-for-testing-only"
    # Desactivar validaciones que podrían bloquear tests
    WTF_CSRF_ENABLED = False


@pytest.fixture(scope="session")
def app():
    """
    Crea la aplicación Flask para tests.
    
    Scope: session = Se crea una vez para TODOS los tests
    
    Returns:
        Flask app con configuración de tests
    """
    # Configurar app para tests
    flask_app.config.from_object(Config)
    
    # Crear tablas en BD en memoria
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        # Cleanup después de todos los tests
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """
    Cliente HTTP para hacer peticiones a la app.
    
    Scope: function = Se crea para CADA test
    
    Returns:
        Test client de Flask
    """
    return app.test_client()


@pytest.fixture(scope="function")
def runner(app):
    """
    CLI runner para ejecutar comandos.
    
    Returns:
        Test CLI runner
    """
    return app.test_cli_runner()


@pytest.fixture(scope="function")
def db_session(app):
    """
    Sesión de BD limpia para cada test.
    
    Scope: function = BD se resetea entre tests
    
    Yields:
        Sesión de SQLAlchemy
    """
    with app.app_context():
        # Limpiar datos antes de test
        db.session.remove()
        db.drop_all()
        db.create_all()
        
        yield db
        
        # Limpiar datos después de test
        db.session.rollback()
        db.session.remove()


@pytest.fixture
def sample_user(db_session):
    """
    Crea un usuario de prueba.
    
    Returns:
        User object con datos de prueba
    """
    user = User(
        email='test@example.com',
        name='Test',
        lastname='User',
        phone='666666666'
    )
    # Nota: password se establece así en tests sin hashing
    user.password_hash = b'hashed_password'
    
    db_session.session.add(user)
    db_session.session.commit()
    return user


@pytest.fixture
def sample_association(db_session, sample_user):
    """
    Crea una asociación de prueba.
    
    Args:
        db_session: Sesión de BD
        sample_user: Usuario propietario de la asociación
    
    Returns:
        Association object con datos de prueba
    """
    association = Association(
        name='Test Association',
        description='Test Description',
        cif='A12345678',
        contact_email='assoc@example.com',
        phone='666666666',
        user_id=sample_user.id
    )
    db_session.session.add(association)
    db_session.session.commit()
    return association


@pytest.fixture
def auth_headers(client, sample_user):
    """
    Crea headers con token JWT válido.
    
    Esto permite hacer requests autenticadas en tests.
    
    Args:
        client: Test client
        sample_user: Usuario para autenticarse
    
    Returns:
        Dict con headers HTTP incluyendo Authorization
    """
    # En tests reales, generar un token JWT válido
    # Por ahora devolvemos estructura esperada
    token = "test_jwt_token"
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }


# Hooks de pytest para logs y reportes

def pytest_configure(config):
    """Se ejecuta al inicio de pytest"""
    # Agregar markers personalizados
    config.addinivalue_line(
        "markers", "unit: marca un test como unitario"
    )
    config.addinivalue_line(
        "markers", "integration: marca un test como integración"
    )
    config.addinivalue_line(
        "markers", "slow: marca un test como lento"
    )


def pytest_collection_modifyitems(config, items):
    """Se ejecuta después de recopilar tests"""
    for item in items:
        # Marcar automáticamente tests por ubicación
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        elif "unit" in item.nodeid:
            item.add_marker(pytest.mark.unit)


# Fixtures de uso común

@pytest.fixture
def json_headers():
    """Headers para peticiones JSON"""
    return {'Content-Type': 'application/json'}


@pytest.fixture
def admin_user(db_session):
    """Usuario con rol de admin (si lo tienes)"""
    user = User(
        email='admin@example.com',
        name='Admin',
        lastname='User',
        phone='666666666'
    )
    user.password_hash = b'hashed_password'
    user.is_admin = True  # Si existe este campo
    
    db_session.session.add(user)
    db_session.session.commit()
    return user
