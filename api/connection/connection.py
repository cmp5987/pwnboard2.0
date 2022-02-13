import datetime
import sys
import time
from operator import truediv
from typing import Any, List

import mongoengine
from mongoengine.errors import NotUniqueError
from pymongo.errors import DuplicateKeyError

from models.host import Host
from models.tool import Tool, ToolDescription

'''
'''


class MongoConnection():
    conn = None

    def __init__(self,
                 mongodb_db: str = "pwnboard",
                 mongodb_host: str = "127.0.0.1",
                 mongodb_port: int = 27017):
        self.conn = mongoengine.connect(
            mongodb_db, host=mongodb_host, port=mongodb_port)

    def WipeCollection(self):
        Host.drop_collection()
        ToolDescription.drop_collection()

    def BuildBoard(self, board: list):
        boardobjs = []
        for host in board:
            boardobjs.append(self.createHostDict(host))
        return boardobjs

    def GetBoard(self):
        boardobjs = []
        for host in Host.objects():
            boardobjs.append(host)
        return boardobjs

    def GetHost(self, primary_ip: str) -> Host:
        foundhost = Host.objects(primary_ip=primary_ip).first()
        if foundhost == None:
            raise Exception(f"Host {primary_ip} does not exist yet.\n"
                            f"Consider loading a board")
        return foundhost

    def createHostDict(self, hostdict: dict) -> Host:
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
            newhost.save()
        return newhost

    def createHost(self, primary_ip: str, name: str, fqdn: str,
                   os: str, team_name: str, service_group: str,
                   tags: List[str]) -> Host:
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
        newTool = Tool(tool_name=tool_name)
        return newTool

    def RegisterCallback(self, primary_ip: str, tool_name: str) -> dict:
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
        return toolobj.totalbeacons

    # Get all hosts that are a part of one of the teams provided
    # in the team_name list. eg. ["Hulto", "squid"] or ["Hulto"]
    def GetTeamHosts(self, team_name: List[str]) -> List[Host]:
        hostList = []
        for host in Host.objects(team_name__in=team_name):
            hostList.append(host)
        return hostList

    def GetServiceHosts(self, service_group: List[str]) -> List[Host]:
        hostList = []
        for host in Host.objects(service_group__in=service_group):
            hostList.append(host)
        return hostList

    def GetInstalledToolHosts(self, tool_names: List[str]) -> List[Host]:
        hostList = []
        for host in Host.objects(tools__tool_name__in=tool_names):
            hostList.append(host)
        return hostList

    def GetNeverActiveToolHosts(self, tool_names: List[str]) -> List[Host]:
        hostList = []
        for host in Host.objects(tools__tool_name__not__in=tool_names):
            hostList.append(host)
        return hostList

    def GetTimedOutToolHosts(self, tool_names: List[str], timeout_seconds: int) -> List[Host]:
        hostList = []
        for host in Host.objects(tools__tool_name__in=tool_names)\
                .filter(tools__lastseen__lt=datetime.datetime.now()-datetime.timedelta(seconds=timeout_seconds)):
            hostList.append(host)
        return hostList

    def GetActiveToolHosts(self, tool_names: List[str], timeout_seconds: int) -> List[Host]:
        hostList = []
        for host in Host.objects(tools__tool_name__in=tool_names)\
                .filter(tools__lastseen__gte=datetime.datetime.now()-datetime.timedelta(seconds=timeout_seconds)):
            hostList.append(host)
        return hostList

    def CreateToolDescription(self, tool_name: str, poc: str, usage: str) -> None:
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
        toolDescs = []
        for toolDesc in ToolDescription.objects(
                tool_name__in=tool_names):
            toolDescs.append(toolDesc)
        return toolDescs
