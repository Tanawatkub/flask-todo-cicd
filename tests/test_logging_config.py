import pytest
from app import logging_config

def test_logging_config_loads():
    """Ensure logging config loads successfully"""
    try:
        import logging.config
        logging.config.dictConfig(logging_config.LOGGING)
    except Exception as e:
        pytest.fail(f"Logging config failed: {e}")
