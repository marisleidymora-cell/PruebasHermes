"""
Suite de contrato API para `gestor-inventario`.

Cobertura:
- Health check
- Listado de proveedores
- CRUD productos (list, detalle, 404, 201, 409 duplicado)
- Validaciones faltantes en productos (min_stock / cost_cents negativos)
- Listado de movimientos

Nota: usa la fixture `client` desde conftest.py, que apunta a BASE_URL.
"""
import uuid
import pytest


class TestHealth:
    """Verifica que el endpoint de salud responda correctamente."""

    def test_health_returns_200(self, client):
        """
        Caso feliz: GET /api/health debe responder 200 y JSON con status='ok'.
        """
        r = client.get("/api/health")           # Llamada al endpoint.
        assert r.status_code == 200             # Validamos código HTTP.
        body = r.json()
        assert isinstance(body, dict)           # La respuesta debe ser un objeto.
        assert body.get("status") == "ok"       # Y el campo status debe ser 'ok'.


class TestSuppliers:
    """Verifica el listado de proveedores."""

    def test_list_suppliers_returns_array(self, client):
        """
        Caso feliz: GET /api/suppliers debe responder 200 con una lista no vacía.
        """
        r = client.get("/api/suppliers")        # Pedimos el listado.
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)           # Debe ser array JSON.
        assert len(data) >= 1                   # Debe tener al menos 1 proveedor.


class TestProducts:
    """Verifica contratos y Happy/negative path del recurso productos."""

    def test_list_products_returns_array(self, client):
        """
        Caso feliz: GET /api/products debe responder 200 con lista de productos.
        """
        r = client.get("/api/products")        # Pedimos el listado.
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_existing_product_fields(self, client):
        """
        Caso feliz: GET /api/products/1 debe responder 200
        y traer los campos esperados del producto.
        """
        r = client.get("/api/products/1")      # Producto sembrado por defecto.
        assert r.status_code == 200
        p = r.json()
        for k in ("id", "name", "sku", "cost_cents", "price_cents", "stock", "min_stock", "supplier_id"):
            assert k in p                       # Cada campo debe existir en la respuesta.

    def test_get_missing_product_returns_404(self, client):
        """
        Caso negativo: GET /api/products/999999 debe responder 404.
        """
        r = client.get("/api/products/999999")
        assert r.status_code == 404

    def test_create_product_201(self, client):
        """
        Caso feliz: POST /api/products con datos válidos debe responder 201
        y reflejar el stock enviado.
        """
        payload = {
            "name": "Libreta A4",
            "sku": f"SKU-{uuid.uuid4().hex[:8]}",  # SKU único aleatorio para evitar colisiones.
            "cost_cents": 1500,                      # Costo en centavos.
            "price_cents": 2500,                     # Precio en centavos.
            "stock": 100,
            "min_stock": 10,
            "supplier_id": 1,
        }
        r = client.post("/api/products", json=payload)
        assert r.status_code == 201
        p = r.json()
        assert p["sku"] == payload["sku"]         # El SKU creado coincide.
        assert p["stock"] == 100                  # El stock inicial se persiste.

    def test_create_product_duplicate_sku_409(self, client):
        """
        Caso negativo: repetir un SKU existente debe responder 409 Conflict.
        Usamos 'PAP-001' que viene sembrado en el SUT.
        """
        payload = {
            "name": "SKU duplicado",
            "sku": "PAP-001",                     # SKU que ya existe en la base seed.
            "cost_cents": 1000,
            "price_cents": 2000,
            "stock": 5,
            "min_stock": 2,
            "supplier_id": 1,
        }
        r = client.post("/api/products", json=payload)
        assert r.status_code == 409               # Conflicto por SKU repetido.

    def test_create_product_allows_negative_min_stock(self, client):
        """
        Caso negativo documentado (hallazgo): el SUT acepta min_stock=-1 sin error.
        Esto es un defecto conocido del SUT, la prueba deja evidencia reproducible.
        """
        payload = {
            "name": "Min stock negativo",
            "sku": f"SKU-{uuid.uuid4().hex[:8]}",
            "cost_cents": 1000,
            "price_cents": 2000,
            "stock": 10,
            "min_stock": -1,                     # Valor negativo inválido.
            "supplier_id": 1,
        }
        r = client.post("/api/products", json=payload)
        assert r.status_code == 201               # SUT lo acepta sin rechazo.

    def test_create_product_allows_negative_cost(self, client):
        """
        Caso negativo documentado (hallazgo): el SUT acepta cost_cents=-1000 sin error.
        Esto es un defecto conocido del SUT, la prueba deja evidencia reproducible.
        """
        payload = {
            "name": "Costo negativo",
            "sku": f"SKU-{uuid.uuid4().hex[:8]}",
            "cost_cents": -1000,                 # Costo negativo inválido.
            "price_cents": 1000,
            "stock": 0,
            "min_stock": 1,
            "supplier_id": 1,
        }
        r = client.post("/api/products", json=payload)
        assert r.status_code == 201               # SUT lo acepta sin rechazo.


class TestMovements:
    """Verifica el listado general de movimientos."""

    def test_list_movements_returns_array(self, client):
        """
        Caso feliz: GET /api/movements debe responder 200 con lista.
        """
        r = client.get("/api/movements")         # Historial de movimientos.
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
