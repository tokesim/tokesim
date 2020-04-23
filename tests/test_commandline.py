import glob
import os
import subprocess
from typing import Any


TEST_CONFIG_DIR = os.path.dirname(__file__)
TEST_CONFIG_PATH = TEST_CONFIG_DIR + "/fixtures/config/test-simulation-config.json"


def test_help_command() -> None:
    command = ["python", "-m", "tokesim"]
    command.extend(["--help"])
    output = subprocess.check_output(command).decode("utf-8")
    assert output.find("launches a simulation") > -1
    assert output.find("creates an initial simu") > -1


def init_command(tmpdir: Any) -> str:
    command = ["python", "-m", "tokesim"]
    command.extend(["init", "--dir", str(tmpdir), "--agents", "10"])
    output = subprocess.check_output(command).decode("utf-8")
    return output


def run_command(tmpdir: Any) -> str:
    command = ["python", "-m", "tokesim"]
    command.extend(
        ["run", "--config", f"{str(tmpdir)}/simulation.json", "--port", "2000"]
    )
    output = subprocess.check_output(command).decode("utf-8")
    return output


def test_init_command(tmpdir: Any) -> None:
    output = init_command(tmpdir)
    assert output.find("creating simulation") > -1
    files = [filename for filename in glob.iglob(f"{str(tmpdir)}/**/*", recursive=True)]
    expected_files = set(
        [
            "config_schema.json",
            "simulation.json",
            "contracts/SimpleToken_abi.json",
            "contracts/SimpleToken.bin",
            "simple_token_model.py",
            "simple_token_agent.py",
        ]
    )
    expected_files = set([f"{str(tmpdir)}/{file}" for file in expected_files])
    # assert that the files exist in the initialization directory
    assert len(expected_files.intersection(files)) == len(expected_files)


def skip_test_run_command(tmpdir: Any) -> None:
    command = ["python", "-m", "tokesim"]
    command.extend(["run", "--config", str(tmpdir), "--port", "100"])
    init_command(tmpdir)
    run_command(tmpdir)
