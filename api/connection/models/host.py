from mongoengine import *

from models.tool import Tool


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
