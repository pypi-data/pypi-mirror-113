# random-strings

Generate strings that are ✨ random ✨

## how to install

```bash
$ pip install random-strings
```

## how to use

```python

>>> from random_strings import random_string
>>> random_string(5)
'YSuz5'

```

## advanced usage

```python
from random_strings import random_hex, random_string as randstr

password = randstr(16)
SECRET_KEY = randstr(64)
verification_code = randstr(12)
verification_code = randstr(12,upper=False) # no uppercase letters
verification_code = randstr(12,lower=False,digit=False) # only uppercase letters
SECURE_TOKEN = random_hex(128)

```

## more examples

```python

>>> from random_strings import *

>>> random_hex(16)
'ec583ef0aaa226cba9cb07e3dc2e623c'

>>> random_uuid()
'85273146-3ad8-489f-9964-e7af16ab6a26'

>>> random_uuid(dashes=False)
'a33ee36ad08242e4a2a819147f084a51'
```

## more details

Generated strings are suitable for cryptographically secure usecase

See `os.urandom`, `random.SystemRandom` and PEP 506 for more details on how it works.
