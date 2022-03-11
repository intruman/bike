import inspect
import datetime
from typing import Any


class Field:
    def __new__(cls, *args, **kwargs):
        members = inspect.getmembers(cls)
        obj = super().__new__(cls)
        return obj

    def __init__(
            self,
            default: Any = None,
            *,
            field_type=str,
            name: str = '',
            null: bool = True,
            alias: str = ''
    ):
        self.default = default
        self.type = field_type
        self.name = name
        self.null = null
        self.alias = alias
        self.required: bool = True
        self.list: bool = False
        self.object: bool = False
        self.model = None
        self.validators_pre = []
        self.validators_pos = []

    def prepare_value(self, value, instance):
        if (value is None or value == '') and self.required:
            if self.default is not None:
                return self.default
            else:
                raise Exception(f'Field {self.name} required.')
        for validator in self.validators_pre:
            value = validator(instance, value)
        if not value:
            value = self.default or None
        if self.type == int:
            value = int(value)
        if self.type == datetime.datetime:
            value = datetime.datetime.strptime(value)
        if self.type == datetime.date:
            value = datetime.datetime.strptime(value, '%Y-%m-%d').date()
        if self.type == float:
            value = float(value)
        if self.type == bool:
            value = True if value == 'true' else False
        if self.list:
            value = [self.type(**item) for item in value]
        for validator in self.validators_pos:
            value = validator(instance, value)
        return value
