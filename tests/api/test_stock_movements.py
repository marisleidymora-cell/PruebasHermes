"""
Suite de caja negra sobre alertas y movimientos de stock.

Cobertura:
- GET /api/stock/alerts en modo normal (200, lista)
- GET /api/stock/alerts con ALERTS_FAIL=1 real -> 503 (servidor aislado)
- POST /api/stock/movement OUT sin fallo (201)
- Casos de frontera de qty: qty=0 y qty negativo

Esta suite usa `client` desde conftest.py (modo normal, servidor principal).
El escenario 503 se prueba contra un servidor auxiliar aparte, levantado
por la fixture `alerts_fail_client`, para no depender de adivinar en qué
estado quedó el servidor principal.
"""
import pytest


class TestAlerts:
    """Casos sobre el recurso de alertas de stock mínimo."""

    def test_alerts_without_failure_returns_200(self, client):
        """
        Caso feliz: sin fallo, GET /api/stock/alerts debe responder 200
        y devolver un array JSON con productos bajo mínimo.
        """
        r = client.get("/api/stock/alerts")      # Pedimos alertas al SUT principal.
        assert r.status_code == 200
        assert isinstance(r.json(), list)         # Debe ser lista, vacía o con items.

    def test_alerts_with_alerts_fail_returns_503(self, alerts_fail_client):
        """
        Caso negativo / Integración real: contra un servidor auxiliar que
        arrancó con ALERTS_FAIL=1 desde el inicio, GET /api/stock/alerts
        debe responder 503 sí o sí. Antes este caso tenía un assert que
        aceptaba (201, 503) — es decir, nunca podía fallar. Ahora se prueba
        contra un servidor donde sabemos con certeza que el fallo está activo,
        así que el test SÍ puede fallar si el SUT deja de comportarse así.
        """
        r = alerts_fail_client.get("/api/stock/alerts")
        assert r.status_code == 503

    def test_out_movement_with_alerts_fail_returns_503(self, alerts_fail_client):
        """
        Caso negativo / Integración real: con ALERTS_FAIL=1 activo desde el
        arranque, un movimiento OUT también debe fallar con 503, ya que el
        endpoint consulta el servicio de alertas después de registrar la
        salida de stock.
        """
        r = alerts_fail_client.get("/api/products")
        product_id = r.json()[0]["id"]
        payload = {"product_id": product_id, "type": "OUT", "qty": 1}
        r = alerts_fail_client.post("/api/stock/movement", json=payload)
        assert r.status_code == 503

    def test_out_movement_without_failure_returns_201(self, client, fresh_product):
        """
        Caso feliz: POST /api/stock/movement type=OUT sin fallo debe ser 201.
        Usa `fresh_product` (producto propio del test) en vez de un producto
        semilla, para no depender ni alterar el stock de otros tests.
        """
        payload = {"product_id": fresh_product["id"], "type": "OUT", "qty": 1}
        r = client.post("/api/stock/movement", json=payload)
        assert r.status_code == 201


class TestMovementQtyBoundaries:
    """
    Casos de frontera para el campo `qty` de un movimiento de stock.

    El SUT define `qty` como float sin validación de rango (ver defecto D-02
    en docs/defect_report.md). Estos tests documentan, con evidencia
    reproducible, qué pasa exactamente en los límites: qty=0 y qty negativo.
    """

    def test_movement_with_qty_zero_is_accepted_no_op(self, client, fresh_product):
        """
        Caso de frontera: qty=0 en un movimiento IN.
        Hallazgo: el SUT acepta qty=0 con 201 y no cambia el stock
        (movimiento "sin efecto" registrado igual en el historial).
        """
        before = fresh_product["stock"]
        r = client.post("/api/stock/movement", json={
            "product_id": fresh_product["id"],
            "type": "IN",
            "qty": 0,
            "notes": "QA boundary qty=0",
        })
        assert r.status_code == 201               # El SUT no rechaza qty=0.
        r = client.get(f"/api/products/{fresh_product['id']}")
        assert r.json()["stock"] == before         # Y el stock no cambia.

    def test_movement_with_negative_qty_is_accepted_and_inverts_direction(self, client, fresh_product):
        """
        Caso de frontera / hallazgo: qty negativo en un movimiento IN.
        El SUT no valida que qty sea positivo, así que un IN con qty=-5
        termina restando stock en vez de sumarlo (invierte la dirección
        del movimiento sin avisar). Se documenta como evidencia reproducible.
        """
        before = fresh_product["stock"]
        r = client.post("/api/stock/movement", json={
            "product_id": fresh_product["id"],
            "type": "IN",
            "qty": -5,
            "notes": "QA boundary qty negativo",
        })
        assert r.status_code == 201                # El SUT lo acepta sin rechazo.
        r = client.get(f"/api/products/{fresh_product['id']}")
        assert r.json()["stock"] == before - 5      # IN con qty negativo resta en vez de sumar.
