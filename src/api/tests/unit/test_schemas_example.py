"""
test_schemas.py - Tests para validación de DTOs

Este archivo muestra ejemplos de cómo testear la validación de datos.
Es un archivo TEMPLATE que puedes copiar y adaptar.

Para ejecutar:
  pytest test_schemas.py -v
"""

import pytest
from src.api.schemas.user_schema import validate_email, validate_user_data


class TestEmailValidation:
    """Tests para validar direcciones de email"""
    
    def test_valid_email_format(self):
        """✅ Email válido debe devolver True"""
        assert validate_email('user@example.com') == True
        assert validate_email('test.user+tag@domain.co.uk') == True
        assert validate_email('a@b.co') == True
    
    def test_invalid_email_no_at_symbol(self):
        """❌ Email sin @ debe devolver False"""
        assert validate_email('userexample.com') == False
    
    def test_invalid_email_no_domain(self):
        """❌ Email sin dominio debe devolver False"""
        assert validate_email('user@') == False
    
    def test_invalid_email_no_tld(self):
        """❌ Email sin extensión debe devolver False"""
        assert validate_email('user@domain') == False
    
    def test_empty_email(self):
        """❌ Email vacío debe devolver False"""
        assert validate_email('') == False


class TestUserRegistrationValidation:
    """Tests para la validación de datos de registro de usuario"""
    
    def test_valid_user_registration(self):
        """✅ Datos válidos no devuelven errores"""
        valid_data = {
            'email': 'user@example.com',
            'password': 'ValidPassword123',
            'name': 'Juan',
            'lastname': 'Pérez',
            'phone': '666666666'
        }
        
        errors = validate_user_data(valid_data)
        assert errors is None or errors == {}
    
    def test_missing_email(self):
        """❌ Falta email"""
        data = {
            'password': 'ValidPassword123',
            'name': 'Juan',
            'lastname': 'Pérez'
        }
        
        errors = validate_user_data(data)
        assert errors is not None
        assert 'email' in errors
    
    def test_invalid_email_format(self):
        """❌ Email con formato inválido"""
        data = {
            'email': 'not-an-email',
            'password': 'ValidPassword123',
            'name': 'Juan',
            'lastname': 'Pérez'
        }
        
        errors = validate_user_data(data)
        assert errors is not None
        assert 'email' in errors
    
    def test_short_password(self):
        """❌ Contraseña muy corta"""
        data = {
            'email': 'user@example.com',
            'password': 'short',  # Menos de 8 caracteres
            'name': 'Juan',
            'lastname': 'Pérez'
        }
        
        errors = validate_user_data(data)
        assert errors is not None
        assert 'password' in errors
    
    def test_password_no_numbers(self):
        """❌ Contraseña sin números"""
        data = {
            'email': 'user@example.com',
            'password': 'NoNumbersHere',  # Sin dígitos
            'name': 'Juan',
            'lastname': 'Pérez'
        }
        
        errors = validate_user_data(data)
        assert errors is not None
        assert 'password' in errors
    
    def test_password_no_letters(self):
        """❌ Contraseña sin letras"""
        data = {
            'email': 'user@example.com',
            'password': '12345678',  # Sin letras
            'name': 'Juan',
            'lastname': 'Pérez'
        }
        
        errors = validate_user_data(data)
        assert errors is not None
        assert 'password' in errors
    
    def test_missing_name(self):
        """❌ Falta nombre"""
        data = {
            'email': 'user@example.com',
            'password': 'ValidPassword123',
            'lastname': 'Pérez'
        }
        
        errors = validate_user_data(data)
        assert errors is not None
        assert 'name' in errors
    
    def test_missing_lastname(self):
        """❌ Falta apellido"""
        data = {
            'email': 'user@example.com',
            'password': 'ValidPassword123',
            'name': 'Juan'
        }
        
        errors = validate_user_data(data)
        assert errors is not None
        assert 'lastname' in errors
    
    def test_name_too_long(self):
        """❌ Nombre excede límite de caracteres"""
        data = {
            'email': 'user@example.com',
            'password': 'ValidPassword123',
            'name': 'A' * 101,  # 101 caracteres (máximo es 100)
            'lastname': 'Pérez'
        }
        
        errors = validate_user_data(data)
        assert errors is not None
        assert 'name' in errors
    
    def test_optional_phone_not_required(self):
        """✅ Teléfono es opcional"""
        data = {
            'email': 'user@example.com',
            'password': 'ValidPassword123',
            'name': 'Juan',
            'lastname': 'Pérez'
            # Sin phone
        }
        
        errors = validate_user_data(data)
        assert errors is None or 'phone' not in errors


# Fixtures personalizadas para estos tests (si las necesitas)

@pytest.fixture
def valid_user_data():
    """Datos válidos de usuario para reutilizar"""
    return {
        'email': 'test@example.com',
        'password': 'ValidPassword123',
        'name': 'Test',
        'lastname': 'User',
        'phone': '666666666'
    }


# Ejemplo usando fixture
class TestWithFixtures:
    """Ejemplo usando fixtures"""
    
    def test_valid_user_with_fixture(self, valid_user_data):
        """✅ Usar fixture para datos válidos"""
        errors = validate_user_data(valid_user_data)
        assert errors is None or errors == {}
    
    def test_modify_fixture(self, valid_user_data):
        """✅ Modificar fixture para test específico"""
        # Cambiar email
        valid_user_data['email'] = 'invalid-email'
        
        errors = validate_user_data(valid_user_data)
        assert 'email' in errors


# Parametrización - Ejecutar el mismo test con múltiples valores

@pytest.mark.parametrize("email,should_be_valid", [
    ('user@example.com', True),
    ('test.user@domain.co.uk', True),
    ('a@b.co', True),
    ('invalid-email', False),
    ('user@', False),
    ('@domain.com', False),
    ('', False),
])
def test_email_parametrized(email, should_be_valid):
    """Test email con múltiples casos"""
    result = validate_email(email)
    assert result == should_be_valid


# Ejecutar: pytest test_schemas.py::test_email_parametrized -v
# Output:
# test_schemas.py::test_email_parametrized[user@example.com-True] PASSED
# test_schemas.py::test_email_parametrized[test.user@domain.co.uk-True] PASSED
# test_schemas.py::test_email_parametrized[invalid-email-False] PASSED
# ... más tests
