from typing import overload, Union
from .helpers import get_arg, get_arg_type, apply_numbers, apply_formatting


class Translator:
    def __init__(self):
        self.data = None
        self.global_context = {}
        self.extension = None
        self.reset()

    def add(self, dictionary: dict):
        """
        Adds key/value pair data and contexts that are to be used when translating text.
        :param dictionary: The language data:
         {
           "values":{
             "Yes":"はい",
             "No":"いいえ"
           }
         }

        For a more complete example see: http://i18njs.com/i18n/ja.json .
        """

        if "values" in dictionary and dictionary["values"]:
            if not isinstance(dictionary["values"], dict):
                raise TypeError("'values' is not a dictionary")
            for k, v in dictionary["values"].items():
                self.data["values"][k] = v

        if "contexts" in dictionary and dictionary["contexts"]:
            if not isinstance(dictionary["contexts"], list):
                raise TypeError("'contexts' is not a list")
            self.data["contexts"] += dictionary["contexts"]

    def extend(self, ext):
        self.extension = ext

    def set_context(self, key: str, value: str):
        """
        Sets the context globally.
        This context will be used when translating all strings unless a different context
        is provided when calling i18n().
        :param key: The key for the context e.g. "gender"
        :param value: The value for the context e.g. "female"
        """
        self.global_context[key] = value

    def clear_context(self, key: str):
        """
        Clears the context for the given key.
        :param key: The key to clear.
        """
        del self.global_context[key]

    def reset(self):
        """
        Destroys all translation and context data.
        """
        self.reset_data()
        self.reset_context()

    def reset_data(self):
        """
        Destroys all translation data.
        Useful for when you change languages.
        """
        self.data = {"values": {}, "contexts": []}

    def reset_context(self):
        """
        Destroys all context data.
        """
        self.global_context = {}

    @overload
    def translate(self, text: str, context=None) -> Union[str, dict]:
        ...

    @overload
    def translate(self, text: str, formatting: dict, context=None) -> Union[str, dict]:
        ...

    @overload
    def translate(self, text: str, num: int, formatting: dict, context=None) -> Union[str, dict]:
        ...

    @overload
    def translate(self, text: str, default_text: str, context=None) -> Union[str, dict]:
        ...

    @overload
    def translate(self, text: str, default_text: str, formatting: dict, context=None) -> Union[str, dict]:
        ...

    @overload
    def translate(self, text: str, default_text: str, num: int, formatting: dict, context=None) -> Union[str, dict]:
        ...

    def translate(self, text: str, *args) -> Union[str, dict]:
        num = None
        formatting = None
        default_text = None
        context = self.global_context

        if len(args):
            type0 = get_arg_type(args, 0)
            if type0 is str:
                default_text = args[0]
                type1 = get_arg_type(args, 1)
                if type1 is int:
                    num = args[1]
                    formatting = get_arg(args, 2)
                    context = get_arg(args, 3, context)
                elif type1 is dict:
                    formatting = args[1]
                    context = get_arg(args, 2, context)
            elif type0 is int:
                num = args[0]
                formatting = get_arg(args, 1)
                context = get_arg(args, 2, context)
            elif type0 is dict:
                formatting = args[0]
                context = get_arg(args, 1, context)

        if isinstance(text, dict):
            if "i18n" in text and isinstance(text['i18n'], dict):
                text = text['i18n']
            return self._translate_dict(text, context)
        else:
            return self._translate_text(text, num, formatting, context, default_text)

    def _translate_text(self, text: str, num: Union[int, None], formatting: [
                        dict, None], context=None, default_text=None) -> str:

        # If we have failed to find any language data simply use the supplied text.
        if not self.data:
            return apply_formatting(default_text or text, num, formatting)

        result = None

        # Try to get a result using the current context
        context_data = self._get_context_data(self.data, context or self.global_context)
        if context_data:
            result = self._find_translation(text, num, formatting, context_data["values"], default_text)

        # If we didn't get a result with the context then use the non-contextual values
        if not result:
            result = self._find_translation(text, num, formatting, self.data["values"], default_text)

        # If we still didn't get a result then use the original text
        if not result:
            return apply_formatting(default_text or text, num, formatting)

        # Otherwise we got a result so lets use it.
        return result

    def _translate_dict(self, dictionary: dict, context=None) -> dict:
        """
        Translates all the keys in a dictionary.
        Useful for translating the i18n property that exists for some lovely.io packages.
        :param dictionary: Dictionary containing the strings to be translated
        :param context: Context to be used when translating the dict values
        :return: Dictionary
        """
        for k, v in dictionary.items():
            if isinstance(v, str):
                dictionary[k] = self._translate_text(v, None, None, context)
        return dictionary

    def _find_translation(self, text: str, num: Union[int, None],
                          formatting: dict, data: dict, default_text: Union[str, None]):
        if text not in data:
            return None

        value = data[text]
        value_type = type(value)

        if value_type is dict:
            # We are using an extension to translate.
            if self.extension and callable(self.extension):
                value = self.extension(text, num, formatting, value)
                value = apply_numbers(value, num)
                return apply_formatting(value, num, formatting)
            else:
                return apply_formatting(default_text or text, num, formatting)

        a = num is None
        x = value_type is list
        if a and not x:
            if value_type is str:
                return apply_formatting(value, num, formatting)
        else:
            if x:
                for triple in value:
                    b = triple[0] is None
                    c = triple[1] is None
                    d = not a and triple[0] is not None and num >= triple[0]
                    e = not a and triple[1] is not None and num <= triple[1]

                    if a and b and c or not a and (not b and d and (c or e) or b and not c and e):
                        return apply_formatting(triple[2], num, formatting)
        return None

    @staticmethod
    def _get_context_data(data: dict, query: dict) -> Union[dict, None]:
        if "contexts" not in data:
            return None

        for _context in data["contexts"]:
            found = True
            for k, v in query.items():
                if k not in _context["matches"] or _context["matches"][k] != v:
                    found = False
                    break
            if found:
                return _context
        return None
