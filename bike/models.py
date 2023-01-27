import inspect
import json
import types
import typing
from typing import Set, Dict

from .fields import Field


__validators__ = {}


class ModelMetaclass(type):
    def __new__(mcs, *args, **kwargs):
        members = inspect.getmembers(mcs)
        return mcs


class FieldsList:
    def __get__(self, obj):
        ...

    def __set__(self, obj, value):
        ...


class Model:
    __fields__: dict = {}
    __fields_type_list__: list = []

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '__ready__'):
            prepare_fields(cls)
        obj = super(Model, cls).__new__(cls)
        return obj

    def __init__(self, *args, **kwargs):
        for k, field in self.__fields__.items():
            value = kwargs.get(k, None)
            value = field.prepare_value(value, self)
            setattr(self, k, value)

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

    def json(self) -> str:
        dic = self.dict()
        jsn = json.dumps(dic)
        return jsn


def get_fields_from_annotations(cls, annotations: dict = {}):
    fields = {}
    fields_list = []
    fields_object = []
    for name, typee in annotations.items():
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
                name_ = opts['_name']
                field.type = args[0]
                if len(args) > 1:
                    if isinstance(args[-1], type(None)):
                        field.required = False
                if name_ == 'Optional':
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


def create_custom_class(name, fields):
    cls = type(name, (Model,), {**fields, })
    return cls


def prepare_fields(cls):
    members = inspect.getmembers(cls)
    annotations = cls.__annotations__
    fields, fields_list, fields_object = get_fields_from_annotations(cls, annotations=annotations)
    for field in fields:
        ...
    if not hasattr(cls, '__ready__'):
        cls = create_custom_class(cls.__name__, fields)
    cls.__fields__ = fields
    cls.__ready__ = True
    cls.__fields_type_list__ = fields_list
    cls.__fields_type_object__ = fields_object
    return cls


def prepare_db_config(cls, table: str, pk: str = ''):
    cls.__db__ = {
        'table': table if table else cls.__name__.lower(),
        'pk': pk if pk else 'id'
    }
    return cls


def model():
    def wrapper(cls):
        return prepare_fields(cls)
    return wrapper


def db(table: str = '', pk: str = ''):
    def wrapper(cls):
        return prepare_db_config(cls, table=table, pk=pk)
    return wrapper


def validator(field, pre=False):
    def wrapper(fnc, *args, **kwargs):
        if field not in __validators__:
            __validators__[field] = []
        __validators__[field].append({'func': fnc, 'pre': pre})
        return fnc
    return wrapper

