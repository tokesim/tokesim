from typing import List, NewType

from mypy_extensions import TypedDict


Port = NewType("Port", str)

Chain = NewType("Chain", str)

PrivateKey = NewType("PrivateKey", str)

PubAddr = NewType("PubAddr", str)

Balance = NewType("Balance", str)

ChainId = NewType("ChainId", int)


class Meta(TypedDict):
    rpcPort: Port
    chainId: ChainId


class Master(TypedDict):
    private_key: PrivateKey
    pub_addr: PubAddr
    balance: Balance


class AccountEntry(TypedDict):
    private_key: PrivateKey
    pub_addr: PubAddr
    balance: Balance


AccountList = NewType("AccountList", List[AccountEntry])


class Accounts(TypedDict):
    master: Master
    accounts: AccountList


class SimulationParams(TypedDict):
    chain: Chain
    accounts: Accounts


SimulationId = NewType("SimulationId", str)


class SimulationResult(TypedDict):
    id: SimulationId
    meta: Meta
    port: Port


StoppedSimulation = NewType("StoppedSimulation", bool)

StartedBlockTransactionResult = NewType("StartedBlockTransactionResult", bool)

EndBlockTransactionResult = NewType("EndBlockTransactionResult", bool)
