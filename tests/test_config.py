import os

from tests.fixtures import dummy_simulation
from tokesim.config import config_parser


TEST_CONFIG_DIR = os.path.dirname(__file__)
TEST_CONFIG_PATH = TEST_CONFIG_DIR + "/fixtures/config/test-simulation-config.json"


def test_loading_config() -> None:
    parsed_config = config_parser.parse_config(TEST_CONFIG_PATH)
    assert parsed_config.class_ref == dummy_simulation.DummyModel
    assert parsed_config.accounts["master"] is not None
    assert len(parsed_config.accounts["accounts"]) >= 0
    assert parsed_config.model_params is not None
    assert len(parsed_config.contract_data) >= 0
    assert parsed_config.version is not None
