## Documentation for bacx utils
Last update: 25.06.2021

* [Namedict](#namedict)
* [Config](#config)

### Namedict:

Namedict is an immutable python dictionary, which supports key access by attribute call. Namedict can be crated by
non-recursive constructor `Namedict()` or by recursive static method `Namedict.from_obj()`:

```python
from bacx.utils.namedict import Namedict

# Only first layer keys:
nd = Namedict({'a': 1, 'b': {'c': 2}})
nd.a  # returns 1
nd.b.c  # this would fail
# Recursive:
nd = Namedict.from_obj({'a': 1, 'b': {'c': 2}})
nd.b.c  # returns 2
```

Namedict instance can't be modified, but it can be converted back to python dictionary, modified, and converted back to
Namedict:

```python
from bacx.utils.namedict import Namedict

nd = Namedict.from_obj({'a': 1, 'b': {'c': 2}})
dic = nd.to_obj()
dic['b']['c'] = 3
nd = Namedict.from_obj(dic)
nd.b.c  # returns 3
```

Namedict supports also python dictionary like access:

```python
nd['key']
```

As Namedict keys can be accessed as attribute, they can contain only letters, numbers, underscores, and they can't be
strings reserved in Namespace class (for example 'from_obj'). More precisely, they must satisfy this regex:

```regexp
"^[A-Za-z][A-Za-z0-9_]*$"
```

### Config:

Config is Namedict (see above), which can be created from yaml file:

```python
from bacx.utils.config import Config

# three options:
with open('conf.yaml', 'r') as file:
    cf = Config(file)
cf = Config(path='conf.yaml')
cf = Config(data={'a': 1, 'b': {'c': 2}})

```

Config supports also [yamale](https://github.com/23andMe/Yamale) schema checking:

```python
from bacx.utils.config import Config

cf = Config(path='config.yaml')
try:
    cf.check_yamale_schema(path="/path/to/schema.yaml")
except ValueError as e:
    print("Config does not satisfy yamale schema.")
```

Moreover, values in Config can be replaced by calling `set_in(...)` method. New Config will be returned:

```python
from bacx.utils.config import Config

cf1 = Config(data={'a': 1, 'b': {'c': 2}})
cf2 = cf1.set_in('a', 10)
cf2.a  # returns 10

# for more details see:
print(Config.set_in.__doc__)
```

Config supports also merging functionality:

```python
from bacx.utils.config import Config

cf1 = Config(data={'a': 1, 'b': {'c': 10}})
cf2 = Config(data={'a': 2, 'b': {'c': 11, 'd': 12}})
cf3 = Config(data={'a': 3, 'b': {'e': 13}})
dic = {'b': {'c': 2.5, 'f': 14}}
cf4 = cf1.merge_config(cf2, cf3, dic)
cf4.a  # returns 3
cf4.b  # returns {'c': 2.5, 'd': 12, 'e': 13, 'f': 14}

# for more details see:
print(Config.merge_config.__doc__)
```

