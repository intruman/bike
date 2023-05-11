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


def test_nested_models():
    @bike.model()
    class Phone:
        country_code: str
        local_code: str
        number: str

    @bike.model()
    class Person:
        name: str
        phones: list[Phone]
    ...
    data = {
        'name': 'Aline Mark',
        'phones': [
            {
                'country_code': '+1',
                'local_code': '010',
                'number': '134354325'
            },
            {
                'country_code': '+2',
                'local_code': '010',
                'number': '134565436'
            }
        ]
    }
    ...
    p1 = Person(**data)
    assert p1.phones[0].country_code == '+1'
    assert p1.phones[1].country_code == '+2'