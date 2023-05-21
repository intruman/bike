# bike
A lightweight model validator for modern projects.

## Instalation
```shell
pip install bike
```

## First Pedals

Lets define a simple model to represent a person.

```python hl_lines="1"
import bike


@bike.model()
class Person:
    name: str
    height: float
    weight: float
    
...

p1 = Person(
    name='Patrick Love', 
    height=75, 
    weight=180
)
```
A Person instance can be created passing the attributes.
Also can be instantiated by a dict.
```python
...

data = {
    'name': 'Patrick Love',
    'height': 75,
    'weight': 180
}

p1 = Person(**data)
```

## Nested Models

We can create and mananger more complex structs by nested
models. It's simply by using a model as field type of other model.

```python
# implement.py
import bike


@bike.model()
class Address:
    address_1: str
    address_2: str = ''
    city: str
    state: str
    code: str
    country: str

    
@bike.model()
class Phone:
    country_code: str
    local_code: str
    number: str

    
@bike.model()
class Person:
    name: str
    address: Address
    phones: list[Phone]
    
...
    
payload = {
    'name': 'Aline Mark',
    'address': {
        'address_1': '239 W 45th St',
        'address_2': '',
        'city': 'New York',
        'state': 'NY',
        'code': '10036',
        'country': 'EUA'
    },
    'phones': [
        {
            'country_code': '+1',
            'local_code': '010',
            'number': '134354325'
        },
        {
            'country_code': '+2',
            'local_code': '011',
            'number': '134565436'
        }
    ]
}
p1 = Person(**payload)
print(p1.phones[0].country_code)
# +1
print(p1.phones[1].local_code)
# 011
print(p1.address.state)
# NY
```

## Parsing to Json and Dict

We can parse data to dict or json by using
.dict() or json() methods respectively.

```python
import bike


@bike.model()
class Make:
    name: str
    country: str

    
@bike.model()
class Car:
    name: str
    make: Make
    

m1 = Make(name='Nissan', country='JP')
c1 = Car(name='Leaf', make=m1)

c1_dict = c1.dict()
print(c1_dict['make']['country'])
# JP

c1_json = c1.json()
print(c1_json)
# {"name": "Leaf", "make": {"name": "Nissan", "country": "JP"}}
```

## Validating Fields

Fields can be validated adding the validator annotation.

```python
import bike


@bike.model()
class Character:
    name: str
    health: float = 1.0

    @bike.validator('name')
    def name_validator(cls, val):
        return val.title()
    
    @bike.validator('health')
    def health_validator(cls, val):
        if val < 0: 
            return 0.0
        elif val > 1:
            return 1.0
        return val
    
    
c1 = Character(name='ninki walker', health=2.0)
print(c1.name)
# Ninki Walker
print(c1.health)
# 1.0
```
