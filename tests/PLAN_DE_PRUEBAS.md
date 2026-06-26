# Plan de Pruebas - Track QA

## Alcance y Objetivo

Este documento define la estrategia de pruebas para el SUT `gestor-inventario`, una aplicación FastAPI para gestión de inventario con integración de alertas de stock.

**Objetivo:** Validar la calidad del SUT identificando defectos funcionales, problemas de integración y fallos de datos.

## Dimensiones de Prueba

### 1. API Contract Tests
- Validación de códigos de estado HTTP (200, 201, 400, 404, 409, 503)
- Estructura y tipos de datos en respuestas JSON
- Mensajes de error consistentes

### 2. Functional Tests - Happy Path
- Endpoints principales funcionan correctamente con datos válidos
- Creación de productos con validaciones básicas (SKU único, proveedor existente)

### 3. Defect Tests (Identificados en CLAUDE.md)
- **Bug #1:** Stock negativo permitido (OUT qty > stock)
- **Bug #2:** Cantidad decimal aceptada (qty: float en lugar de int)
- **Bug #3:** min_stock negativo permitido
- **Bug #4:** cost_cents negativo permitido

### 4. Integration Failure Tests
- Simulación de caída del servicio de alertas (ALERTS_FAIL=1)
- Verificación de respuesta 503 Service Unavailable

### 5. Data Integrity Tests
- Stock se incrementa/decrementa correctamente después de movimientos
- Persistencia de datos en SQLite

### 6. UI/E2E Tests
- Carga de productos en la interfaz
- Registro de movimientos desde el frontend
- Consulta de alertas desde la UI

## Herramientas

| Tipo | Herramienta | Justificación |
|------|-------------|---------------|
| API Tests | pytest + httpx | Testing asíncrono de FastAPI con ASGITransport |
| E2E Tests | Playwright | Automatización de navegador para flujos UI |
| Database | SQLite integrado | Testing aislado con base de datos temporal |

## Criterios de Aceptación

- Todos los endpoints devuelven códigos de estado apropiados
- Los defectos críticos (Bugs #1 y #2) están identificados y reproducidos
- La cobertura incluye happy path, edge cases y negative cases
- Los tests son idempotentes y pueden ejecutarse en paralelo

## Riesgos

| Riesgo | Mitigación |
|--------|------------|
| Base de datos compartida en tests | Usar DB_PATH temporal único por ejecución |
| Puertos ocupados | Usar puertos diferentes para API (8000) y E2E (8001) |
| Estado entre tests | Fixture de setup/teardown que reinicia DB |

## Resultados Esperados

- 16 tests API + 4 tests E2E = 20 tests totales
- Detección confirmada de los 4 defects conocidos
- Reporte de defectos con severidad y pasos de reproducción