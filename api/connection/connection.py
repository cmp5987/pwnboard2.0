import datetime
import sys
import time
from typing import Any, List

import mongoengine
from mongoengine.errors import NotUniqueError
from pymongo.errors import DuplicateKeyError

if __package__ is None or __package__ == '':
    from models.host import Host
    from models.tool import Tool, ToolDescription
else:
    from connection.models.host import Host
    from connection.models.tool import Tool, ToolDescription


class MongoConnection():
    """This class manages provides a layer of abstraction between the database
    and the web application. This calss provides functions to create and query
    database resources.


    :param mongodb_db: The collection mongodb should use, defaults to pwnboard
    :type mongodb_db: str, optional
    :param mongodb_host: The host mongodb is running on, defaults to 127.0.0.1
    :type mongodb_host: str, optional
    :param mongodb_port: The port mongodb is listening on, defaults to 27017
    :type mongodb_port: str, optional
    """

    conn = None

    def __init__(
            self,
            mongodb_db: str = "pwnboard",
            mongodb_host: str = "127.0.0.1",
            mongodb_port: int = 27017):
        self.conn = mongoengine.connect(
            mongodb_db, host=mongodb_host, port=mongodb_port)

    def WipeCollection(self):
        """Delete the Host and ToolDescription collections. Mostly used for testing
        should not be used mid event.
        """
        Host.drop_collection()
        ToolDescription.drop_collection()

    def BuildBoard(self, board: list) -> List[Host]:
        """Takes in a list of dictionaries defining the board. Modeled after the paragon \
        board. Example board:
        ::
            [
                {
                    "name": "Hulto - web-server",
                    "primaryIP": "10.0.0.1",
                    "os": "LINUX",
                    "serviceGroup": "web-server",
                    "teamName": "Hulto",
                    "tags": ["Linux", "Web", "HTTP"]
                },
                {
                    "name": "Hulto  - mail-server",
                    "primaryIP": "10.0.0.2",
                    "os": "LINUX",
                    "serviceGroup": "mail-server",
                    "teamName": "Hulto",
                    "tags": ["Linux", "mail"]
                },
            ]


        :param board: A list of JSON dictionaries The primaryIP, serviceGroup, and teamName fields \
        are required others can be used as the need arises.
        :type board: List[Host]

        :return: The board we just built as a List of Host objects, An empty [] will be returned on \
        error or an exception will be raisedd
        :rtype: List[Host]
        """
        Host.drop_collection()
        boardobjs = []
        for host in board:
            boardobjs.append(self.createHostDict(host))
        return boardobjs

    def GetBoard(self) -> List[Host]:
        """Returns the current board. Pulls all hosts form the database. This may
        eventually become cachedd in redis if performance is an issue.


        :return: The whole board as a List of Host objects, An empty [] will be returned on \
        error or an exception will be raisedd
        :rtype: List[Host]
        """
        boardobjs = []
        for host in Host.objects():
            boardobjs.append(host)
        return boardobjs

    def GetBoardDict(self) -> List[dict]:
        """Returns the current board in JSON. Pulls all hosts form the database. This may
        eventually become cached in redis if performance is an issue.


        :return: The whole board as a List of dict, An empty [] will be returned on \
        error or an exception will be raisedd
        :rtype: List[dict]
        """
        boardobjs = []
        for host in Host.objects():
            boardobjs.append(host.toDict())
        return boardobjs

    def GetHost(self, primary_ip: str) -> Host:
        """Return Host object matched by primary_ip (the primary key for Host).


        :param primary_ip: The primary_ip used by the Host.
        :type primary_ip: str

        :return: The Host object requested.
        :rtype: Host
        """
        foundhost = Host.objects(primary_ip=primary_ip).first()
        if foundhost == None:
            raise Exception(f"Host {primary_ip} does not exist yet.\n"
                            f"Consider loading a board")
        return foundhost

    def createHostDict(self, hostdict: dict) -> Host:
        """Create a new Host object. Derived from a dictionary or
        loaded JSON.
        ::
            {
                "name": "Hulto - web-server",
                "primaryIP": "10.0.0.1",
                "os": "LINUX",
                "serviceGroup": "web-server",
                "teamName": "Hulto",
                "tags": ["Linux", "Web", "HTTP"]
            }


        :param hostdict: The structure defining the Host.
        :type hostdict: dict

        :return: The Host object createdd.
        :rtype: Host
        """
        if not isinstance(hostdict, dict):
            raise Exception(f"Expected dictionary recived {type(hostdict)}")
        if 'primaryIP' not in hostdict.keys() or \
            'serviceGroup' not in hostdict.keys() or \
                'teamName' not in hostdict.keys():
            raise Exception(
                "Required fields not provided:\nprimaryIP, serviceGroup, team_name")
        newhost = None
        try:
            newhost = self.GetHost(hostdict['primaryIP'])
        except Exception as e:
            if "does not exist yet." not in str(e):
                raise e
        if newhost is None:
            newhost = self.createHost(
                primary_ip=hostdict['primaryIP'],
                team_name=hostdict['teamName'],
                service_group=hostdict['serviceGroup'],
                name=hostdict.get(
                    'name', f"{hostdict['teamName']} - {hostdict['serviceGroup']}"),
                fqdn=hostdict.get('fqdn', 'notset'),
                os=hostdict.get('os', 'notset'),
                tags=hostdict.get('tags', [])
            )
        return newhost

    def createHost(
        self, primary_ip: str, name: str, fqdn: str, os: str,
        team_name: str, service_group: str, tags: List[str]
    ) -> Host:
        """Create a new Host object and save it to the database.


        :param primary_ip: The primary_ip used by the Host.
        :type primary_ip: str
        :param name: A common name used to describe the host.
        :type name: str
        :param fqdn: The fully qualified domain name used by the host.
        :type fqdn: str
        :param os: The os the host is running.
        :type os: str
        :param team_name: The team the host belongs to.
        :type team_name: str
        :param service_group: The service_group the host belongs to.
        :type os: str
        :param tags: Additional tags to identify the host.
        :type tags: List[str]

        :return: The Host object created.
        :rtype: Host
        """

        newhost = Host(
            primary_ip=primary_ip,
            name=name,
            fqdn=fqdn,
            os=os,
            team_name=team_name,
            service_group=service_group,
            tags=tags,
        )
        newhost.save()
        return newhost

    def createTool(self, tool_name: str) -> Tool:
        """Creates a new Tool object given the name.


        :param tool_name: The name of the being recorded.
        :type tool_name: str

        :return: The Tool object created.
        :rtype: Tool
        """
        newTool = Tool(tool_name=tool_name)
        return newTool

    def RegisterCallback(self, primary_ip: str, tool_name: str) -> int:
        """Registers a callback for a tool against an IP.


        :param primary_ip: The primary IP used by the host.
        :type primary_ip: str
        :param tool_name: The name of the being recorded.
        :type tool_name: str

        :return: The total number of beacons recived for that tool/ip combination.
        :rtype: int
        """
        host = self.GetHost(primary_ip=primary_ip)
        toolobj = None
        # Check if exists
        if host.tools is not None:
            for tool in host.tools:
                if tool.tool_name == tool_name:
                    toolobj = tool
                    toolobj.lastseen = datetime.datetime.utcnow
                    toolobj.totalbeacons = toolobj.totalbeacons+1
                    break
        # If Not create
        if toolobj == None:
            toolobj = self.createTool(
                tool_name=tool_name,
            )
            host.tools.append(toolobj)
        host.save()
        return int(toolobj.totalbeacons)

    # Get all hosts that are a part of one of the teams provided
    # in the team_name list. eg. ["Hulto", "squid"] or ["Hulto"]
    def GetTeamHosts(self, team_name: List[str]) -> List[Host]:
        """Filter for hosts from specific teams.


        :param team_name: A list of team names to pull hosts from. `["Hulto","squidli"]`
        :type team_name: List[str]

        :return: A list of hosts belonging to the requested teams, returns [] on error or none foundd.
        :rtype: List[Host]
        """
        hostList = []
        for host in Host.objects(team_name__in=team_name):
            hostList.append(host)
        return hostList

    def GetServiceHosts(self, service_group: List[str]) -> List[Host]:
        """Filter for hosts from specific service groups.


        :param service_group: A list of service groups to pull hosts from. `["web-server","ssh-server"]`
        :type team_name: List[str]

        :return: A list of hosts belonging to the requested service groups, returns [] on error or \
        none found.
        :rtype: List[Host]
        """
        hostList = []
        for host in Host.objects(service_group__in=service_group):
            hostList.append(host)
        return hostList

    def GetInstalledToolHosts(self, tool_names: List[str]) -> List[Host]:
        """Filter for hosts that have had a tool installed.


        :param tool_names: A list of tool names. If any have called back to pwnboard from a host \
        that host will be returned. `["goofkit","reptile"]`
        :type team_name: List[str]

        :return: A list of hosts belonging to the requested tools, returns [] on error or \
        none foundd.
        :rtype: List[Host]
        """
        hostList = []
        for host in Host.objects(tools__tool_name__in=tool_names):
            hostList.append(host)
        return hostList

    def GetNeverActiveToolHosts(self, tool_names: List[str]) -> List[Host]:
        """Filter for hosts that have never had a tool installed.


        :param tool_names: A list of tool names. If a callback has never been seen from one of \
        those tool/host combinations that host will be returned. `["goofkit","reptile"]`
        :type team_name: List[str]

        :return: A list of hosts belonging to the requested tools, returns [] on error or \
        none foundd.
        :rtype: List[Host]
        """
        hostList = []
        for host in Host.objects(tools__tool_name__not__in=tool_names):
            hostList.append(host)
        return hostList

    def GetTimedOutToolHosts(self, tool_names: List[str], timeout_seconds: int) -> List[Host]:
        """Filter for hosts that have a tool installed but haven't see it in timeout_seconds.


        :param tool_names: A list of tool names. If a callback has been seen before but not within \
        the last `tool_names` seconds that host will be returned. `["goofkit","reptile"]`
        :type team_name: List[str]
        :param timeout_seconds: The number of seconds before a tool is counted as timed out.
        :type timeout_seconds: int

        :return: A list of hosts belonging to the requested tools and outside the request timeout, \
        returns [] on error or none foundd.
        :rtype: List[Host]
        """
        hostList = []
        for host in Host.objects(tools__tool_name__in=tool_names)\
                .filter(tools__lastseen__lt=datetime.datetime.now()-datetime.timedelta(seconds=timeout_seconds)):
            hostList.append(host)
        return hostList

    def GetActiveToolHosts(self, tool_names: List[str], timeout_seconds: int) -> List[Host]:
        """Filter for hosts that have a tool installed and have seen it within timeout_seconds.


        :param tool_names: A list of tool names. If a callback has been seen and is within \
        `timeout_seconds` seconds that host will be returned. `["goofkit","reptile"]`
        :type team_name: List[str],

        :param timeout_seconds: The number of seconds before a tool is counted as timed out.
        :type timeout_seconds: int

        :return: A list of hosts belonging to the requested tools and within the request timeout, \
        returns [] on error or none foundd.
        :rtype: List[Host]
        """
        hostList = []
        for host in Host.objects(tools__tool_name__in=tool_names)\
                .filter(tools__lastseen__gte=datetime.datetime.now()-datetime.timedelta(seconds=timeout_seconds)):
            hostList.append(host)
        return hostList

    def CreateToolDescription(self, tool_name: str, poc: str, usage: str) -> None:
        """Create a tool description object and save it to the DB. Tool Descriptions help users
        better identify and use tools when working with pwnboard.


        :param tool_name: The name of your tool.
        :type team_name: str
        :param poc: The point of contact for the tool used for questions, and trouble shooting.
        :type poc: str
        :param usage: Basic usage instructions to describe what your tool does and how to use it.
        :type usage: str
        """

        toolDescs = self.GetToolDescription([tool_name])
        if len(toolDescs) == 0:
            toolDesc = ToolDescription(
                tool_name=tool_name,
                poc=poc,
                usage=usage
            )
        else:
            for toolDesc in toolDescs:
                toolDesc.poc = poc
                toolDesc.usage = usage
        toolDesc.save()

    def GetToolDescription(self, tool_names: List[str]) -> List[ToolDescription]:
        """Get the description objects of multiple tools given a list of tool names.


        :param tool_names: A list of tool names. To pull the Tool Description for.
        :type team_name: List[str]

        :return: A list of ToolDescriptio objects based on the names provided, returns [] on error \
        or none foundd.
        :rtype: List[ToolDescription]
        """
        toolDescs = []
        for toolDesc in ToolDescription.objects(
                tool_name__in=tool_names):
            toolDescs.append(toolDesc)
        return toolDescs
