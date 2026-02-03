# SAE Associations - Web Application

Plataforma web profesional para gestionar asociaciones, voluntarios, eventos y donaciones.

Construida con:
- **Frontend**: React 18 + React Router + Vite + Bootstrap
- **Backend**: Flask + SQLAlchemy + JWT + Stripe + SendGrid
- **Base de datos**: PostgreSQL (producción) / SQLite (desarrollo)
- **DevOps**: Render.com, Docker

## Características Principales

- ✅ Autenticación con JWT
- ✅ Gestión de asociaciones y eventos
- ✅ Sistema de donaciones con Stripe
- ✅ Emails con SendGrid
- ✅ Upload de imágenes con Cloudinary
- ✅ Ratings y reseñas
- ✅ Panel administrativo
- ✅ Tests automáticos (backend)
- ✅ Code-splitting y lazy-loading (frontend)
- ✅ Error Boundary global
- ✅ Linting y formateo automático

## Instalación Rápida

### Requisitos Previos

- Node.js >= 20.0.0
- Python >= 3.10
- PostgreSQL (producción) o SQLite (desarrollo)

### Backend Setup

```bash
# 1. Instalar dependencias Python
pip install -r requirements.txt

# 2. (Opcional) Instalar herramientas de desarrollo
pip install -r requirements-dev.txt

# 3. Crear archivo .env
cp .env.example .env

# 4. Editar .env y llenar variables secretas
# - DATABASE_URL
# - SECRET_KEY, JWT_SECRET_KEY
# - STRIPE_SECRET_KEY, STRIPE_PUBLIC_KEY
# - SENDGRID_API_KEY, SENDGRID_SENDER_EMAIL
# - VITE_CLOUDINARY_CLOUD_NAME, VITE_CLOUDINARY_UPLOAD_PRESET
# - VITE_BACKEND_URL

# 5. Crear base de datos
flask db upgrade

# 6. Ejecutar servidor
python src/app.py
# o con Flask CLI
flask run
```

El backend estará disponible en `http://localhost:3001`

### Frontend Setup

```bash
# 1. Instalar dependencias Node
npm install

# 2. Crear archivo .env (copiado del .env.example)
cp .env.example .env

# 3. Llenar VITE_BACKEND_URL (debe coincidir con backend)
# VITE_BACKEND_URL=http://localhost:3001

# 4. Ejecutar servidor de desarrollo
npm run dev
```

El frontend estará disponible en `http://localhost:5173`

---

## Estructura del Proyecto

### Backend (`src/api/`)

```
src/api/
├── app.py                       # Aplicación Flask principal
├── models/                      # Modelos SQLAlchemy
│   ├── user.py
│   ├── association.py
│   ├── events.py
│   ├── donation.py
│   ├── rating.py
│   └── event_volunteers.py
├── routes/                      # Blueprints de rutas
│   ├── __init__.py             # Carga todos los blueprints
│   ├── auth_routes.py
│   ├── association_routes.py
│   ├── events_routes.py
│   ├── donation_routes.py
│   ├── rating_routes.py
│   └── [más rutas]
├── controllers/                 # Lógica de negocio
│   ├── auth_controller.py
│   ├── association_controller.py
│   └── rating_controller.py
├── services/                    # Servicios e integraciones
│   ├── auth_service.py
│   ├── donation_service.py      # Integración Stripe
│   ├── email_service.py         # Integración SendGrid
│   └── rating_service.py
├── schemas/                     # Validación de datos (DTOs)
│   ├── user_schema.py
│   ├── association_schema.py
│   └── event_schema.py
├── tests/                       # Tests automáticos
│   ├── conftest.py             # Configuración pytest + fixtures
│   ├── unit/                   # Tests unitarios
│   ├── integration/            # Tests de integración
│   └── fixtures/               # Datos de prueba
├── BACKEND_STRUCTURE.md        # Guía de arquitectura backend
├── SCHEMA_AND_DTO_GUIDE.md     # Guía de validación de datos
└── TESTING_GUIDE.md            # Guía de testing
```

**Archivos de Configuración:**
- `pyproject.toml`: Configuración de herramientas Python (black, isort, pytest, mypy)
- `pytest.ini`: Configuración de pytest

### Frontend (`src/front/`)

```
src/front/
├── main.jsx                     # Punto de entrada (con ErrorBoundary)
├── features/                    # Características organizadas por dominio
│   ├── auth/                   # Autenticación
│   ├── associations/           # Gestión de asociaciones
│   ├── events/                 # Gestión de eventos
│   ├── donations/              # Sistema de donaciones
│   └── ratings/                # Sistema de ratings
├── shared/                      # Componentes y utilidades compartidas
│   ├── components/
│   │   ├── Button.jsx
│   │   ├── ImageUploader.jsx
│   │   ├── NotificationModal.jsx
│   │   ├── ErrorBoundary.jsx
│   │   └── index.jsx           # Re-exports para importes limpios
│   ├── hooks/                  # Hooks reutilizables
│   ├── utils/                  # Utilidades (errorHandler.js)
│   └── styles/                 # Estilos globales
├── components/                  # Componentes (legacy, en migración)
├── pages/                       # Páginas principales (legacy)
├── routes/                      # Configuración de rutas (con lazy-loading)
├── context/                     # Context API (AppContext)
├── store/                       # Estado global
├── styles/                      # Estilos CSS
└── FRONTEND_RESTRUCTURE.md     # Guía de reestructuración
```

**Archivos de Configuración:**
- `.eslintrc.json`: Reglas de linting JavaScript/React
- `.eslintignore`: Archivos a ignorar en ESLint
- `.prettierrc.json`: Formateo automático de código
- `vite.config.js`: Configuración de Vite

---

## Guías de Desarrollo

### Backend

#### Cómo crear una nueva ruta

Lee [src/api/BACKEND_STRUCTURE.md](src/api/BACKEND_STRUCTURE.md) para:
- Entender la separación de responsabilidades
- Ver ejemplo completo de ruta → controller → service
- Buenas prácticas de arquitectura

#### Cómo validar datos (DTOs)

Lee [src/api/SCHEMA_AND_DTO_GUIDE.md](src/api/SCHEMA_AND_DTO_GUIDE.md) para:
- Crear DTOs con dataclasses
- Reutilizar validación en múltiples endpoints
- Ejemplos prácticos

#### Cómo escribir tests

Lee [src/api/TESTING_GUIDE.md](src/api/TESTING_GUIDE.md) para:
- Tests unitarios vs integración
- Fixtures compartidas
- Ejecutar tests con coverage

**Comandos útiles:**

```bash
# Ejecutar todos los tests
pytest

# Ejecutar con coverage
pytest --cov=src/api --cov-report=html

# Tests específicos
pytest src/api/tests/unit/test_schemas.py -v

# Tests de una feature
pytest -m unit

# Ver reporte de coverage
open htmlcov/index.html
```

### Frontend

#### Cómo crear un componente compartido

1. Crear en `src/front/shared/components/MiComponente.jsx`
2. Exportar en `src/front/shared/components/index.jsx`
3. Importar desde cualquier parte: `import { MiComponente } from '../shared/components'`

#### Cómo organizar componentes por feature

Lee [src/front/FRONTEND_RESTRUCTURE.md](src/front/FRONTEND_RESTRUCTURE.md) para:
- Estructura recomendada de features
- Cómo migrar componentes sin romper la app
- Lazy-loading de rutas

#### Error Boundary

El frontend envuelve toda la app con `ErrorBoundary` (en `main.jsx`):
- Captura errores no manejados
- Llama a `errorHandler.js` para logging centralizado
- Muestra UI amigable al usuario

Personaliza `src/front/shared/utils/errorHandler.js` para enviar errores a servicio remoto.

#### Code-Splitting con Lazy-Loading

Las rutas principales cargan con `React.lazy` + `Suspense`:
- Primera carga del bundle más ligera
- Páginas se descargan bajo demanda
- Fallback personalizado mientras carga

Verifica [src/front/routes/routes.jsx](src/front/routes/routes.jsx)

**Comandos útiles:**

```bash
# Desarrollo con HMR
npm run dev

# Build para producción
npm run build

# Preview de build
npm run preview

# Linting
npm run lint

# Formateo automático (si configuras)
npx prettier --write src/

# Análisis de bundle
npm run build -- --report
```

---

## Comandos Disponibles

### Backend

```bash
pipenv install              # Instalar dependencias
pipenv run start            # Ejecutar servidor
pipenv run migrate          # Crear migración
pipenv run upgrade          # Aplicar migraciones
pipenv run downgrade        # Deshacer última migración
pipenv run insert-test-data # Insertar datos de prueba
pytest                      # Ejecutar tests
black src/                  # Formatear código
isort src/                  # Ordenar imports
```

### Frontend

```bash
npm install                 # Instalar dependencias
npm run dev                 # Servidor desarrollo
npm run build               # Build producción
npm run preview             # Preview de build
npm run lint                # ESLint check
```

---

## Variables de Entorno

Consulta `.env.example` para documentación completa:

**Críticas en desarrollo:**
- `DATABASE_URL`: Conexión a BD
- `VITE_BACKEND_URL`: URL del backend

**Críticas en producción:**
- `SECRET_KEY`, `JWT_SECRET_KEY`: Claves aleatorias fuertes
- `STRIPE_SECRET_KEY`: Clave secreta de Stripe (pk_live_)
- `SENDGRID_API_KEY`: Clave de SendGrid
- `FLASK_DEBUG`: Siempre 0 en producción

---

## Contribución

### Flujo de trabajo (Git)

1. **Branch**: Crear rama desde `develop`
   ```bash
   git checkout -b feature/mi-feature
   git checkout -b fix/mi-fix
   ```

2. **Commits**: Mensajes claros y estructurados
   ```bash
   git commit -m "feat(backend): add user validation schema"
   git commit -m "fix(frontend): correct lazy-loading fallback"
   git commit -m "refactor(api): reorganize routes with blueprints"
   git commit -m "docs(readme): update installation guide"
   ```

3. **Push y Pull Request**: Enviar a rama develop
   ```bash
   git push origin mi-rama
   # Crear PR en GitHub → describe cambios → review
   ```

4. **Merge**: Una vez aprobada, merge a `develop` y luego a `main`

### Estándares de Código

**Backend (Python):**
- Usar `black` para formateo: `black src/api`
- Usar `isort` para imports: `isort src/api`
- Mantener coverage >= 80%: `pytest --cov`

**Frontend (JavaScript/React):**
- ESLint valida automáticamente
- Prettier formatea en save (si está configurado)
- Componentes funcionales con hooks
- PropTypes o TypeScript (próximas versiones)

### Testing

- **Backend**: Agregar tests en `src/api/tests/`
- **Frontend**: (Próximas fases) Tests con Vitest

---

## Deployment

### Render.com

1. Conectar repositorio GitHub
2. Crear servicio Web (Flask backend)
3. Crear servicio Static (React frontend)
4. Configurar variables de entorno (production)
5. Deploy automático en cada push a `main`

[Documentación oficial de Render](https://docs.render.com)

---

## Estructura de Directorios Completa

```
SAE-Associations/
├── .env.example             # Template de variables de entorno
├── .eslintrc.json           # Configuración ESLint
├── .prettierrc.json         # Configuración Prettier
├── pytest.ini               # Configuración pytest
├── pyproject.toml           # Herramientas Python (black, isort)
├── requirements.txt         # Dependencias backend
├── requirements-dev.txt     # Herramientas desarrollo backend
├── package.json             # Dependencias frontend
├── vite.config.js           # Configuración Vite
├── src/
│   ├── api/                 # Backend Flask
│   │   ├── *.py             # Modelos, rutas, servicios
│   │   ├── tests/           # Tests con pytest
│   │   ├── BACKEND_STRUCTURE.md
│   │   ├── SCHEMA_AND_DTO_GUIDE.md
│   │   └── TESTING_GUIDE.md
│   └── front/               # Frontend React
│       ├── main.jsx         # Entrada con ErrorBoundary
│       ├── features/        # Componentes por dominio
│       ├── shared/          # Componentes compartidos
│       ├── routes/          # Rutas con lazy-loading
│       └── FRONTEND_RESTRUCTURE.md
├── migrations/              # Migraciones de BD (Alembic)
├── docs/                    # Documentación adicional
├── README.md                # Este archivo
└── [otros]
```

---

## Soporte y Recursos

## Soporte y Recursos

- 📚 [Documentación Flask](https://flask.palletsprojects.com/)
- 📚 [Documentación React](https://react.dev)
- 📚 [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- 📚 [Vite](https://vitejs.dev/)
- 🎓 [4Geeks Academy](https://4geeksacademy.com)

---

## Licencia

ISC

## Autores

- **Alejandro Sanchez** - Autor principal ([alesanchezr.com](http://alesanchezr.com))
- **Ignacio Cordoba** - Contribuidor

Más información: [Github 4GeeksAcademy](https://github.com/4geeksacademy/)

