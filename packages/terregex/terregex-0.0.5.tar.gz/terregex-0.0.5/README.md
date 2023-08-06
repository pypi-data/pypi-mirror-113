# Terregex
Terregex is structural regex transformation library. 

## Installation
You can install this library via [PyPI](https://pypi.org/project/terregex/).
```
pip install terregex
```

## Getting Started
```py
from terregex import Transformer, Literal

trans = Transformer()

@trans.add_rule()
def transform_literal(node: Literal):
    node.string = node.string.lower()

trans('(Foo|Bar)+') # => '(foo|bar)+'
```
