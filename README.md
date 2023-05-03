# Pyella

[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
[![Build](https://github.com/edeckers/pyella/actions/workflows/test.yml/badge.svg?branch=develop)](https://github.com/edeckers/pyella/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/pyella.svg?maxAge=3600)](https://pypi.org/project/pyella)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

The Pyella library brings common monads such as [Maybe](https://hackage.haskell.org/package/base/docs/Data-Maybe.html) and [Either](https://hackage.haskell.org/package/base/docs/Data-Either.html) to your Python projects.

These monad implementations are strongly inspired by their Haskell namesakes.

## Requirements

- Python 3.7+

## Installation

```bash
pip3 install pyella
```

## Rationale

Some of the main reasons for writing Pyella were:
- I prefer the more explicit error handling `Eithers` can bring compared to regular Exception handling
- Whenever one of my applications crashes due to an NPE, which are almost always avoidable, I die a little inside. `Maybe` can help with that
- A nice chain of `fmaps`, `binds`, et al looks satisfying to me

By no means am I claiming that this library will prevent all NPEs nor that it will prevent any other errors being thrown, because that's not how Python works. It _does_ however make you think more about what states your application can end up in and how you want to handle them, in my experience.

Also consider the cons though, some of which are outlined pretty nicely in this blogpost that deems _Result types_ such as `Either` [leaky abstractions](https://eiriktsarpalis.wordpress.com/2017/02/19/youre-better-off-using-exceptions/). A very valid point! No reason to ditch them altogether, but defintely a warning to use them wisely.

## The name

It's a nod to Python and sounds like [paella](https://en.wikipedia.org/wiki/Paella) ...that's the intention anyway. Seemed somewhat funny to me at the time and that's pretty much all there is to it.

There's no connection to the actual purpose of the library :)

## Usage

### Maybe

The Maybe type represents values that might or might not have a value, and can in many ways be considered the exact same thing as an `Optional`. It brings some extra functionality though, such as mapping, binding and chaining.

A real-world like example for applying `Maybe` would be reading settings from a config file

```python
from pyella.maybe import Maybe

# Let's say we have a trivial configuration loader function
def load_config(path_to_config:Path) -> Dict[str, Any]:
    with open(path_to_config, "r") as config_handle:
       return json.load(config_handle)

# And assume the config file content looks like this
# {
#   "url": "https://api.github.com/repos/edeckers/pyella"
# }

# We'll build upon this `config_json` variable in the
# examples below
config_json = load_config("/path/to/your.conf.json")
```

Say you want to read the `url` setting

```python
maybe_url = Maybe.of(config_json.get("url"))
print (maybe_url)

# Output:
#
# Just("https://api.github.com/repos/edeckers/pyella")
```

And next the 'api_key'

```python
maybe_api_key = Maybe.of(config_json.get("api_key"))
print (maybe_api_key)

# Output:
#
# Nothing
```

Maybe (!) you want to fallback to another value when the `api_key` is missing from the configuration, let's say to an environment variable

```python
api_key = maybe_api_key.from_maybe(os.getenv("MY_API_KEY"))
print (api_key)

# Output:
#
# <a string representing the api key>
```

And for some more trivial examples

```python
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

Eithers represent values with two possibilities, often an error and success state. It's convention to use `Left` for the error state and `Right` for the success - or the _right_ - state.

A real-world like example for applying `Either` would be the retrieval of a url, something that might _either_ fail or succeed.

```python
from pyella.either import Either, left, lefts, right, rights

# Let's define a very trivial url retriever which returns a
# `Left<int>` or `Right<Response>` depending on the status code
def fetch_some_interesting_url() -> Either[int, Response]:
    response = request.get("https://api.github.com/repos/edeckers/pyella")

    return Either.pure(response) \
        if response.status_code == 200 else \
            left(response.status_code)

# We'll build upon this `error_or_response` variable in the
# examples below
error_or_response = fetch_some_interesting_url()
```

Maybe you want to print the status code

```python
status_code = error_or_response.if_right(200)
print ("Status code", status_code)

# Output:
#
# Status code <status code>
```

Or maybe you're looking for the occurence of a particular string in the response

```python
is_my_string_there = \
    error_or_response \
        .fmap(lambda response:"monad" in response.text) \
        .if_left(False)
print("Is my string there?", is_my_string_there)

# Output:
#
# Left: Is my string there? False
# Right: Is my string there? <True or False depending on occurrence>
```

How about parsing a succcesful response?

```python
# Say we define this trivial response parser
def parse_response(response: Response) -> Either[int, dict]:
    try:
        return Either.of(str(response.json()))
    except:
        return left(-1)
    
error_or_parsed_response =
    error_or_response \
        .fmap(parse_response)
print (error_or_parsed_response)
```

Seems like not such a bad idea at first glance, and it works:

```python
# Output
#
# Left: Right(Left(-1))
# Right: Right(Right({ "name": "pyella" }))
```

...but that nesting is a little confusing, unnecessary and reminds me of the

                        P Y R A M I D  O F  D O O M

      https://en.wikipedia.org/wiki/Pyramid_of_doom_(programming)


Surely there must be a better way to go about this, and there is!

```python
error_or_parsed_response_with_bind =
    error_or_response.bind(parse_response)
print (error_or_parsed_response_with_bind)
   
# Output
#
# Left: Left(-1)
# Right: Right({ "name": "pyella" })
```

That's better! :)

Of course, the value in `Left` has a different meaning now - it's no longer a status code - which is _less than ideal_. A way to deal with this is to introduce a common `Error` type. 

```python
class Error:
    message: str

class HttpReponseError(Error):
    status: int

class ParseError(Error):
    code: int

def fetch_some_interesting_url() -> Either[HttpResponseError, Response]:
    # Use the same implementation as before, but instead of returning
    # Left(<int>) wrap the <int> in a `HttpResponseError` first

def parse_response(response: Response) -> Either[ParseError, dict]:
    # Use the same implementation as before, but instead of returning
    # Left(<int>) wrap the <int> in a `ParseError` first

# Output
#
# Left: Left(HttpResponseError(<status code>) | ParseError(<parse error code>))
# Right: Right({ "name": "pyella" })
```

But at the end of the day you might not even care about the errors. Pyella's got you covered

```python
maybe_response = error_or_parsed_response.to_optional()
print (maybe_response)

# Output
#
# Left: None
# Right: { "name": "pyella" }
```

Or if you prefer to stay within the Pyella domain

```python
maybe_response = error_or_parsed_response.to_maybe()
print (maybe_response)

# Output
#
# Left: Nothing
# Right: Just({ "name": "pyella" })
```

And these are some other, trivial use cases of `Either`

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

chained_result = e1.chain(e2)
# Output:
#
# Right(2)

string_result = \
    e1.either( \
        lambda e:f"FAIL: {e}", \
        lambda v:f"SUCCESS: {v}")

# Output:
#
# SUCCESS: 1
```

## Contributing

See the [contributing guide](CONTRIBUTING.md) to learn how to contribute to the  repository and the development workflow.

## Code of Conduct

[Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## License

MPL-2.0
