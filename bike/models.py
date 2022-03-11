import inspect
import json
import types
from typing import Set, Dict

from .fields import Field


__validators__ = {}


class ModelMetaclass(type):
    def __new__(mcs, *args, **kwargs):
        members = inspect.getmembers(mcs)
        return mcs


class FieldsList:
    ...


class Model:
    __fields__ = FieldsList()
    __fields_type_list__ = []

    def __new__(cls, *args, **kwargs):
        members = inspect.getmembers(cls)
        obj = super(Model, cls).__new__(cls)
        for key, value in kwargs.items():
            setattr(obj, key, value)
        return obj

    def dict(
            self,
            *,
            alias: bool = False,
            null: bool = True,
            excludes: Set = None
    ) -> Dict:
        if not excludes:
            excludes = set()
        dic = {}
        for field in self.__fields__.values():
            if field.name in excludes:
                continue
            if not null and self.__dict__[field.name] is None:
                continue
            if alias:
                dic[field.alias or field.name] = self.__dict__[field.name]
            else:
                dic[field.name] = self.__dict__[field.name]
        for name in self.__fields_type_list__:
            dic[name] = [item.dict() for item in dic[name]]
        return dic

    def json(self):
        dic = self.dict()
        jsn = json.dumps(dic)
        return jsn


def get_fields_from_annotations(fields, annotation, model):
    fields_list = []
    fields_object = []
    for name, typee in annotation.items():
        if name not in fields:
            field = Field(field_type=typee, name=name)
            field.model = model
            if name in __validators__:
                validators = __validators__[name]
                for vali in validators:
                    if vali['pre']:
                        field.validators_pre.append(vali['func'])
                    else:
                        field.validators_pos.append(vali['func'])
                del __validators__[name]
            opts = typee.__dict__
            if '__origin__' in opts:
                args = typee.__args__
                origin = typee.__origin__
                field.type = args[0]
                if len(args) > 1:
                    if isinstance(args[-1], type(None)):
                        field.required = False
                field.list = origin == list
                field.object = origin == dict
                if field.list:
                    fields_list.append(name)
                if field.object:
                    fields_object.append(name)
            fields[name] = field
    return fields, fields_list, fields_object


def create_init_function():
    def init(self, *args, **kwargs):
        fields = self.__fields__
        for k, field in fields.items():
            value = kwargs.get(k, None)
            value = field.prepare_value(value, self)
            setattr(self, k, value)
    return init


def model():
    def wrapper(cls):
        members = inspect.getmembers(cls)
        fields = {}
        for member in members:
            key, value = member
            if not key.startswith('__'):
                if type(value) == Field:
                    field = fields[key]
                    value.name = field.name
                    value.null = field.null
                    value.type = field.type
                    fields[key] = value
                elif isinstance(value, types.FunctionType):
                    continue
                else:
                    fields[key].default = value
                continue
            if key == '__annotations__':
                fields, fields_list, fields_object = get_fields_from_annotations(fields, value, cls)
        cls.__fields__ = fields
        cls.__fields_type_list__ = fields_list
        cls.__fields_type_object__ = fields_object
        cls.__init__ = create_init_function()
        cls.dict = Model.dict
        cls.json = Model.json
        return cls
    return wrapper


def validator(field, pre=False):
    def wrapper(fnc, *args, **kwargs):
        if field not in __validators__:
            __validators__[field] = []
        __validators__[field].append({'func': fnc, 'pre': pre})
        return fnc
    return wrapper

