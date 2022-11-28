# Pyella

[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
[![Build](https://github.com/edeckers/pyella/actions/workflows/test.yml/badge.svg?branch=develop)](https://github.com/edeckers/pyella/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/pyella.svg?maxAge=3600)](https://pypi.org/project/pyella)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

This library brings common monads such as `Maybe` and `Either` to your Python projects.

## Requirements

- Python 3.7+

## Installation

```bash
pip3 install pyella
```

## Usage

### Maybe

The snippet below demonstrates some of the oprations that are available for `Maybe`.

```python
from pyella.maybe import Maybe

j0 = Maybe.of(1)
print (j0)
# Output: Just(1)

print (j0.from_maybe(-1))
# Output: 1

j1 = j0.fmap(lambda x:x*2)
print(j0)
print(j1)
# Output:
#
# Just(1)
# Just(2)
```

### Either

And these are some things you can do with `Either`.

```python
from pyella.either import Either, left, lefts, right, rights

e0: Either[str, int] = left("invalid value")
print(e0)
# Output: Left(invalid value)

print (e0.if_left(-1))
print (e0.if_right("the value was valid"))
# Output:
#
# -1
# 'invalid value'

e1: Either[str, int] = right(1)
print (e1)
# Output: Right(1)

e2 = e1.fmap(lambda x:x*2)
print(e1)
print(e2)
# Output:
#
# Right(1)
# Right(2)

valid_values = rights([e0, e1, e2])
print (valid_values)
# Output: [1, 2]
```


## Contributing

See the [contributing guide](CONTRIBUTING.md) to learn how to contribute to the  repository and the development workflow.

## Code of Conduct

[Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## License

MPL-2.0
