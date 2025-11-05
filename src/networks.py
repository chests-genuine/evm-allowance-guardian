from __future__ import annotations
import os

DEFAULT_RPCS = {
    "ethereum": os.getenv("RPC_ETHEREUM", "https://ethereum.publicnode.com"),
    "base":     os.getenv("RPC_BASE", "https://base-rpc.publicnode.com"),
    "arbitrum": os.getenv("RPC_ARBITRUM", "https://arbitrum-one.publicnode.com"),
    "polygon":  os.getenv("RPC_POLYGON", "https://polygon-bor.publicnode.com"),
    "bsc":      os.getenv("RPC_BSC", "https://bsc-dataseed.binance.org"),
    "optimism":      os.getenv("RPC_BSC", "https://optimism.publicnode.com"),
}

def get_rpc(chain: str) -> str:
    rpc = DEFAULT_RPCS.get(chain.lower())
    if not rpc:
        raise ValueError(f"Unsupported chain: {chain}")
    return rpc

SUPPORTED_CHAINS = tuple(DEFAULT_RPCS.keys())
