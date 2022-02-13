import datetime

from mongoengine import *


class Tool(EmbeddedDocument):
    """This class is a DRM (Document Relational Model) for mongoDB. This class defines \
    the Tool embedded objects. These represent tools installed on systems.  \
    As on `EmbeddedDocument` it doesn't have it's own collection in monogdb but it can \
    be added as a member of the Host.tools list.
    """

    tool_name = StringField(required=True)
    lastseen = DateTimeField(default=datetime.datetime.utcnow)
    firstseen = DateTimeField(default=datetime.datetime.utcnow)
    totalbeacons = IntField(default=0)


class ToolDescription(Document):
    """This class is a DRM (Document Relational Model) for mongoDB. This class defines \
    the ToolDescription objects. These are only used for the UI to communicate with \
    users how tools should be used and who to reach out to in the event of an error.
    """
    tool_name = StringField(required=True, unique=True)
    poc = StringField()
    usage = StringField()
