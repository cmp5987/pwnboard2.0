import datetime
import sys
import time
from typing import Any, List

import mongoengine
from mongoengine.errors import NotUniqueError
from pymongo.errors import DuplicateKeyError

if __package__ is None or __package__ == '':
    from models.host import Host  # pragma: no cover
    from models.tool import Tool, Tool_description  # pragma: no cover
else:
    from connection.models.host import Host
    from connection.models.tool import Tool, Tool_description


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
        """Delete the Host and Tool_description collections. Mostly used for testing
        should not be used mid event.
        """
        Host.drop_collection()
        Tool_description.drop_collection()

    def BuildBoardFromDictList(self, board: List[dict], retry=True) -> List[Host]:
        """Takes in a list of dictionaries defining the board. Modeled after the paragon \
        board. Example board:
        ::
            [
                {
                    "name": "Hulto - web-server",
                    "primary_ip": "10.0.0.1",
                    "os": "LINUX",
                    "service_group": "web-server",
                    "team_name": "Hulto",
                    "tags": ["Linux", "Web", "HTTP"]
                },
                {
                    "name": "Hulto  - mail-server",
                    "primary_ip": "10.0.0.2",
                    "os": "LINUX",
                    "service_group": "mail-server",
                    "team_name": "Hulto",
                    "tags": ["Linux", "mail"]
                    "tools": [{
                        "tool_name": "reptile",
                        "last_seen": 1645500015,
                        "first_seen": 1645500015,
                        "total_beacons": 1
                    }]
                },
            ]


        :param board: A list of JSON dictionaries The primary_ip, service_group, and team_name fields \
        are required others can be used as the need arises.
        :type board: List[Host]

        :return: The board we just built as a List of Host objects, An empty [] will be returned on \
        error or an exception will be raisedd
        :rtype: List[Host]
        """
        backup: List[dict]
        backup = self.GetBoardDict()
        try:
            Host.drop_collection()
            board_host_list = []
            for host in board:
                board_host_list.append(self.createHostDict(host))
        except Exception as e:
            if retry:
                self.BuildBoardFromDictList(backup, retry=False)
            raise e
        return board_host_list

    def GetBoard(self) -> List[Host]:
        """Returns the current board. Pulls all hosts form the database. This may
        eventually become cachedd in redis if performance is an issue.


        :return: The whole board as a List of Host objects, An empty [] will be returned on \
        error or an exception will be raisedd
        :rtype: List[Host]
        """
        board_host_objs: List[Host]
        board_host_objs = []
        for host in Host.objects():
            board_host_objs.append(host)
        return board_host_objs

    def GetBoardDict(self) -> List[dict]:
        """Returns the current board in JSON. Pulls all hosts form the database. This may
        eventually become cached in redis if performance is an issue.


        :return: The whole board as a List of dict, An empty [] will be returned on \
        error or an exception will be raisedd
        :rtype: List[dict]
        """
        board_dict_list: List[dict]
        board_dict_list = []
        for host in Host.objects():
            board_dict_list.append(host.toDict())
        return board_dict_list

    def GetHost(self, primary_ip: str) -> Host:
        """Return Host object matched by primary_ip (the primary key for Host).


        :param primary_ip: The primary_ip used by the Host.
        :type primary_ip: str

        :return: The Host object requested.
        :rtype: Host
        """
        if not isinstance(primary_ip, str):
            raise Exception(f"Expected type string for variable primary_ip\n"
                            f"Recieved {type(primary_ip)}")
        found_host_objs: Host
        found_host_objs = Host.objects(primary_ip=primary_ip).first()
        if found_host_objs == None:
            raise Exception(f"Host {primary_ip} does not exist yet.\n"
                            f"Consider loading a board")
        return found_host_objs

    def createHostDict(self, host_dict: dict) -> Host:
        """Create a new Host object. Derived from a dictionary or
        loaded JSON.
        ::
            {
                "name": "Hulto - web-server",
                "primary_ip": "10.0.0.1",
                "os": "LINUX",
                "service_group": "web-server",
                "team_name": "Hulto",
                "tags": ["Linux", "Web", "HTTP"]
                "tools": [{
                    "tool_name": "reptile",
                    "last_seen": "1645500015",
                    "first_seen": "1645500015",
                    "total_beacons": "1",
                }]
            }


        :param host_dict: The structure defining the Host.
        :type hostdict: dict

        :return: The Host object createdd.
        :rtype: Host
        """
        if not isinstance(host_dict, dict):
            raise Exception(f"Expected dictionary recived {type(host_dict)}")
        if 'primary_ip' not in host_dict.keys() or \
            'service_group' not in host_dict.keys() or \
                'team_name' not in host_dict.keys():
            raise Exception(
                "Required fields not provided:\primary_ip, service_group, team_name")
        newhost = None
        try:
            newhost = self.GetHost(host_dict['primary_ip'])
        except Exception as e:
            # If the host just doesn't exist we'll create a new one.
            if "does not exist yet." not in str(e):
                # If its a different error raise it.
                raise e  # pragma: no cover
        if newhost is None:
            newhost = self.createHost(
                primary_ip=host_dict['primary_ip'],
                team_name=host_dict['team_name'],
                service_group=host_dict['service_group'],
                name=host_dict.get(
                    'name', f"{host_dict['team_name']} - {host_dict['service_group']}"),
                fqdn=host_dict.get('fqdn', 'notset'),
                os=host_dict.get('os', 'notset'),
                tags=host_dict.get('tags', []),
                tools=host_dict.get('tools', []),
            )
        return newhost

    def createHost(
        self, primary_ip: str, name: str, fqdn: str, os: str,
        team_name: str, service_group: str, tags: List[str],
        tools: List[dict]
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
        :param tools: Tools to prepoulate the host with.
        :type tools: List[dict]

        :return: The Host object created.
        :rtype: Host
        """
        tool_objs: List[Tool]
        tool_objs = []
        for tool_dict in tools:
            if "tool_name" not in tool_dict:
                raise Exception("Missing required property tool_name")
            tool_objs.append(
                self.createTool(
                    tool_name=tool_dict['tool_name'],
                    last_seen=float(tool_dict['last_seen']),
                    first_seen=float(tool_dict['first_seen']),
                    total_beacons=tool_dict['total_beacons'],
                )
            )

        newhost = Host(
            primary_ip=primary_ip,
            name=name,
            fqdn=fqdn,
            os=os,
            team_name=team_name,
            service_group=service_group,
            tags=tags,
            tools=tool_objs,
        )
        newhost.save()
        return newhost

    def createTool(self,
                   tool_name: str,
                   last_seen: float = float(
                       datetime.datetime.now().timestamp()),
                   first_seen: float = float(
                       datetime.datetime.now().timestamp()),
                   total_beacons: float = 0,
                   ) -> Tool:
        """Creates a new Tool object given the name.


        :param tool_name: The name of the being recorded.
        :type tool_name: str

        :return: The Tool object created.
        :rtype: Tool
        """
        newTool = Tool(
            tool_name=tool_name,
            last_seen=datetime.datetime.fromtimestamp(last_seen),
            first_seen=datetime.datetime.fromtimestamp(first_seen),
            total_beacons=total_beacons,
        )
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
        tool_obj = None
        # Check if exists
        if host.tools is not None:
            for tool in host.tools:
                if tool.tool_name == tool_name:
                    tool_obj = tool
                    tool_obj.last_seen = datetime.datetime.utcnow
                    tool_obj.total_beacons = tool_obj.total_beacons+1
                    break
        # If Not create
        if tool_obj == None:
            tool_obj = self.createTool(
                tool_name=tool_name,
            )
            host.tools.append(tool_obj)
        host.save()
        return int(tool_obj.total_beacons)

    # Get all hosts that are a part of one of the teams provided
    # in the team_name list. eg. ["Hulto", "squid"] or ["Hulto"]
    def GetTeamHosts(self, team_name: List[str]) -> List[Host]:
        """Filter for hosts from specific teams.


        :param team_name: A list of team names to pull hosts from. `["Hulto","squidli"]`
        :type team_name: List[str]

        :return: A list of hosts belonging to the requested teams, returns [] on error or none foundd.
        :rtype: List[Host]
        """
        host_obj_list: List[Host]
        host_obj_list = []
        for host in Host.objects(team_name__in=team_name):
            host_obj_list.append(host)
        return host_obj_list

    def GetServiceHosts(self, service_group: List[str]) -> List[Host]:
        """Filter for hosts from specific service groups.


        :param service_group: A list of service groups to pull hosts from. `["web-server","ssh-server"]`
        :type team_name: List[str]

        :return: A list of hosts belonging to the requested service groups, returns [] on error or \
        none found.
        :rtype: List[Host]
        """
        host_obj_list: List[Host]
        host_obj_list = []
        for host in Host.objects(service_group__in=service_group):
            host_obj_list.append(host)
        return host_obj_list

    def GetOsHosts(self, oses: List[str]) -> List[Host]:
        """Filter for hosts from specific oses.


        :param oses: A list of oses to pull hosts from. `["Debian","rhel"]`
        :type oses: List[str]

        :return: A list of hosts belonging to the requested oses, returns [] on error or \
        none found.
        :rtype: List[Host]
        """
        host_obj_list: List[Host]
        host_obj_list = []
        for host in Host.objects(os__in=oses):
            host_obj_list.append(host)
        return host_obj_list

    def GetInstalledToolHosts(self, tool_names: List[str]) -> List[Host]:
        """Filter for hosts that have had a tool installed.


        :param tool_names: A list of tool names. If any have called back to pwnboard from a host \
        that host will be returned. `["goofkit","reptile"]`
        :type team_name: List[str]

        :return: A list of hosts belonging to the requested tools, returns [] on error or \
        none foundd.
        :rtype: List[Host]
        """
        host_obj_list: List[Host]
        host_obj_list = []
        for host in Host.objects(tools__tool_name__in=tool_names):
            host_obj_list.append(host)
        return host_obj_list

    def GetNeverActiveToolHosts(self, tool_names: List[str]) -> List[Host]:
        """Filter for hosts that have never had a tool installed.


        :param tool_names: A list of tool names. If a callback has never been seen from one of \
        those tool/host combinations that host will be returned. `["goofkit","reptile"]`
        :type team_name: List[str]

        :return: A list of hosts belonging to the requested tools, returns [] on error or \
        none foundd.
        :rtype: List[Host]
        """
        host_obj_list: List[Host]
        host_obj_list = []
        for host in Host.objects(tools__tool_name__not__in=tool_names):
            host_obj_list.append(host)
        return host_obj_list

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
        host_obj_list: List[Host]
        host_obj_list = []
        for host in Host.objects(tools__tool_name__in=tool_names)\
                .filter(tools__last_seen__lt=datetime.datetime.now()-datetime.timedelta(seconds=timeout_seconds)):
            host_obj_list.append(host)
        return host_obj_list

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
        host_obj_list: List[Host]
        host_obj_list = []
        for host in Host.objects(tools__tool_name__in=tool_names)\
                .filter(tools__last_seen__gte=datetime.datetime.now()-datetime.timedelta(seconds=timeout_seconds)):
            host_obj_list.append(host)
        return host_obj_list

    def Createtool_description(self, tool_name: str, poc: str, usage: str) -> None:
        """Create a tool description object and save it to the DB. Tool Descriptions help users
        better identify and use tools when working with pwnboard.


        :param tool_name: The name of your tool.
        :type team_name: str
        :param poc: The point of contact for the tool used for questions, and trouble shooting.
        :type poc: str
        :param usage: Basic usage instructions to describe what your tool does and how to use it.
        :type usage: str
        """

        tool_descs = self.Gettool_descriptions([tool_name])
        if len(tool_descs) == 0:
            tool_desc = Tool_description(
                tool_name=tool_name,
                poc=poc,
                usage=usage
            )
        else:
            for tool_desc in tool_descs:
                tool_desc.poc = poc
                tool_desc.usage = usage
        tool_desc.save()

    def Gettool_descriptions(self, tool_names: List[str]) -> List[Tool_description]:
        """Get the description objects of multiple tools given a list of tool names.


        :param tool_names: A list of tool names. To pull the Tool Description for.
        :type team_name: List[str]

        :return: A list of tool_descriptio objects based on the names provided, returns [] on error \
        or none foundd.
        :rtype: List[Tool_description]
        """
        tool_descs: List[Tool_description]
        tool_descs = []
        for tool_desc in Tool_description.objects(
                tool_name__in=tool_names):
            tool_descs.append(tool_desc)
        return tool_descs

    def Filter(self, teams: List[str], service_groups: List[str], oses: List[str],
               tool_names: List[str], tool_match: str = "active", timeout: int = 480) -> List[Host]:
        """Given a series of lists (teams, services, osses, and tools) bulid a unique set \
            of the corresponding Hosts.

        :param teams: A list of team names.
        :type teams: List[str]
        :param service_groups: A list of service_groups.
        :type service_groups: List[str]
        :param oses: A list of oses.
        :type oses: List[str]
        :param tool_names: A list of tool names.
        :type tool_names: List[str]
        :param tool_match: Type of matching on tool set. (active, inactive, installed, never present)
        :type tool_match: str
        :param timeout: Number of seconds for a tool to be considered inactive.
        :type timeout: int

        :return: A list of dictionary objects based on the names provided, returns [] on error \
        or none foundd.
        :rtype: List[Tool_description]
        """

        teamSet = set()
        servicesSet = set()
        osesSet = set()
        toolSet = set()
        if len(teams) > 0:
            teamSet = set(self.GetTeamHosts(teams))

        if len(service_groups) > 0:
            servicesSet = set(self.GetServiceHosts(service_groups))

        if len(oses) > 0:
            servicesSet = set(self.GetOsHosts(oses))

        if len(tool_names) > 0:
            if tool_match == "active":
                toolSet = set(self.GetActiveToolHosts(
                    tool_names, timeout_seconds=timeout))
            elif tool_match == "inactive":
                toolSet = set(self.GetTimedOutToolHosts(
                    tool_names, timeout_seconds=timeout))
            elif tool_match == "never":
                toolSet = set(self.GetNeverActiveToolHosts(tool_names))
            elif tool_match == "installed":
                toolSet = set(self.GetInstalledToolHosts(tool_names))

        list_of_sets = [teamSet, servicesSet, osesSet, toolSet]
        # Empty sets evaluate to false,
        # so will be excluded from list comp.
        non_empties = [x for x in list_of_sets if x]
        res = []

        if len(non_empties) > 0:
            solution_set = set.intersection(*non_empties)
            i: Host
            for i in list(solution_set):
                res.append(i.toDict())
        return res

    def GetAllServiceGroups(self) -> List[str]:
        """Get the description objects of multiple tools given a list of tool names.


        :param tool_names: A list of tool names. To pull the Tool Description for.
        :type team_name: List[str]

        :return: A list of tool_descriptio objects based on the names provided, returns [] on error \
        or none foundd.
        :rtype: List[Tool_description]
        """
        service_groups: List[str]
        service_groups = []
        for service_group in Host.objects().distinct("service_group"):
            service_groups.append(service_group)
        return service_groups.sort()
