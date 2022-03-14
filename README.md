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

```
A Person instance can be created passing the attributes.
```python
person = Person(name='Patrick Love', height=75, weight=180)
```
Also can be instatiated by a dict data.
```python
data = {
    'name': 'Patrick Love',
    'height': 75,
    'weight': 180
}

person = Person(**data)

```



