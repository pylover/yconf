# yconf


## Install

```bash
pip install yconf
```

## quickstart

```python
from yconf import loads

yamldoc = '''
foo:
  enabled: true
  title: BAR
  rate: .73
  user: !env USER
  greeting: !shell echo Hello

fruites:
  - cherry
  - melon
  - banana
  - pineapple
'''

obj = loads(ymldoc)
assert obj.foo.enabled
assert obj.title == 'BAR'
assert obj.rate == 0.73
assert obj.fruites == ['cherry', 'melon', 'banana', 'pineapple']
```

## Tutorial

### Parsing

You may user `loads(str)` function to parse `YAML` string, and `load(file)` 
to parse `file-like` object or filename. these functions return a 
`yconf.Meld` object. The `Meld` object is subclass of the Python's dictionary
but in addtion you can access the members by `getattr`, `setattr` and 
`delattr` operations.


```python
meld = loads('foo: bar')
assert meld.foo == 'bar'
```

```python
meld = load('foo.yml')
```

```python
with open('foo.yml') as file:
  meld = load(file)
```

### Merging/Melting

Using the `|=` operator you may merge any other dictionary or `YAML-string` 
into a `Meld`.

```python
meld |= '''
  foo: bar
  baz: 23
'''
```

And also using the `<<=` you may load a file-like object or a filename into a
`Meld` object.

```python
meld <<= 'foo.yml'
```

```python
with open('foo.yml') as file:
  meld <<= file
```


### Dump

Use `yconf.dumps(obj) -> str`, `yconf.dump(obj, file)` and also 
`meld >>= filename`.

```python
dumps(meld, indent=6, indentsize=2)
dump(meld, 'foo.yml', indent=6, indentsize=2)

with open('foo.yml', 'w') as file:
  dump(meld, file, indent=6, indentsize=2)

```

```python
meld >>= 'foo.yml'
```

```python
with open('foo.yml', 'w') as file:
  meld >>= file
```

## Contribution

### Dependencies
Install [python-makelib](https://github.com/pylover/python-makelib).

### Virtualenv

Create virtual environment:
```bash
make venv
```

Delete virtual environment:
```bash
make venv-delete
```

Activate the virtual environment:
```bash
source ./activate.sh
```


### Install (editable mode)
Install this project as editable mode and all other development dependencies:
```bash
make env
```


### Tests
Execute all tests:
```bash
make test
```

Execute specific test(s) using wildcard:
```bash
make test F=tests/test_db*
make test F=tests/test_form.py::test_querystringform
```

*refer to* [pytest documentation](https://docs.pytest.org/en/7.1.x/how-to/usage.html#how-to-invoke-pytest)
*for more info about invoking tests.*

Execute tests and report coverage result:
```bash
make cover
make cover F=tests/test_static.py
make cover-html
```


# Lint
```bash
make lint
```


### Distribution
Execute these commands to create `Python`'s standard distribution packages
at `dist` directory:
```bash
make sdist
make wheel
```


### Clean build directory
Execute: 
```bash
make clean
```
to clean-up previous `dist/*` and `build/*` directories.


### PyPI

> **_WARNING:_** Do not do this if you'r not responsible as author and 
> or maintainer of this project.

Execute
```bash
make clean
make pypi
```
to upload `sdists` and `wheel` packages on [PyPI](https://pypi.org).


## Documentation

```bash
source activate.sh
make doc
make doclive
make doctest
```

Or 

```bash
source activate.sh
cd sphinx
make doctest
make html
make livehtml
```
