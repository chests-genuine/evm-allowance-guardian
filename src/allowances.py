from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

from web3 import Web3
from web3.middleware import geth_poa_middleware

from .erc20 import ERC20
from .networks import get_rpc

DATA_DIR = Path(__file__).parent / "data"

def load_json(name: str) -> dict:
    with open(DATA_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)

def connect(chain: str) -> Web3:
    w3 = Web3(Web3.HTTPProvider(get_rpc(chain)))
    # Some chains (e.g., Polygon/BSC/Base) need POA middleware
    try:
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    except Exception:
        pass
    if not w3.is_connected():
        raise RuntimeError(f"Cannot connect RPC for chain {chain}")
    return w3

def format_amount(value: int, decimals: int) -> str:
    if decimals <= 0:
        return str(value)
    factor = 10 ** decimals
    whole = value // factor
    frac = value % factor
    if frac == 0:
        return str(whole)
    s = f"{whole}.{str(frac).zfill(decimals)}"
    # trim trailing zeros
    return s.rstrip("0").rstrip(".")

def check_allowances(
    address: str,
    chains: Optional[List[str]] = None,
) -> List[Tuple[str, str, str, str]]:
    """
    Returns list of (chain, token_symbol, spender, allowance_str)
    """
    address = Web3.to_checksum_address(address)
    tokens_cfg: Dict[str, List[dict]] = load_json("tokens.json")
    spenders_cfg: Dict[str, List[str]] = load_json("spenders.json")

    results: List[Tuple[str, str, str, str]] = []
    chains = chains or list(tokens_cfg.keys())
    for chain in chains:
        if chain not in tokens_cfg:
            continue
        w3 = connect(chain)
        for token in tokens_cfg[chain]:
            erc = ERC20(w3, token["address"])
            decimals = token.get("decimals")
            if decimals is None:
                try:
                    decimals = erc.decimals()
                except Exception:
                    decimals = 18
            symbol = token.get("symbol") or erc.symbol("TOKEN")
            for spender in spenders_cfg.get(chain, []):
                try:
                    raw = erc.allowance(address, spender)
                    human = format_amount(raw, decimals)
                    results.append((chain, symbol, Web3.to_checksum_address(spender), human))
                except Exception:
                    results.append((chain, symbol, Web3.to_checksum_address(spender), "error"))
    return results
