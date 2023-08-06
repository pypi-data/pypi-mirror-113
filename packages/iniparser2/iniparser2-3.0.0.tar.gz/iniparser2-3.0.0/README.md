# iniparser2
  
[![Build Status](https://travis-ci.com/HugeBrain16/iniparser2.svg?branch=main)](https://travis-ci.com/HugeBrain16/iniparser2)  
  
**iniparser2** is An INI parser or a Config parser.  
  
this package is the improved version of [**iniparser**](https://github.com/HugeBrain16/iniparser) with more features.
  
---
  
## Installation
- using pip
    - from pypi
        - `pip install iniparser2`
        - `pip install iniparser2 --upgrade`
    - from github repository
        - `pip install git+https://github.com/HugeBrain16/iniparser2.git`
    - from source
        - `pip install .`
- from source
    - `python setup.py install`
  
## Examples
#### read string
```py
import iniparser2

string = """
[me]
name = josh
age = 0
"""

parser = iniparser2.INI()
parser.read(string)

print(parser)
```
  
#### using parser methods
```py
import iniparser2

parser = iniparser2.INI()

parser.set_section("me")
parser.set("name", "josh", section="me")
parser.set("age", 0, section="me")

print(parser)
```

or

```py
import iniparser2

parser = iniparser2.INI()
parser.set_section("me")
parser["me"]["name"] = "josh"
parser["me"]["age"] = 0

print(parser)
```
    
#### read from file
```py
import iniparser2

parser = iniparser2.INI()
parser.read_file("filename.ini")

print(parser)
```
  
#### read-write file
`file.ini`
```ini
car = 1
bike = 1
```
  
`main.py`
```py
import iniparser2

parser = iniparser2.INI(convert_property=True)
parser.read_file("file.ini")

parser.set("car", parser.get("car") + 1)
parser.remove_property("bike")

parser.write("file.ini")
parser.read_file("file.ini")

print(parser)
```

or 

```py
import iniparser2

parser = iniparser2.INI(convert_property=True)
parser.read_file("file.ini")

parser["car"] += 1
del parser["bike"]

parser.write("file.ini")
parser.read_file("file.ini")

print(parser)
```

### Exceptions
exceptions because why not
  
- base exception
    - `ParsingError`
        - `ParseSectionError`
        - `ParsePropertyError`
        - `ParseDuplicateError`
- something else
    - `DuplicateError`
    - `PropertyError`
    - `SectionError`