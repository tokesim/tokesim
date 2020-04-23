from typing import Any, Callable

import requests


REQUEST_ID = 0


def make_requestor(url: str) -> Callable[[str, Any], Any]:
    global REQUEST_ID
    REQUEST_ID = REQUEST_ID + 1

    def requestor(method: str, params: Any) -> Any:
        payload = {
            "method": method,
            "params": [params],
            "jsonrpc": "2.0",
            "id": REQUEST_ID,
        }
        json_response = requests.post(url, json=payload).json()
        if "result" in json_response:
            return json_response["result"]
        return json_response

    return requestor
