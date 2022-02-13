import datetime

from mongoengine import *


class Tool(EmbeddedDocument):
    tool_name = StringField(required=True)
    lastseen = DateTimeField(default=datetime.datetime.utcnow)
    firstseen = DateTimeField(default=datetime.datetime.utcnow)
    totalbeacons = IntField(default=0)


class ToolDescription(Document):
    tool_name = StringField(required=True, unique=True)
    poc = StringField()
    usage = StringField()
