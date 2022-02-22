import json
from unicodedata import name

from mongoengine import *

try:
    from connection.models.tool import Tool
except Exception as e:  # pragma: no cover
    from models.tool import Tool  # pragma: no cover


class Host(Document):
    """This class is a DRM (Document Relational Model) for mongoDB. This class defines \
    the Host objects. These represent target systems and can be tracked by their various \
    attributes most commonly `team_name` and `service_group`
    """
    primary_ip = StringField(required=True, unique=True)
    name = StringField()
    fqdn = StringField()
    os = StringField(max_length=50)
    team_name = StringField(max_length=50)
    service_group = StringField(max_length=50)
    tags = ListField(StringField())
    tools = ListField(EmbeddedDocumentField(Tool))

    def toDict(self) -> str:
        dictonary = {
            "primary_ip": self.primary_ip,
            "name": self.name,
            "fqdn": self.fqdn,
            "os": self.os,
            "team_name": self.team_name,
            "service_group": self.service_group,
            "tags":  [],
            "tools": []
        }
        for tag in self.tags:
            dictonary['tags'].append(tag)
        for tool in self.tools:
            dictonary['tools'].append(tool.toDict())
        return dictonary
