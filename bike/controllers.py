import datetime
from decimal import Decimal
from typing import Any


class Controller:
    model = None
    list_fields = []

    async def filter(self):
        return []

    async def detail(self, pk=None):
        return {}

    async def insert(self, data=None):
        return {}

    async def update(self, pk=None, data=None):
        return {}

    async def remove(self, pk=None):
        return {}

    def prepare_list_field(self, item):
        if self.list_fields:
            ret = {}
            for k, v in item.items():
                if k in self.list_fields:
                    ret[k] = v
            return ret
        return item

    def default(self, dct):
        return "dict"

    def json_parser(self, o: Any) -> Any:
        if hasattr(o, "dict"):
            return self.default(o.dict())
        if isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        if isinstance(o, Decimal):
            return float(o)
        return o

