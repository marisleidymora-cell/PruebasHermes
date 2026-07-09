# Plan de pruebas — Gestor de Inventario (SUT Track QA)

## 1. Estrategia
- Enfoque API-first (contrato + errores) con pytest + FastAPI TestClient.
- Aislamiento por test mediante DB temporal por caso o fixture.
- Verificación post-despliegue del frontend estático.
- E2E deseable con Playwright sobre `localhost:8000`.

## 2. Alcance
### Incluido
- Health API.
- CRUD productos (`GET`, `POST`).
- Movimientos de stock (`POST /api/stock/movement`).
- Alertas de stock (`GET /api/stock/alerts`).
- Frontend estático (`/`).
- Contrato, códigos HTTP, mensajes y campos devueltos.

### Excluido
- Modificar el SUT en producción; solo se reportan hallazgos.
- Pruebas de carga / stress.

## 3. Riesgos
- Estado compartido entre tests si no se aísla la DB.
- Observabilidad limitada: no hay logs estructurados ni métricas.
- Dependencia de `ALERTS_FAIL` como toggle manual para simular fallos.
- Bugs funcionales conocidos pueden hacer ruido en validaciones comerciales.

## 4. Criterios de aceptación
- Suite API pasa al menos:
  - 100% de casos de contrato documentados.
  - 90%+ de casos negativos documentados.
- Casos E2E (si se incluyen):
  - Flujo happy path navegable.
  - Validaciones de formulario reflejadas en UI.
- Reporte de defectos generado con evidencia reproducible.
