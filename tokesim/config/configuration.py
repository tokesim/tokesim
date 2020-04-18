import os
from typing import Any, Callable, Union

from mypy_extensions import TypedDict

from tokesim.config.ethereum_config import (
    EthereumAccountsConfig,
    EthereumContractConfigs,
    EthereumContractData,
    parse_ethereum_accounts_config,
    parse_ethereum_contract_config,
)
from tokesim.config.model_config import ModelConfig
from tokesim.util import utils


ContractConfig = Union[EthereumContractConfigs]
ContractData = Union[EthereumContractData]
AccountsConfig = Union[EthereumAccountsConfig]
ContractParser = Callable[[Any], ContractData]
AccountsParser = Callable[[Any], AccountsConfig]


class ContractParserMap(TypedDict):
    ethereum: ContractParser


class AccountParserMap(TypedDict):
    ethereum: AccountsParser


CONFIG_SCHEMA_DIR = os.path.dirname(__file__)
CONFIG_SCHEMA_PATH = CONFIG_SCHEMA_DIR + "/config_schema.json"
CONFIG_SCHEMA = utils.read_json_file(CONFIG_SCHEMA_PATH)

CONFIG_CONTRACT_PARSERS: ContractParserMap = {
    "ethereum": parse_ethereum_contract_config
}

CONFIG_ACCOUNT_PARSERS: AccountParserMap = {"ethereum": parse_ethereum_accounts_config}


class ConfigFile(TypedDict):
    accounts_path: str
    chain_type: str
    contract_config: ContractConfig
    model: ModelConfig
    version: str
