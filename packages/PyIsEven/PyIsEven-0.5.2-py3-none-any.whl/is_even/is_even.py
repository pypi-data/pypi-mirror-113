import requests
from functools import lru_cache
from retry import retry
from typing import Union


@lru_cache(maxsize=None)
@retry(ConnectionError, tries=3, delay=2)
def is_even(number: Union[str, int]) -> bool:
    n = int(number)
    r = requests.get(f"https://api.isevenapi.xyz/api/iseven/{n}/")

    if r.status_code == requests.codes.ok:
        return r.json()["iseven"]
    else:
        raise Exception(r.json()["error"])


def is_odd(number: Union[str, int]) -> bool:
    return not is_even(number)


if __name__ == '__main__':

    for i in range(10):
        if is_even(i):
            print(f"{i} is even")
        else:
            print(f"{i} is odd")

    print("second run with cache memo")

    for i in range(10):
        if is_even(i):
            print(f"{i} even")
        else:
            print(f"{i} is odd")
