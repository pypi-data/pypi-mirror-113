from typing import Union, Tuple


def get_arg(args: Tuple, index: int, default_value=None):
    try:
        return args[index]
    except Exception:
        return default_value


def get_arg_type(args: Tuple, index: int):
    try:
        return type(args[index])
    except Exception:
        return None


def apply_numbers(text: str, num: int) -> str:
    return text.replace("-%n", str(-num)).replace("%n", str(num))


def apply_formatting(text: str, num: Union[int, None], formatting: Union[dict, None]) -> str:
    if isinstance(num, int):
        text = apply_numbers(text, num)
    if formatting:
        for k, v in formatting.items():
            text = text.replace("%{" + k + "}", v)
    return text
