# strategy maps a set of historical states to future actions
# a behavior chooses a strategy that maximizes the utility of that behavior
# should take generics CoolAgent(BaseAgent[Strategy,bitarray,])
from typing import NamedTuple, TypeVar

from mesa_behaviors.utility.base_utility import BaseUtility
from mesa_behaviors.utility.binary import BinaryUtilityScore
from web3 import Web3

from tokesim.agents.ethereum_agent import EthereumAgent


S = TypeVar("S")
H = TypeVar("H")


class SimpleTokenAgentFeatures(NamedTuple):
    tokens: int
    action: int


class SimpleTokenAgent(EthereumAgent[S, H, SimpleTokenAgentFeatures]):
    def __init__(
        self,
        strategies: S,
        utility: BaseUtility[S, H, BinaryUtilityScore],
        historical_func: H,
        label: str,
    ):
        super().__init__(strategies, utility, historical_func, label)
        self.latest_scores: BinaryUtilityScore = {}
        self.feature = SimpleTokenAgentFeatures(tokens=0, action=0)

    def features(self) -> SimpleTokenAgentFeatures:
        return self.feature

    def select(self, scores: BinaryUtilityScore) -> int:
        score = sorted(scores.items(), key=lambda x: x[1]["score"])[-1][1]
        return score["prediction"]

    def token_supply(self) -> int:
        simple_token = self.contracts[0]
        acct = Web3.toChecksumAddress(self.acct["pub_addr"])
        return simple_token.functions.balanceOf(acct).call()

    def budget(self) -> int:
        simple_token = self.contracts[0]
        acct = Web3.toChecksumAddress(self.acct["pub_addr"])
        return simple_token.web3.eth.getBalance(acct)

    def step(self) -> None:
        self.latest_scores = self.utility.utility_score(self.strategies, self.history)
        action = self.select(self.latest_scores)
        simple_token = self.contracts[0]
        acct = Web3.toChecksumAddress(self.acct["pub_addr"])
        self.balance = simple_token.web3.eth.getBalance(acct)
        budget_limit = int(self.balance * 0.90)
        if action == 1:
            try:
                simple_token.functions.pay().transact(
                    {"from": acct, "value": budget_limit}  # type: ignore
                )
                self.feature = SimpleTokenAgentFeatures(tokens=1, action=1)
            except Exception as e:
                print(e)
                self.feature = SimpleTokenAgentFeatures(tokens=0, action=0)
        else:
            try:
                if simple_token.functions.balanceOf(acct).call() > 0:
                    simple_token.functions.exchange(1).transact({"from": acct})
                    self.feature = SimpleTokenAgentFeatures(tokens=0, action=-1)
            except Exception as e:
                self.feature = SimpleTokenAgentFeatures(tokens=0, action=0)
                print(e)

    def label(self) -> str:
        return self.label_name
