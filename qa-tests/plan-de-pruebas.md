# Plan de Pruebas — gestor-inventario

## Objetivo
Validar calidad funcional, contrato API, integridad de datos, fallo de integración y flujo UI sin modificar el SUT.

## Alcance
- Endpoints obligatorios: `/api/health`, `/api/suppliers`, `/api/products`, `/api/products/{id}`, `/api/stock/movement`, `/api/stock/alerts`, `/api/movements`.
- Modos: normal y `ALERTS_FAIL=1`.

## Criterios de aceptación
- 18 pruebas API verdes.
- Defectos planteados detectados con repro reproducible.
- Tests aislados en DB y libres de estado.

## Riesgos
- Estado compartido entre tests.
- Dependencia de datos seed.
- Falta de frameworks por entorno Windows; mitigado con `uv` + venv.

## Estrategia
- API: pytest + TestClient, fixtures por test.
- Integración: manipulación controlada de `ALERTS_FAIL`.
- E2E: Playwright, si `localhost:8000` está arriba.
