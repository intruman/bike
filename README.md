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
Also can be instatiated by a dict data.
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
print(p1.phones[1].local_code)
print(p1.address.state)
```
```shell
$ python implement.py
+1
001
NY
```
The model Person

