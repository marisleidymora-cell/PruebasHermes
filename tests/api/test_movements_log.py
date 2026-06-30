"""
Suite para historial de movimientos de stock.

Cobertura:
- GET /api/movements responde 200 y devuelve lista.
- Forma de entrega: newest first por id descendente.
"""
import pytest


class TestMovementsLog:
    """Verifica el endpoint de historial/lectura de movimientos."""

    def test_movements_returns_array_and_ordered_desc(self, client):
        """
        Caso feliz: GET /api/movements debe responder 200 y ser una lista.
        Si hay más de un movimiento, se asume ordenamiento descendente
        verificando que el primer id sea mayor o igual al segundo.
        """
        r = client.get("/api/movements")        # Pedimos historial completo.
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)           # Debe ser array JSON.
        if len(data) > 1:                       # Si hay muestra, validamos orden.
            assert data[0]["id"] >= data[1]["id"]
