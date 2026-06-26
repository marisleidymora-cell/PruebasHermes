import pytest
import os
import sys
import importlib

# Ensure the project root is in sys.path so `import app` works
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture(autouse=True)
def setup_db():
    """Initialize database before each test with proper isolation"""
    test_db = "/tmp/test_inventario.db"

    try:
        os.remove(test_db)
    except FileNotFoundError:
        pass

    os.environ["DB_PATH"] = test_db

    # Force reload of app module to pick up new DB_PATH
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
