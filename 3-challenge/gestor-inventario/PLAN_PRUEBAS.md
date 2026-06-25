# Plan de Pruebas -- Gestor de Inventario

## 1. Objetivo

Validar la aplicacion gestor-inventario (SUT) cubriendo contrato de API, funcionalidad, integridad de datos y fallos de integracion.

## 2. Alcance

### Endpoints bajo prueba:
| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | /api/health | Estado del servicio |
| GET | /api/suppliers | Lista de proveedores activos |
| GET | /api/products | Lista de productos activos |
| GET | /api/products/{id} | Detalle de producto |
| POST | /api/products | Crear producto |
| POST | /api/stock/movimiento | Movimiento IN/OUT |
| GET | /api/stock/alerts | Productos en alerta |
| GET | /api/movements | Historial de movimientos |

### Fuera de alcance:
- Pruebas de rendimiento / carga
- Seguridad (autenticacion, autorizacion)
- UI/E2E con Playwright (pendiente por tiempo)

## 3. Criterios de Aceptacion

- Todos los endpoints retornan status codes correctos (200, 201, 400, 404, 409, 422, 503)
- Los campos de respuesta cumplen el contrato definido
- Stock se actualiza correctamente tras movimientos IN/OUT
- No se permite stock negativo (bug detectado, comportamiento actual lo permite)
- Movimientos OUT no deberian depender del servicio de alertas (bug detectado)

## 4. Riesgos

| Riesgo | Mitigacion |
|--------|------------|
| ALERTS_FAIL=1 en servidor | Tests adaptados para aceptar 503 |
| Base de datos compartida | Reset de DB entre corridas |
| Sin Playwright para E2E | Priorizar cobertura API |

## 5. Criterios de Salida

- Suite API ejecutable con `python -m pytest tests/ -v`
- 100% de tests pasando
- Defectos documentados con severidad y pasos de reproduccion
- SOUL.md actualizado con hallazgos
