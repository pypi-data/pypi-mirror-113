import json
import os.path
from typing import Callable

from .Translator import Translator


i18n_translator = Translator()
i18n = i18n_translator.translate


def _load_translation(file_path: str) -> dict:
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as f:
        return json.loads(f.read())


def load(file_path: str) -> Translator:
    """
    Load i18n JSON file and create a Translator instance
    :param file_path: i18n JSON file path
    :return: Translator instance
    """
    data = _load_translation(file_path)
    return create(data)


def loads(file_path: str) -> Callable:
    """
    Load i18n JSON and create a Translator instance, but return only reference to the translate method
    :param file_path: i18n JSON file path
    :return: Reference to the instance translate method
    """
    instance = load(file_path)
    return instance.translate


def create(data=None) -> Translator:
    """
    Create Translator instance and put data in it
    :param data: The translation data to put
    :return:
    """
    trans = Translator()
    if data:
        trans.add(data)
    return trans


def i18n_load(file_path: str) -> Callable:
    """
    Load i18n JSON into global i18n variable
    :param file_path: i18n JSON file path
    :return: Callable i18n
    """
    data = _load_translation(file_path)
    i18n_translator.add(data)
    return i18n
