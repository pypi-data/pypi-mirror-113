import os
# import json
from . import jsn as json

from hashlib import md5
from random import shuffle, randint

from typing import Any, Callable

def md5(string: str):
    from hashlib import md5 as HASH_FN
    return HASH_FN(string.encode()).hexdigest()

def hash_string(string: str, fn: Callable[[str, ], str]=None) -> str:
    """Generate unique ID for a string.
    """
    if fn is None:
        return md5(string.encode()).hexdigest()
    else:
        return fn(string)


## 对字典键值对的唯一性进行哈希
def to_str(data: Any) -> str:
    if isinstance(data, dict):
        ks = sorted(list(data.keys()))
        d = {k: to_str(data[k]) for k in ks}
        return json.dumps(d)
    else:
        return json.dumps(data)

def hash_dict_content(data: dict) -> str:
    s = to_str(data)
    return hash_string(s)

def random_id(length=64, use: str='NAa', chars=''):
    x = {
        'N': '1234567890',
        'a': 'abcdefghijklmnopqrstuvwxyz',
        'A': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'S': '~`!@#$%^&*()_-+=[]{}\|;:\'",.<>/?'
    }
    y = {'N': 10, 'a': 26, 'A': 26, 'S': 33}

    keys = []
    for k in x:
        if k in use:
            keys.append(k)
            chars += x[k]

    chars = [i for i in chars]
    shuffle(chars)

    seq = ''
    for i in range(length):
        seq += chars[randint(0, len(chars)-1)]

    return seq

## 通过链式字符串取出多层哈希的值
## 自动识别键的前n个唯一字符
def get_by_chain(hash, keys, sep='.'):
    """
    Get data from multi-level hash object.
    Args:
        `hash`: `dict` object whose elements are base types or new hash objects.
        `keys`: `str` object as key route where different-level keys are joint by dot.
                For example, `keys="xx.yy.zz"` means `hash['xx']['yy']['zz']`.
        `sep`: separate character used in keys chain, default is dot (`.`).
    Return: 
        data stored in `hash` by specific querying route.
    """
    key_list = keys.split(sep)
    val = hash
    for k in key_list:
        ks = list(val.keys())
        if k in ks:
            val = val[k]
        else:
            possible_ks = []
            for _ks in ks:
                if _ks.startswith(k):
                    possible_ks.append(_ks)
            if len(possible_ks) != 1:
                raise KeyError(f"Key `{k}` not in [{', '.join([str(i) for i in ks])}]")
            val = val[possible_ks[0]]
    return val


class Help:
    """
    Load help docment from multi-level JSON file.
    Args:
        `fp`: `str` object. JSON file, default is "help.json" in current directory.
        `language`: optional "zh" or "en", default is "zh", language of help text.
                    If not provided in the file, return empty string.
    Usage:
        Use `obj[KEYS_CHAIN]` to access data under specific route in `obj` which is
        a `Help` object related to specific JSON file. Especially, elementary key of
        KEYS_CHAIN joined by dot can be a shorted prefix string, as long as there is
        only one actual key starting with the shorter string. Otherwise it will raise
        a `KeyError`.
    """
    def __init__(self, fp=None, language='zh') -> None:
        if fp is None: fp = 'help.json'
        self.data = json.load(fp)
        self.language = language

    def __getitem__(self, index):
        """
        Get data using keys chain.
        Args:
            `index`: `str` object. Different-level keys joint by dot.
        Returns:
            Language-specific data according to the preset language.
        """
        d = get_by_chain(self.data, index)
        return d.get(self.language, '')