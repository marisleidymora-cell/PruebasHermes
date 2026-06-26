import pytest
import os
import sys
import importlib
from httpx import AsyncClient, ASGITransport

@pytest.fixture(autouse=True)
def setup_db():
    """Initialize database before each test with proper isolation"""
    test_db = "/tmp/test_inventario.db"
    
    try:
        os.remove(test_db)
    except FileNotFoundError:
        pass
    
    os.environ["DB_PATH"] = test_db
    
    # Force reload of app module
    if 'app' in sys.modules:
        del sys.modules['app']
    
    import app
    importlib.reload(app)
    app.init_db()
    
    yield
    
    try:
        os.remove(test_db)
    except FileNotFoundError:
        pass
    if 'app' in sys.modules:
        del sys.modules['app']


@pytest.fixture
def transport():
    """Create fresh ASGITransport for each test"""
    import app
    return ASGITransport(app=app.app)


BASE_URL = "http://testserver"


# ========== API Contract Tests ==========\

@pytest.mark.anyio
async def test_health_endpoint(transport):
    """Test /api/health returns ok status"""
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        response = await client.get("/api/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


@pytest.mark.anyio
async def test_list_suppliers(transport):
    """Test /api/suppliers returns list of suppliers"""
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        response = await client.get("/api/suppliers")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3


@pytest.mark.anyio
async def test_list_products(transport):
    """Test /api/products returns list of products"""
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        response = await client.get("/api/products")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 6


@pytest.mark.anyio
async def test_get_product_found(transport):
    """Test /api/products/{id} returns product when found"""
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        response = await client.get("/api/products/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["sku"] == "PAP-001"


@pytest.mark.anyio
async def test_get_product_not_found(transport):
    """Test /api/products/{id} returns 404 when product not found"""
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        response = await client.get("/api/products/999")
        assert response.status_code == 404


# ========== Functional Tests - Happy Path ==========\

@pytest.mark.anyio
async def test_create_product_success(transport):
    """Test POST /api/products creates product successfully"""
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        product_data = {
            "name": "Producto Nuevo",
            "sku": "NEW-001",
            "cost_cents": 10000,
            "price_cents": 15000,
            "stock": 10,
            "min_stock": 5,
            "supplier_id": 1
        }
        response = await client.post("/api/products", json=product_data)
        assert response.status_code == 201


@pytest.mark.anyio
async def test_create_product_duplicate_sku(transport):
    """Test POST /api/products returns 409 for duplicate SKU"""
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        product_data = {
            "name": "Producto Duplicado",
            "sku": "PAP-001",
            "cost_cents": 10000,
            "price_cents": 15000,
            "stock": 10,
            "min_stock": 5,
            "supplier_id": 1
        }
        response = await client.post("/api/products", json=product_data)
        assert response.status_code == 409
        assert "SKU ya existe" in response.json()["detail"]


@pytest.mark.anyio
async def test_create_product_invalid_supplier(transport):
    """Test POST /api/products returns 400 for invalid supplier"""
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        product_data = {
            "name": "Producto Sin Proveedor",
            "sku": "NEW-002",
            "cost_cents": 10000,
            "price_cents": 15000,
            "stock": 10,
            "min_stock": 5,
            "supplier_id": 999
        }
        response = await client.post("/api/products", json=product_data)
        assert response.status_code == 400
        assert "Proveedor no encontrado" in response.json()["detail"]


# ========== Defect Tests ==========\

@pytest.mark.anyio
async def test_defect_negative_stock_allowed(transport):
    """DEFECT #1: OUT movement with qty > stock should NOT be allowed, but it is"""
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        initial = await client.get("/api/products/1")
        initial_stock = initial.json()["stock"]
        
        movement = {
            "product_id": 1,
            "type": "OUT",
            "qty": 99999,
            "notes": "Test negativo"
        }
        response = await client.post("/api/stock/movement", json=movement)
        assert response.status_code == 201  # BUG: Should be 400!
        
        updated = await client.get("/api/products/1")
        assert updated.json()["stock"] < 0


@pytest.mark.anyio
async def test_defect_decimal_quantity_accepted(transport):
    """DEFECT #2: qty accepts decimal values like 2.5"""
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        movement = {
            "product_id": 1,
            "type": "IN",
            "qty": 2.5,
            "notes": "Test decimal"
        }
        response = await client.post("/api/stock/movement", json=movement)
        assert response.status_code == 201
        assert response.json()["qty"] == 2.5


@pytest.mark.anyio
async def test_defect_negative_min_stock_accepted(transport):
    """DEFECT #3: min_stock accepts negative values"""
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        product_data = {
            "name": "Producto con min_stock negativo",
            "sku": "NEG-001",
            "cost_cents": 10000,
            "price_cents": 15000,
            "stock": 10,
            "min_stock": -1,
            "supplier_id": 1
        }
        response = await client.post("/api/products", json=product_data)
        assert response.status_code == 201
        assert response.json()["min_stock"] == -1


@pytest.mark.anyio
async def test_defect_negative_cost_accepted(transport):
    """DEFECT #4: cost_cents accepts negative values"""
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        product_data = {
            "name": "Producto con costo negativo",
            "sku": "NEG-002",
            "cost_cents": -5000,
            "price_cents": 15000,
            "stock": 10,
            "min_stock": 5,
            "supplier_id": 1
        }
        response = await client.post("/api/products", json=product_data)
        assert response.status_code == 201
        assert response.json()["cost_cents"] == -5000


# ========== Integration Failure Tests ==========\

@pytest.mark.anyio
async def test_alerts_service_failure(transport):
    """Test ALERTS_FAIL=1 causes 503 on stock alerts"""
    os.environ["ALERTS_FAIL"] = "1"
    try:
        async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
            response = await client.get("/api/stock/alerts")
            assert response.status_code == 503
            assert "Servicio de alertas no disponible" in response.json()["detail"]
    finally:
        os.environ.pop("ALERTS_FAIL", None)


@pytest.mark.anyio
async def test_alerts_service_failure_on_out_movement(transport):
    """Test ALERTS_FAIL=1 causes 503 on OUT movement"""
    os.environ["ALERTS_FAIL"] = "1"
    try:
        async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
            movement = {
                "product_id": 1,
                "type": "OUT",
                "qty": 1,
                "notes": "Test alert failure"
            }
            response = await client.post("/api/stock/movement", json=movement)
            assert response.status_code == 503
    finally:
        os.environ.pop("ALERTS_FAIL", None)


# ========== Stock Data Integrity Tests ==========\

@pytest.mark.anyio
async def test_stock_increases_on_in_movement(transport):
    """Verify stock increments correctly on IN movement"""
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        get_before = await client.get("/api/products/2")
        stock_before = get_before.json()["stock"]
        
        movement = {"product_id": 2, "type": "IN", "qty": 50}
        response = await client.post("/api/stock/movement", json=movement)
        assert response.status_code == 201
        
        get_after = await client.get("/api/products/2")
        assert get_after.json()["stock"] == stock_before + 50


@pytest.mark.anyio
async def test_movement_type_validation(transport):
    """Test invalid movement type is rejected"""
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        movement = {"product_id": 1, "type": "INVALID", "qty": 10}
        response = await client.post("/api/stock/movement", json=movement)
        assert response.status_code == 400
        assert "IN o OUT" in response.json()["detail"]