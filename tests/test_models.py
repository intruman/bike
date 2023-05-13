from typing import Optional
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

    data = {
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

    ...

    p1 = Person(**data)
    assert p1.phones[0].country_code == '+1'
    assert p1.phones[1].country_code == '+2'
    assert p1.phones[1].local_code == '011'
    assert p1.address.state == 'NY'

    ...

    json_str = p1.json()
    assert json_str != ''


def test_json_parser_models():
    @bike.model()
    class Make:
        name: str
        country: str

    @bike.model()
    class Car:
        name: str
        make: Make

    ...

    data = {
        'name': 'Leaf',
        'make': {
            'name': 'Nissan',
            'country': 'JP'
        }
    }
    import json
    json_str_base = json.dumps(data)

    ...

    c1 = Car(**data)
    assert c1.make.name == 'Nissan'

    ...

    json_str = c1.json()
    assert json_str == json_str_base
