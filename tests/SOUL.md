# SOUL.md - Track QA Reto AI-First Fase 1

## Proceso de Testing

### Herramientas Utilizadas
- **pytest + httpx**: Tests API con ASGITransport para testing sin servidor real
- **Playwright**: Tests E2E con navegador Chromium headless
- **Python 3.11.15**: Entorno de ejecución

### Decisiones Técnicas

1. **Testing sin servidor**: Usé `ASGITransport` de httpx para evitar necesidad de levantar el servidor real en tests API
2. **Database isolation**: Cada test usa `DB_PATH=/tmp/test_inventario.db` para aislamiento total
3. **E2E real server**: Los tests E2E levantan el servidor en puerto 8001 con su propia base de datos

## Hallazgos (Defects)

### Defect #1 - Stock Negativo - CRÍTICO
- **Severidad**: Alta
- **Endpoint**: POST /api/stock/movement (type=OUT)
- **Descripción**: La API permite registrar movimientos de salida con cantidad mayor al stock disponible
- **Impacto**: El stock puede volverse negativo, violación de invariante de negocio
- **Reproducción**: 
  ```python
  movement = {"product_id": 1, "type": "OUT", "qty": 99999}
  # Retorna 201, stock pasa de 50 a -99949
  ```
- **Evidencia**: Test `test_defect_negative_stock_allowed` pasa confirmando el defecto

### Defect #2 - Cantidad Decimal - CRÍTICO
- **Severidad**: Media
- **Endpoint**: POST /api/stock/movement
- **Descripción**: El campo `qty` acepta valores decimales (float) cuando debería ser entero
- **Impacto**: La columna SQLite está definida como REAL, lo que permite decimales
- **Reproducción**:
  ```python
  movement = {"product_id": 1, "type": "IN", "qty": 2.5}
  # Retorna 201, qty almacenado como 2.5
  ```
- **Evidencia**: Test `test_defect_decimal_quantity_accepted` confirma

### Defect #3 - min_stock Negativo - MEDIO
- **Severidad**: Media
- **Endpoint**: POST /api/products
- **Descripción**: Se permite crear productos con `min_stock` negativo
- **Impacto**: Las alertas nunca se dispararán para ese producto (stock <= -1 es siempre falso para valores positivos)
- **Reproducción**:
  ```python
  product = {"name": "X", "sku": "X-1", "min_stock": -1, ...}
  # Retorna 201, min_stock = -1 almacenado
  ```
- **Evidencia**: Test `test_defect_negative_min_stock_accepted` confirma

### Defect #4 - cost_cents Negativo - MEDIO
- **Severidad**: Media
- **Endpoint**: POST /api/products  
- **Descripción**: Se permite crear productos con `cost_cents` negativo
- **Impacto**: Datos de costos inconsistentes, podría afectar reportes financieros
- **Reproducción**:
  ```python
  product = {"name": "X", "sku": "X-2", "cost_cents": -5000, ...}
  # Retorna 201, costo negativo almacenado
  ```
- **Evidencia**: Test `test_defect_negative_cost_accepted` confirma

### Defect #5 - ALERTS_FAIL Integration - ESPERADO
- **Severidad**: Funcional (comportamiento documentado)
- **Endpoints Afectados**: GET /api/stock/alerts, POST /api/stock/movement (type=OUT)
- **Descripción**: Cuando `ALERTS_FAIL=1`, los endpoints retornan 503
- **Nota**: Este es el comportamiento esperado para testing de fallos de integración

## Resumen de Tests

| Categoría | Tests | Estado |
|-----------|-------|--------|
| API Contract | 5 | ✓ Pasados |
| Functional Happy Path | 3 | ✓ Pasados |
| Defect Detection | 4 | ✓ Pasados (detectan bugs) |
| Integration Failure | 2 | ✓ Pasados |
| Data Integrity | 2 | ✓ Pasados |
| **Total API** | **16** | **100%** |

| Categoría E2E | Tests | Estado |
|---------------|-------|--------|
| UI Load | 1 | ✓ Pasado |
| Register Movement | 1 | ✓ Pasado |
| Check Alerts | 1 | ✓ Pasado |
| Defect Verification | 1 | ✓ Pasado |
| **Total E2E** | **4** | **100%** |

## Comandos de Ejecución

```bash
# Tests API
pytest tests/test_api.py -v

# Tests E2E  
pytest tests/test_e2e.py -v

# Todos los tests
pytest tests/ -v
```

## Fix Aplicado: ModuleNotFoundError

Los tests fallaban con `ModuleNotFoundError: No module named 'app'` porque el `conftest.py` intentaba hacer `import app` sin tener el directorio raíz en `sys.path`.

**Solución:** Se agregó `sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))` al inicio de `conftest.py`.

## Entorno de Ejecución

```bash
# Crear venv
python3.11 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt pytest pytest-asyncio httpx anyio playwright
playwright install chromium

# Ejecutar todos los tests
pytest tests/ -v
```

## Próximos Pasos

1. Agregar tests de edge case para qty=0, strings en campos numéricos
2. Tests de concurrencia con múltiples movimientos simultáneos
3. Reporte formal de defects con tickets para el equipo DEV (completado en tests/DEFECT_REPORT.md)