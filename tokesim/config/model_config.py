import importlib
import sys
from typing import Any

from mypy_extensions import TypedDict


class ModelModuleConfig(TypedDict):
    module_path: str
    module_name: str
    class_name: str


class ModelConfig(TypedDict):
    package: ModelModuleConfig
    params: object
    config: ModelModuleConfig
    dashboard: ModelModuleConfig


def get_module_class(module_config: ModelModuleConfig) -> Any:
    sys.path.insert(0, module_config["module_path"])
    try:
        module = importlib.import_module(module_config["module_name"])
        return getattr(module, module_config["class_name"])
    except Exception as e:
        print(e)
        raise e
