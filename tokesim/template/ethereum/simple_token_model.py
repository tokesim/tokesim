from mesa.datacollection import DataCollector
from mesa_behaviors.history.binary import BinaryHistory
from web3 import HTTPProvider, Web3

from tokesim.client.tokesim import TokesimClient
from tokesim.models.ethereum_model import EthereumModel, EthereumModelConfig
from tokesim.template.ethereum.simple_token_agent import SimpleTokenAgentFeatures


# There exists some function that you can Type to reference the required returned state of an agent So an AgentPopulation
# is typed to return a subset of state that you can reference in the model to build aggregate statistics
# The aim is to be abble to call binary_encode_state in a typesafe way or a type constrained way because you know the agent
# population is bound to contain a subset of data
"""
  SimpleTokenModelConfig : EthereumModelConfig = {


  }
        agent_population: AgentPopulation[SimpleTokenAgentFeatures],
        schedule: BaseScheduler,
        history: BinaryHistory,
        terminal_step: int,
"""


class SimpleTokenModel(EthereumModel[SimpleTokenAgentFeatures, BinaryHistory]):
    # typings don't support Generic Dictionaries
    def __init__(
        self,
        config: EthereumModelConfig[SimpleTokenAgentFeatures, BinaryHistory] = None,
        height: int = 0,
        width: int = 0,
        simulationId: str = None,
        client: TokesimClient = None,
    ):
        super().__init__(config, client)
        self.datacollector = DataCollector(
            {
                "tokens_purchased": "tokens",
                "token_supply": "token_supply",
                "token_price": "token_price",
            },
            {
                "token": lambda agent: agent.features().tokens
            },  # Model-level count of happy agents
        )
        self.running = True

    def initial_capital(self) -> int:
        accts = self.config.config.accounts["accounts"]
        return sum([int(acct["balance"], 16) for acct in accts])

    def assign_contracts(self) -> None:
        agents = self.config.model_spec.agent_population
        [agent.set_contracts([self.simple_token]) for agent in agents]

    def assign_accounts(self) -> None:
        agents = self.config.model_spec.agent_population
        accounts = self.config.config.accounts["accounts"]
        [agent.set_account(accounts[idx]) for idx, agent in enumerate(agents)]

    def deploy(self) -> None:
        master = self.config.config.accounts["master"]
        token_contract = self.config.config.contract_data[0]
        w3 = Web3(HTTPProvider(f"http://localhost:{self.config.rpcPort}"))  # type: ignore

        SimulatedContract = w3.eth.contract(
            abi=token_contract["abi"], bytecode=token_contract["bytecode"]  # type: ignore
        )
        master_acct_addr = Web3.toChecksumAddress(master["pub_addr"])

        tx_hash = SimulatedContract.constructor("Gold", "GLD").transact(
            {"from": master_acct_addr}
        )
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        self.simple_token = w3.eth.contract(
            address=tx_receipt.contractAddress, abi=token_contract["abi"]  # type: ignore
        )

        self.assign_accounts()
        self.assign_contracts()

    def encode_history(self) -> int:
        tokens = sum([agent.features().tokens for agent in self.agents]) / len(
            self.agents
        )
        if tokens > 0.5:
            return 1
        else:
            return 0

    def step(self) -> None:
        majority_buy = self.encode_history()
        self.history.add(majority_buy)
        self.schedule.step()
        # collect data
        super().step()
        self.tokens = sum([agent.features().tokens for agent in self.agents])
        self.token_supply = self.simple_token.functions.totalSupply().call()
        self.token_price = self.simple_token.functions.rate().call()
        self.datacollector.collect(self)
        if self.schedule.steps >= 100:
            self.running = False
