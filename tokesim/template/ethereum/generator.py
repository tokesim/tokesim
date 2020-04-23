import json
import os
import shutil

# from tokesim.util import account, utils
from tokesim.config import ethereum_config
from tokesim.config.configuration import CONFIG_SCHEMA_PATH, ConfigFile


# TODO fix this by refactoring everything to utils and dropping config except for config path
TEMPLATE_DIR = f"{os.path.dirname(__file__)}"
TEMPLATE_CONTRACT_DIR = f"{TEMPLATE_DIR}/contracts"


def _create_default_config(dest: str, agents: int) -> ConfigFile:
    default_config: ConfigFile = {  # type: ignore
        "$schema": f"./config_schema.json",
        "accounts_path": f"{dest}/accounts.json",
        "chain_type": f"ethereum",
        "contract_config": [
            {
                "abi_path": f"{dest}/contracts/SimpleToken_abi.json",
                "bytecode_path": f"{dest}/contracts/SimpleToken.bin",
                "name": "TestToken",
            }
        ],
        "model": {
            "package": {
                "class_name": "SimpleTokenModel",
                "module_name": "simple_token_model",
                "module_path": dest,
            },
            "params": {
                "population": agents,
                "name": "MyToken",
                "symbol": "MYT",
                "decimals": 2,
                "num_agents": 10,
                "memory": 3,
                "num_strategies": 4,
            },
            "config": {
                "class_name": "SimpleTokenMixedGameRandom",
                "module_name": "simple_token_config",
                "module_path": dest,
            },
            "dashboard": {
                "class_name": "SimpleTokenDashboard",
                "module_name": "simple_token_dashboard",
                "module_path": dest,
            },
        },
        "version": "0.0.1",
    }
    return default_config


def setup(dest: str, num_agents: int) -> None:
    # create if the destination directory doesn't exist
    # write the default json schema to disk for config
    # generate an accounts file if it doesn't exist
    # generate reasonable defaults for the paths for Sample contracts
    normalized_dest = os.path.realpath(os.path.abspath(f"{dest}"))
    contracts_dir = f"{normalized_dest}/contracts"

    src_token_abi_path = f"{TEMPLATE_CONTRACT_DIR}/SimpleToken_abi.json"
    src_token_bin_path = f"{TEMPLATE_CONTRACT_DIR}/SimpleToken.bin"
    dest_token_abi_path = f"{contracts_dir}/SimpleToken_abi.json"
    dest_token_bin_path = f"{contracts_dir}/SimpleToken.bin"
    account_file_path = f"{normalized_dest}/accounts.json"
    src_template_token_path = f"{TEMPLATE_DIR}/simple_token_model.py"
    src_template_agent_path = f"{TEMPLATE_DIR}/simple_token_agent.py"
    src_template_token_config = f"{TEMPLATE_DIR}/simple_token_config.py"
    src_template_token_dashboard = f"{TEMPLATE_DIR}/simple_token_dashboard.py"
    if not os.path.exists(dest):
        os.makedirs(dest)
    if not os.path.exists(contracts_dir):
        os.makedirs(contracts_dir)

    shutil.copy(CONFIG_SCHEMA_PATH, dest)
    shutil.copy(src_template_token_path, normalized_dest)
    shutil.copy(src_template_agent_path, normalized_dest)
    shutil.copy(src_template_token_config, normalized_dest)
    shutil.copy(src_template_token_dashboard, normalized_dest)
    if not os.path.exists(account_file_path):
        ethereum_config.create_account_config_file(
            ethereum_config.create_ethereum_account_config(num_agents),
            account_file_path,
        )
    if not os.path.exists(dest_token_abi_path):
        shutil.copy(src_token_abi_path, dest_token_abi_path)
    if not os.path.exists(dest_token_bin_path):
        shutil.copy(src_token_bin_path, dest_token_bin_path)
    with open(dest + "/simulation.json", "w") as f:
        config = _create_default_config(normalized_dest, num_agents)
        f.write(json.dumps(config, indent=4, sort_keys=True))
