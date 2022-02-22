import datetime
import math

from mongoengine import *


class Tool(EmbeddedDocument):
    """This class is a DRM (Document Relational Model) for mongoDB. This class defines \
    the Tool embedded objects. These represent tools installed on systems.  \
    As on `EmbeddedDocument` it doesn't have it's own collection in monogdb but it can \
    be added as a member of the Host.tools list.
    """

    tool_name = StringField(required=True)
    last_seen = DateTimeField(default=datetime.datetime.now().timestamp())
    first_seen = DateTimeField(default=datetime.datetime.now().timestamp())
    total_beacons = LongField(default=0)

    def toDict(self):
        return {
            'tool_name': self.tool_name,
            'last_seen': math.floor(self.last_seen.timestamp()),
            'first_seen': math.floor(self.first_seen.timestamp()),
            'total_beacons': self.total_beacons
        }


class Tool_description(Document):
    """This class is a DRM (Document Relational Model) for mongoDB. This class defines \
    the tool_description objects. These are only used for the UI to communicate with \
    users how tools should be used and who to reach out to in the event of an error.
    """
    tool_name = StringField(required=True, unique=True)
    poc = StringField()
    usage = StringField()

    def toDict(self):
        return {
            'tool_name': self.tool_name,
            'poc': self.poc,
            'usage': self.usage
        }
