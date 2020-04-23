import json
import os


def read_file(path: str) -> str:
    with open(os.path.realpath(path)) as f:
        return f.read().strip()


def read_json_file(path: str) -> object:
    with open(os.path.realpath(path)) as f:
        return json.load(f)
