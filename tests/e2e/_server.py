import os
import subprocess
import sys
import time
from urllib.request import urlopen
from pathlib import Path

SUT_DIR = Path(__file__).resolve().parents[0] / ".." / "reto-ai-first-fase1" / "reto-ai-first-fase1" / "3-challenge" / "gestor-inventario"


def start_server(port: int = 18003):
    env = os.environ.copy()
    env["ALERTS_FAIL"] = "1"
    script = SUT_DIR / "_qa_temp_server.py"
    script.write_text(
        "from app import app\n"
        "import uvicorn\n"
        "uvicorn.run(app, host='127.0.0.1', port=%d, log_level='error')\n" % port
    )
    proc = subprocess.Popen(
        [sys.executable, str(script)],
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
    raise RuntimeError("No se pudo levantar servidor SUT")


def stop_server(proc):
    try:
        proc.terminate()
    except Exception:
        pass
