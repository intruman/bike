from typing import Optional
from dataclasses import dataclass
import bike


def test_instance_model():
    @bike.model()
    class Person:
        name: str
        height: Optional[int]
        weight: float = bike.Field()
        house: str = 'blank'
    ...
    data = {
        'name': 'Patrick Love',
        'height': 75,
        'weight': 180
    }
    ...
    person = Person(**data)
    assert person.name == 'Patrick Love'
    assert person.height == 75
    assert person.weight == 180
    assert person.house == 'blank'
    ...


def tests_nested_models():
    @bike.model()
    class Phone:
        code: str
        number: str

    @bike.model()
    class Person:
        name: str
        phones: list[Phone]
    ...


