# i18npy

[![PyPI](https://img.shields.io/pypi/v/i18npy)](https://pypi.org/project/i18npy/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/i18npy)](https://github.com/marverix/i18npy/actions/workflows/tests.yml)
[![Codecov](https://img.shields.io/codecov/c/gh/marverix/i18npy?token=NPX0JP4458)](https://app.codecov.io/gh/marverix/i18npy)
[![GitHub](https://img.shields.io/github/license/marverix/i18npy)](https://tldrlegal.com/license/mit-license)

This is Python implementation of [roddeh/i18njs](https://github.com/roddeh/i18njs) (http://i18njs.com/).
It's fully compatible with it's  JSON dictionaries syntax.

## Usage

### Installation

```sh
pip install i18npy
```

### Samples

#### With external dictionary and global i18n instance

pl.json

```json
{
  "values": {
    "Hello World": "Witaj świecie",
    "I have %n cookies": [
      [null, null, "Nie ma rączek, nie ma ciasteczek"],
      [0, 0, "Nie mam ciasteczek"],
      [1, 1, "Mam jedno ciasteczko"],
      [2, 4, "Mam %n ciasteczka"],
      [5, null, "Mam %n ciasteczek"]
    ]
  }
}

```

code

```python
from i18npy import i18n, i18n_load

i18n_load("./pl.json")

i18n("Hello World")
# Witaj świecie

KEY = "I have %n cookies"
i18n(KEY, None)
# Nie ma rączek, nie ma ciasteczek

i18n(KEY, 0)
# Nie mam ciasteczek

i18n(KEY, 1)
# Mam jedno ciasteczko

i18n(KEY, 3)
# Mam 3 ciasteczka

i18n(KEY, 5)
# Mam 5 ciasteczek
```

#### Create translator instances

```python
import i18npy

lang_pl = i18npy.create({
  "values": {
    "Hello World": "Witaj świecie",
    "I have %n cookies": [
      [None, None, "Nie ma rączek, nie ma ciasteczek"],
      [0, 0, "Nie mam ciasteczek"],
      [1, 1, "Mam jedno ciasteczko"],
      [2, 4, "Mam %n ciasteczka"],
      [5, None, "Mam %n ciasteczek"]
    ]
  }
})

lang_pl.translate("Hello World")
# Witaj świecie

lang_pl.translate("I have %n cookies", 3)
# Mam 3 ciasteczka
```

## Word of appreciation 

The original i18njs library ha been written by [roddeh](https://github.com/roddeh/).
The library code is based on his code, which is also licensed by MIT.

## License

This project is licensed under MIT License - see the [LICENSE](LICENSE) file for details.
