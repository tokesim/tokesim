from typing import Any, NamedTuple, cast

import jsonschema

from tokesim.config import model_config
from tokesim.config.configuration import (
    CONFIG_CONTRACT_PARSERS,
    CONFIG_SCHEMA,
    AccountsConfig,
    ConfigFile,
    ContractData,
)
from tokesim.util import utils


class ParsedConfig(NamedTuple):
    contract_data: ContractData
    class_ref: Any
    config_class_ref: Any
    dashboard_class_ref: Any
    model_params: Any
    version: str
    accounts: AccountsConfig


def parse_contract_config(config: ConfigFile) -> ContractData:
    chain_type = config["chain_type"]
    parser = CONFIG_CONTRACT_PARSERS[chain_type]  # type: ignore
    if parser is None:
        raise ValueError(f"Could not understand chain type: {chain_type}")
    return parser(config["contract_config"])


def _parse_config(config: ConfigFile) -> ParsedConfig:
    contract_data = parse_contract_config(config)
    accounts = cast(AccountsConfig, utils.read_json_file(config["accounts_path"]))
    model = config["model"]
    package = model["package"]
    config_class = model["config"]
    dashboard_class = model["dashboard"]
    class_ref = model_config.get_module_class(package)
    config_class_ref = model_config.get_module_class(config_class)
    dashboard_class_ref = model_config.get_module_class(dashboard_class)
    version = config["version"]
    return ParsedConfig(
        contract_data=contract_data,
        class_ref=class_ref,
        model_params=model["params"],
        config_class_ref=config_class_ref,
        dashboard_class_ref=dashboard_class_ref,
        version=version,
        accounts=accounts,
    )


def parse_config(config_path: str) -> ParsedConfig:
    config_file: ConfigFile = cast(ConfigFile, utils.read_json_file(config_path))
    try:

        jsonschema.validate(config_file, schema=CONFIG_SCHEMA)
        return _parse_config(config_file)
    except Exception as e:
        raise ValueError(e.with_traceback(e.__traceback__))
