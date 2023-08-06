# mcpackutil
[![PyPI](https://img.shields.io/pypi/v/mcpackutil.svg)](https://pypi.python.org/pypi/mcpackutil)
[![PyPI](https://img.shields.io/pypi/pyversions/mcpackutil.svg)](https://pypi.python.org/pypi/mcpackutil)

[![PyPI](https://img.shields.io/pypi/dd/mcpackutil.svg)](https://pypi.python.org/pypi/mcpackutil)
[![PyPI](https://img.shields.io/pypi/dw/mcpackutil.svg)](https://pypi.python.org/pypi/mcpackutil)
[![PyPI](https://img.shields.io/pypi/dm/mcpackutil.svg)](https://pypi.python.org/pypi/mcpackutil)

A CLI application for working with Minecraft resource packs

## Installation
### Via PIP
If you have `pip` installed, you can run;
```
pip install mcpackutil
```
This will install both the library and CLI tool. The CLI tool can then be used via `mcpackutil`, given the directory it was installed to is in your `PATH`
### Via Just
If you want to build the library and/or CLI tool locally and have `just` installed, you can run
```
just build
```
To install both the library and CLI tool or;
```
just build-exe
```
To build just the executable or;
```
just build-lib
```
To build just the Python library as a wheel

