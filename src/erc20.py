from __future__ import annotations
from web3 import Web3
from typing import Optional

# Minimal ABI for name/decimals/allowance/approve
ERC20_ABI = [
    {"constant": True, "inputs": [], "name": "name", "outputs": [{"name": "", "type": "string"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "type": "function"},
    {"constant": True, "inputs": [{"name":"owner","type":"address"},{"name":"spender","type":"address"}],
     "name":"allowance","outputs":[{"name":"","type":"uint256"}], "type":"function"},
    {"constant": False, "inputs": [{"name":"spender","type":"address"},{"name":"amount","type":"uint256"}],
     "name":"approve","outputs":[{"name":"","type":"bool"}], "type":"function"},
    {"constant": True, "inputs": [], "name": "symbol", "outputs": [{"name": "", "type": "string"}], "type": "function"}
]

class ERC20:
    def __init__(self, w3: Web3, address: str):
        self.w3 = w3
        self.address = Web3.to_checksum_address(address)
        self.contract = w3.eth.contract(address=self.address, abi=ERC20_ABI)

    def decimals(self, fallback: Optional[int] = None) -> int:
        try:
            return int(self.contract.functions.decimals().call())
        except Exception:
            if fallback is not None:
                return fallback
            raise

    def symbol(self, fallback: Optional[str] = None) -> str:
        try:
            return str(self.contract.functions.symbol().call())
        except Exception:
            return fallback or "TOKEN"

    def allowance(self, owner: str, spender: str) -> int:
        owner = Web3.to_checksum_address(owner)
        spender = Web3.to_checksum_address(spender)
        return int(self.contract.functions.allowance(owner, spender).call())

    def build_revoke_tx(self, owner: str, spender: str) -> dict:
        spender = Web3.to_checksum_address(spender)
        return self.contract.functions.approve(spender, 0).build_transaction
