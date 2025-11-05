import pytest
from src.networks import get_rpc, SUPPORTED_CHAINS

def test_supported_chains():
    assert "ethereum" in SUPPORTED_CHAINS

def test_get_rpc_known():
    assert get_rpc("ethereum").startswith("http")

def test_get_rpc_unknown():
    with pytest.raises(ValueError):
        get_rpc("unknown")
