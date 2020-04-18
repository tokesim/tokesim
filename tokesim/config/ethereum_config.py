import json
import secrets
from typing import List, NamedTuple, Sequence, cast

from eth_keys import keys
from eth_utils import encode_hex
from mypy_extensions import TypedDict
import numpy as np

from tokesim.util import utils


class EthereumContractConfig(TypedDict):
    abi_path: str
    bytecode_path: str
    name: str


class AccountConfig(TypedDict):
    private_key: str
    pub_addr: str
    balance: str


class EthereumAccountsConfig(TypedDict):
    master: AccountConfig
    accounts: List[AccountConfig]


class EthereumContractDatum(NamedTuple):
    abi: object
    bytecode: str
    name: str


EthereumContractData = Sequence[EthereumContractDatum]
EthereumContractConfigs = Sequence[EthereumContractConfig]


def parse_ethereum_contract_config(
    contract_config: EthereumContractConfigs,
) -> EthereumContractData:
    ethereum_config = []
    for contract in contract_config:
        abi = utils.read_json_file(contract["abi_path"])
        bytecode = utils.read_file(contract["bytecode_path"])
        name = contract["name"]
        ethereum_contract_datum = cast(
            EthereumContractDatum, {"abi": abi, "bytecode": bytecode, "name": name}
        )
        ethereum_config.append(ethereum_contract_datum)
    return ethereum_config


def parse_ethereum_accounts_config(accounts_path: str) -> EthereumAccountsConfig:
    return cast(EthereumAccountsConfig, utils.read_json_file(accounts_path))


def generate_random_account_config(balance: int) -> AccountConfig:
    priv_key = keys.PrivateKey(secrets.token_bytes(32))
    address = encode_hex(priv_key.public_key.to_canonical_address())
    return {
        "private_key": priv_key.to_hex(),
        "pub_addr": address,
        "balance": hex(balance),
    }


def create_ethereum_account_config(num_accounts: int) -> EthereumAccountsConfig:

    master = generate_random_account_config(10000000000000000000)
    distro = [
        int(np.random.normal(10000, 0.1) * 100000000000000000)
        for x in range(num_accounts)
    ]
    accounts = [generate_random_account_config(bal) for bal in distro]
    return {"master": master, "accounts": accounts}


def create_account_config_file(
    config: EthereumAccountsConfig, full_path: str = "accounts.json"
) -> None:
    with open(full_path, "w") as outfile:
        json.dump(config, outfile, indent=4)
