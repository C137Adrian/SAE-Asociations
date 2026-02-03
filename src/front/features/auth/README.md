# Feature: Auth

Esta carpeta contendrá todo lo relativo a autenticación (páginas, componentes y servicios).

Estructura sugerida:

- features/auth/
  - components/        # Componentes específicos de auth (LoginForm.jsx, RegisterForm.jsx)
  - pages/             # Páginas: Login.jsx, Register.jsx
  - hooks/             # Hooks específicos de auth (useAuth)
  - services/          # Lógica para llamadas al backend (auth.api.js)

Pasos para migrar:
1. Mover `src/front/pages/Login.jsx` a `features/auth/pages/Login.jsx`.
2. Mover componentes relacionados a `features/auth/components/`.
3. Actualizar imports en `src/front/routes` o `main.jsx`.
4. Ejecutar la app y corregir imports rotos.
