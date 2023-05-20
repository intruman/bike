import datetime
from typing import Any


class Field:
    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        return obj

    def __init__(
            self,
            default: ... = None,
            *,
            field_type: type = str,
            name: str = '',
            null: bool = True,
            alias: str = '',
            prefix: str = ''
    ):
        self.default = default
        self.type = field_type
        self.name = name
        self.null = null
        self.alias = alias
        self.prefix = prefix
        self.alias_load = True
        self.required: bool = True
        self.list: bool = False
        self.list_type = None
        self.object: bool = False
        self.model = None
        self.validators_pre = []
        self.validators_pos = []

    def __str__(self):
        return f'Field:{self.name}({self.type})'

    def __repr__(self):
        return f'Field:{self.name}({self.type})'

    def __get__(self, obj, owner):
        value = getattr(obj, f'_{self.name}')
        return value

    def __set__(self, obj, value):
        value = self.__prepare_value(value, self)
        setattr(obj, f'_{self.name}', value)

    def __prepare_value(self, value, instance):
        if (value is None or str(value) == '') and self.required:
            if self.default is not None:
                return self.default
            else:
                raise Exception(f'Field {self.name} required.')
        for validator in self.validators_pre:
            value = validator(self.model, value)
        if not value:
            value = self.default or None
        if self.list:
            value = [
                self.list_type(**item) if isinstance(item, dict) else self.list_type(item) for item in value
            ]
        elif self.object:
            value = self.list_type(**value) if isinstance(value, dict) else value
        else:
            match self.type:
                case int():
                    value = int(value) if value else None
                case datetime.datetime():
                    value = datetime.datetime.strptime(value, '')
                case datetime.date():
                    value = datetime.datetime.strptime(value, '%Y-%m-%d').date()
                case float():
                    value = float(value)
                case bool():
                    value = True if value == 'true' else False
                case str():
                    value = str(value)
        for validator in self.validators_pos:
            value = validator(instance, value)
        return value

    def set_validators(self, func: callable, pre: bool):
        if pre:
            self.validators_pre.append(func)
        else:
            self.validators_pos.append(func)
