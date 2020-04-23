from abc import ABC
from typing import Any, Sequence, TypeVar

from mesa_behaviors.agents.base_agent import BaseAgent
from mesa_behaviors.utility.base_utility import BaseUtility
from web3.contract import Contract

from tokesim.config.ethereum_config import AccountConfig


S = TypeVar("S")
H = TypeVar("H")
F = TypeVar("F")


class EthereumAgent(BaseAgent[S, H, F], ABC):
    def __init__(
        self,
        strategies: S,
        utility: BaseUtility[S, H, Any],
        historical_func: H,
        label: str,
    ):
        super().__init__(strategies, utility, historical_func, label)

    def set_account(self, acct: AccountConfig) -> None:
        self.acct = acct

    def set_contracts(self, contracts: Sequence[Contract]) -> None:
        self.contracts = contracts
