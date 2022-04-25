from mongoengine import Document, EmbeddedDocument
from mongoengine.queryset import QuerySet
from datetime import datetime


def to_dict(obj):
    if isinstance(obj, (QuerySet, list)):
        return list(map(to_dict, obj))
    elif isinstance(obj, (Document, EmbeddedDocument)):
        doc = {}
        for field_name, field_type in obj._fields.items():
            field_value = getattr(obj, field_name)
            doc[field_name] = to_dict(field_value)
        return doc
    else:
        return obj

import json, bson


def json_response(obj, cls=None):

    return json.loads(json.dumps(obj, cls=cls))

class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bson.ObjectId):
            return str(obj)

        if isinstance(obj, bson.DBRef):
            return str(obj.id)

        if isinstance(obj, datetime):
                return str(obj)

        return json.JSONEncoder.default(self, obj)