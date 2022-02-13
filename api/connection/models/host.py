from mongoengine import *

from models.tool import Tool


class Host(Document):
    primary_ip = StringField(required=True, unique=True)
    name = StringField()
    fqdn = StringField()
    os = StringField(max_length=50)
    team_name = StringField(max_length=50)
    service_group = StringField(max_length=50)
    tags = ListField(StringField())
    tools = ListField(EmbeddedDocumentField(Tool))
