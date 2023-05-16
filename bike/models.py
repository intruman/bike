import inspect
import json
import types
from typing import Set, Any

import bike
from .fields import Field


__validators__ = {}
types_default = {
    'str': '""',
    'int': '0',
    'float': '0.0',
    'bool': 'False'
}


class ModelMetaclass(type):
    def __new__(mcs, *args, **kwargs):
        members = inspect.getmembers(mcs)
        return mcs


class FieldsList:
    def __get__(self, obj):
        ...

    def __set__(self, obj, value):
        ...


def create_init_function(fields):
    params_required_txt = ''
    params_optional_txt = ''
    body_fn = ''
    for k, field in fields.items():
        if field.object:
            param = f'{k}: dict | Any'
        else:
            param = f'{k}: {field.type.__name__}'
        if field.required:
            if field.default:
                param = f"{param} = '{field.default}'"
                params_optional_txt = f'{params_optional_txt}, {param}' if params_optional_txt else param
            else:
                params_required_txt = f'{params_required_txt}, {param}' if params_required_txt else param
        else:
            default = field.default or types_default.get(field.type.__name__, "None")
            param = f'{param} = {default}'
            params_optional_txt = f'{params_optional_txt}, {param}' if params_optional_txt else param
        statement = f'self.{k} = {k}'
        body_fn += f'\t{statement}\n'
    params_txt = f'*, {params_required_txt}, {params_optional_txt}'
    init_fn = f'def __init__(self, {params_txt}):\n{body_fn}'
    ns = {}
    exec(init_fn, None, ns)
    return ns['__init__']


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


def prepare_class_members(members):
    ret = {mb[0]: mb[1] for mb in members}
    return ret


def prepare_fields(cls):
    members = {mb[0]: mb[1] for mb in inspect.getmembers(cls)}
    annotations = cls.__annotations__
    fields, fields_list, fields_object = get_fields_from_annotations(cls, annotations=annotations, members=members)
    class_name = cls.__name__
    if issubclass(cls, Model):
        for name, field in fields.items():
            setattr(cls, name, field)
    elif not hasattr(cls, '__ready__') and not issubclass(cls, Model):
        cls = type(class_name, (Model,), {**fields, })
    cls.__fields__ = fields
    cls.__fields_type_list__ = fields_list
    cls.__fields_type_object__ = fields_object
    cls.__name__ = class_name
    cls.__ready__ = True
    init_fn = create_init_function(fields)
    setattr(cls, '__init__', init_fn)
    return cls


def get_fields_from_annotations(cls, annotations=None, members=None):
    annotations = annotations or {}
    members = members or {}
    fields = {}
    fields_list = []
    fields_object = []
    for name, typee in annotations.items():
        if name not in fields:
            if name in members:
                value = members[name]
                if isinstance(value, Field):
                    field = value
                    field.name = name
                    field.type = typee
                else:
                    field = Field(field_type=typee, name=name, default=value)
            else:
                field = Field(field_type=typee, name=name)
            # field.model = model
            if name in __validators__:
                validators = __validators__[name]
                for vali in validators:
                    if vali['pre']:
                        field.validators_pre.append(vali['func'])
                    else:
                        field.validators_pos.append(vali['func'])
                del __validators__[name]
            opts = typee.__dict__
            args = getattr(typee, '__args__', ())
            if args and typee.__name__ == 'list':
                field.list = True
                field.list_type = args[0]
            if inspect.isclass(typee) and issubclass(typee, bike.Model):
                field.object = True
                field.list_type = typee
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


class Model:
    __fields__: dict = {}
    __fields_type_list__: list = []

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '__ready__'):
            cls = prepare_fields(cls)
        obj = super(Model, cls).__new__(cls)
        return obj

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def __str__(self):
        return f'{self.__class__.__name__}()'

    def __eq__(self, other) -> bool:
        equal = True
        for f_name in self.__fields__.keys():
            equal = getattr(self, f_name) == getattr(other, f_name)
            if not equal:
                break
        return equal

    def dict(
            self,
            *,
            alias: bool = False,
            null: bool = True,
            excludes: Set = None
    ) -> dict:
        if not excludes:
            excludes = set()
        dic = {}
        for field in self.__fields__.values():
            if field.name in excludes or (not null and self.__dict__[field.name] is None):
                continue
            if alias:
                dic[field.alias or field.name] = self.__dict__[field.name]
            else:
                value = getattr(self, field.name)
                if isinstance(value, list):
                    value = [item.dict() if isinstance(item, bike.Model) else item for item in value]
                elif isinstance(value, bike.Model):
                    value = value.dict()
                dic[field.name] = value
        for name in self.__fields_type_list__:
            dic[name] = [item.dict() for item in dic[name]]
        return dic

    def json(self) -> str:
        dic = self.dict()
        jsn = json.dumps(dic)
        return jsn
