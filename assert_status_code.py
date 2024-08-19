# -*- coding: utf-8 -*-
import json
import requests

# assertion is checked or test a statement or condition and the result


def assert_status_code(resp: requests.Response, code: int):
    try:
        print(resp.status_code)
        assert resp.status_code == code
    except AssertionError as exc:
        print(resp.status_code)
        # print(resp.json())
        print(
            f'There is an error with the API call, {resp.status_code}. Look to error.json file for more detail.')
        with open('error.json', 'w') as text:
            text.write(json.dumps(resp.json(), sort_keys=True, indent=4))
        raise exc
