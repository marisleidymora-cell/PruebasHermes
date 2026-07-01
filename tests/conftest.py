import os
import importlib
import uuid
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import urlopen

import pytest
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
ALERTS_FAIL = os.getenv("ALERTS_FAIL", "0")

# Ruta local al SUT real, usada solo para levantar un servidor auxiliar
# aislado cuando necesitamos forzar ALERTS_FAIL=1 sin tocar el servidor
# principal que usa el resto de la suite.
SUT_DIR = (
    Path.home() / "Desktop" / "reto-ai-first-fase1" / "reto-ai-first-fase1"
    / "3-challenge" / "gestor-inventario"
)


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL.rstrip("/")


@pytest.fixture(scope="session")
def client(base_url):
    import httpx
    return httpx.Client(base_url=base_url, timeout=10.0)


@pytest.fixture
def fresh_client(base_url):
    import httpx
    with httpx.Client(base_url=base_url, timeout=10.0) as c:
        yield c


@pytest.fixture
def fresh_product(client):
    """
    Crea un producto nuevo y único para cada test que la use, en vez de
    reusar los productos sembrados (id=1, id=2, ...).

    Por qué existe esta fixture:
    - Antes, varios tests sumaban/restaban stock directo sobre los productos
      semilla del SUT. Si la suite se corría dos veces seguidas, el stock
      quedaba distinto cada vez (no era repetible) y un test podía "ensuciar"
      el punto de partida de otro.
    - Con esta fixture, cada test arranca con su propio producto, con stock
      conocido y controlado por el propio test. Así la suite es repetible:
      se puede correr N veces sin que los resultados cambien por acumulación
      de datos de corridas anteriores.

    Devuelve el dict del producto recién creado (igual que la respuesta de
    la API), incluyendo su "id" para usarlo en movimientos de stock.
    """
    payload = {
        "name": "QA Fixture Product",
        "sku": f"QA-FIX-{uuid.uuid4().hex[:10]}",
        "cost_cents": 1000,
        "price_cents": 2000,
        "stock": 50,
        "min_stock": 5,
        "supplier_id": 1,
    }
    r = client.post("/api/products", json=payload)
    assert r.status_code == 201, f"No se pudo crear producto de prueba: {r.text}"
    return r.json()


def _write_alerts_fail_server_script(script_path: Path, port: int) -> None:
    script_path.write_text(
        "import os\n"
        f"os.chdir({str(SUT_DIR)!r})\n"
        "import sys\n"
        f"sys.path.insert(0, {str(SUT_DIR)!r})\n"
        "from app import app\n"
        "import uvicorn\n"
        f"config = uvicorn.Config(app, host='127.0.0.1', port={port}, log_level='error')\n"
        "server = uvicorn.Server(config)\n"
        "server.run()\n"
    )


def start_alerts_fail_server(port: int = 18003):
    """
    Levanta una instancia aparte del SUT (proceso separado) con
    ALERTS_FAIL=1 desde el arranque, para poder probar el 503 real
    de /api/stock/alerts sin afectar al servidor principal que usa
    el resto de la suite.

    Devuelve (proceso, puerto). Usar siempre junto con stop_alerts_fail_server
    para cerrarlo al terminar el test.
    """
    import tempfile

    env = os.environ.copy()
    env["ALERTS_FAIL"] = "1"
    fd, script_path_str = tempfile.mkstemp(suffix=".py", prefix=f"sut_alerts_{port}_")
    script_path = Path(script_path_str)
    try:
        os.close(fd)
        _write_alerts_fail_server_script(script_path, port)
        proc = subprocess.Popen(
            [sys.executable, str(script_path)],
            cwd=str(SUT_DIR),
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        url = f"http://127.0.0.1:{port}/api/health"
        for _ in range(50):
            try:
                urlopen(url, timeout=0.3)
                return proc, port
            except Exception:
                time.sleep(0.25)
        proc.terminate()
        raise RuntimeError(f"No se pudo levantar servidor ALERTS_FAIL=1 en puerto {port}")
    finally:
        try:
            script_path.unlink()
        except Exception:
            pass


def stop_alerts_fail_server(proc) -> None:
    try:
        proc.terminate()
        proc.wait(timeout=5)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass


@pytest.fixture
def alerts_fail_client(request):
    """
    Fixture función que arma un servidor auxiliar del SUT con ALERTS_FAIL=1
    y entrega un cliente httpx apuntando a él. Al terminar el test, apaga
    ese servidor y espera a que el proceso libere el puerto antes de seguir.
    El servidor principal (usado por el resto de la suite) no se toca en
    ningún momento.

    Cada test que pida esta fixture recibe un puerto distinto (basado en un
    hash corto del nombre del test) para poder correr varios tests que la
    usan sin pisarse el puerto entre sí, incluso si un proceso anterior
    tarda en soltar el socket.
    """
    import httpx

    port = 18003 + (abs(hash(request.node.nodeid)) % 500)
    proc, port = start_alerts_fail_server(port)
    try:
        with httpx.Client(base_url=f"http://127.0.0.1:{port}", timeout=10.0) as c:
            yield c
    finally:
        stop_alerts_fail_server(proc)


def _allure_attach_text(name, body):
    try:
        allure = importlib.import_module("allure")
        allure.attach(body, name=name, attachment_type=allure.attachment_type.TEXT)
    except Exception:
        pass


def write_allure_screenshot(page, name="screenshot"):
    try:
        allure = importlib.import_module("allure")
        allure.attach(page.screenshot(full_page=True), name=name, attachment_type=allure.attachment_type.PNG)
    except Exception:
        pass


def _clean_allure_results(path="/Users/admin/Desktop/PruebasHermes-trackQA/allure-results"):
    try:
        import shutil
        if os.path.isdir(path):
            shutil.rmtree(path)
        os.makedirs(path, exist_ok=True)
    except Exception:
        pass


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    _clean_allure_results()

