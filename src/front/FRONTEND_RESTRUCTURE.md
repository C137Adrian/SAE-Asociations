# Reestructuración Frontend (Fase 3A / 3B)

Objetivo: reorganizar `src/front` en features/domains y crear una carpeta `shared/` para componentes reutilizables.

División de commits:
- Fase 3A (commit 1): Crear estructura por features y `shared/`, mover componentes que no rompan imports, crear componentes shared básicos.
- Fase 3B (commit 2): Implementar `ErrorBoundary.jsx`, `errorHandler.js`, migrar el resto de componentes y actualizar rutas para lazy-loading.

Plan de migración (pasos):
1. Crear carpetas de features: `auth`, `associations`, `events`, `donations`.
2. Crear carpeta `shared/components`, `shared/hooks`, `shared/utils`.
3. Copiar (no borrar aún) componentes a `shared/components` y ajustar imports gradualmente.
4. Ejecutar la app localmente y corregir imports uno a uno.
5. Una vez todo funcione, eliminar archivos antiguos y hacer commit final.

Cambios en esta fase 3C:

- Añadido `src/front/shared/components/index.jsx` para re-exportar componentes compartidos y simplificar imports.
- Rutas principales actualizadas para `React.lazy` + `Suspense` en `src/front/routes/routes.jsx` para habilitar code-splitting y carga bajo demanda de páginas (Home, Login, Events, Associations, Donations, etc.).

Notas:

- Después de estos cambios, la primera carga del bundle se hace más ligera y las páginas se descargan cuando el usuario navega a ellas.
- Mantén `src/front/components` con los archivos originales hasta que completes las migraciones de imports; los re-exports permiten usar `src/front/shared/components` gradualmente.

Mapping sugerido (archivo actual -> nuevo lugar):
- `src/front/pages/Login.jsx` -> `src/front/features/auth/pages/Login.jsx`
- `src/front/pages/RegisterUser.jsx` -> `src/front/features/auth/pages/RegisterUser.jsx`
- `src/front/components/ImageUploader.jsx` -> `src/front/shared/components/ImageUploader.jsx` (si es reutilizable)
- `src/front/components/AssociationCard.jsx` -> `src/front/features/associations/components/AssociationCard.jsx`
- `src/front/components/EventCard.jsx` -> `src/front/features/events/components/EventCard.jsx`
- `src/front/components/DonateForm.jsx` -> `src/front/features/donations/pages/DonateForm.jsx`

Recomendación técnica:
- Hacer commits pequeños y frecuentes: primero crear estructura (este commit), luego mover 1-3 archivos y ejecutar tests/manual checks, repetir.
- Usar `git mv` para preservar historial cuando muevas archivos definitivamente.

Ejemplo de comandos para mover con historial:
```bash
# Mover Login.jsx a la nueva carpeta
git mv src/front/pages/Login.jsx src/front/features/auth/pages/Login.jsx
# Corregir imports
# Revisar y testear la app
npm run dev
# Commit
git add -A
git commit -m "refactor(front): Move Login page to features/auth"
```


Notas sobre imports:
- Usa imports relativos desde la nueva ubicación o rutas absolutas con alias si lo tienes configurado.
- Si usas Vite, puedes configurar `vite.config.js` para añadir alias (ej: `@/` -> `src/front`).


Próximos pasos que puedo ejecutar ahora si confirmas:
- Mover 1-3 componentes pequeños como `ImageUploader.jsx`, `BackendURL.jsx` a `shared/components` y actualizar imports.
- Crear `features/*/components` vacíos y `index.jsx` para agrupación.

Confirma si quieres que comience moviendo archivos reales (haré `git mv` y actualizaré imports donde sea seguro).