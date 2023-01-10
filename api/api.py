import json
import re
from distutils.log import debug
from typing import List
from urllib.request import Request
from uuid import uuid4
from xmlrpc.client import ResponseError

from aiohttp import web
from aiohttp_swagger3 import SwaggerDocs, SwaggerUiSettings
from connection.connection import MongoConnection


class API():
    db = None
    app = None
    swagger = None
    routes = web.RouteTableDef()
    redirect_url = "https://cdn.akamai.steamstatic.com"
    port = 5000
    debug = False
    bind_host = "0.0.0.0"
    docs_path = "/docs/"

    def __init__(self, port: int = 5000, bind_host: str = "0.0.0.0",
                 debug: bool = False, redirect_url: str = "https://cdn.akamai.steamstatic.com"):
        self.port = port
        self.debug = debug
        self.bind_host = bind_host
        self.redirect_url = redirect_url
        self.db = MongoConnection()
        self.db, self.app, self.swagger = self.init_app()

    ## Board setup ###
    async def setboard(self, request: web.Request) -> web.Response:
        """
        Create board a for an event.
        The board will represent all the hosts.
        ---
        summary: Create a board for the event.
        tags:
          - Board
        requestBody:
          description: List of host dictionaries to define board state.
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Board'

        responses:
          '200':
            description: Expected response to a valid request
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Board'
        """
        try:
            body = await request.text()
            jsond_doc = json.loads(body)
            _ = self.db.BuildBoardFromDictList(jsond_doc)
            board = self.db.GetBoardDict()
            return web.json_response(board)
        except Exception as e:
            return web.HTTPInternalServerError(text=self.json_error(str(e)))

    async def getboard(self, request: web.Request) -> web.Response:
        """
        Get current board a for an event.
        The board will represent all the hosts.
        ---
        summary: Get board for the event.
        tags:
          - Board

        responses:
          '200':
            description: Expected response to a valid request
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Board'
        """
        try:
            board = self.db.GetBoardDict()
            return web.json_response(board)
        except Exception as e:
            return web.HTTPInternalServerError(text=self.json_error(str(e)))

    async def getboardrows(self, request: web.Request) -> web.Response:
        """
        Get the rows for the board.
        Each service group has a row.
        Each column belongs to a team.
        Each cell representss a host
        ---
        summary: Get board rows for the event. Used by font-end.
        tags:
          - Board

        responses:
          '200':
            description: Expected response to a valid request
            content:
              application/json:
                schema:
                  type: array
                  items:
                    $ref: '#/components/schemas/BoardRow'
        """
        try:
            board = self.db.GetBoardDict()
            rows = {}
            for host in board:
                if host['service_group'] not in rows.keys():
                    rows[host['service_group']] = {}
                    rows[host['service_group']]['service_group'] \
                        = host['service_group']
                    rows[host['service_group']]['team_and_hosts'] = []

                rows[host['service_group']
                     ]['team_and_hosts'].append({'team_name': host['team_name'], 'host': host})

            res = []
            for row_key in rows.keys():
                res.append(rows[row_key])

            return web.json_response(res)
        except Exception as e:
            return web.HTTPInternalServerError(text=self.json_error(str(e)))

    ## Get row / column names ##

    async def getteamnames(self, request: web.Request) -> web.Response:
        """
        Get a list of all team names
        ---
        summary: Get a list of all team names
        tags:
          - Board

        responses:
          '200':
            description: Expected response to a valid request
            content:
              application/json:
                schema:
                  type: array
                  items:
                      type: string
        """
        try:
            team_names = self.db.GetAllTeamNames()
            return web.json_response(team_names)
        except Exception as e:
            return web.HTTPInternalServerError(text=self.json_error(str(e)))

    async def getservicegroups(self, request: web.Request) -> web.Response:
        """
        Get a list of all service groups
        ---
        summary: Get a list of all service groups
        tags:
          - Board

        responses:
          '200':
            description: Expected response to a valid request
            content:
              application/json:
                schema:
                  type: array
                  items:
                      type: string
        """
        try:
            service_groups = self.db.GetAllServiceGroups()
            return web.json_response(service_groups)
        except Exception as e:
            return web.HTTPInternalServerError(text=self.json_error(str(e)))

    ## Tool names and descriptions ##

    async def gettoolnames(self, request: web.Request) -> web.Response:
        """
        Get a list of all tool names.
        ---
        summary: Get a list of all tool names.
        tags:
          - Tool

        responses:
          '200':
            description: Expected response to a valid request
            content:
              application/json:
                schema:
                  type: array
                  items:
                      type: string
        """
        try:
            tool_names = self.db.GetAllToolNames()
            return web.json_response(tool_names)
        except Exception as e:
            return web.HTTPInternalServerError(text=self.json_error(str(e)))

    async def settooldescription(self, request: web.Request) -> web.Response:
        """
        Create a tool description.
        This is used by users to better understand what a tool does and how to use it.
        ---
        summary: Create a tool description.
        tags:
          - Tool
        requestBody:
          description: JSON document to describe tool.
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ToolDescription'

        responses:
          '200':
            description: Expected response to a valid request
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Response'
        """
        try:
            jsond_doc = await request.json()
            if 'tool_name' in jsond_doc and 'poc' in jsond_doc and 'usage' in jsond_doc:
                self.db.Createtool_description(
                    tool_name=jsond_doc['tool_name'],
                    poc=jsond_doc['poc'],
                    usage=jsond_doc['usage'],
                )
                return web.Response(text=self.json_success('Tool created'))
            else:
                return web.HTTPInternalServerError(text=self.json_error('Tool Description must have "tool_name", "poc", and "usage" keys.'))
        except Exception as e:
            return web.HTTPInternalServerError(text=self.json_error(str(e)))

    async def gettooldescription(self, request: web.Request) -> web.Response:
        """
        Get a list or single tool descriptions
        This is used by users to better understand what a tool does and how to use it.
        ---
        summary: Get a list or single tool descriptions
        tags:
          - Tool
        parameters:
          - in: query
            name: tool_names
            schema:
              type: array
              items:
                type: string
            required: true
            description: The name or list of names of the tool(s) to query.

        responses:
          '200':
            description: Expected response to a valid request
            content:
              application/json:
                schema:
                  type: array
                  items:
                    $ref: '#/components/schemas/ToolDescription'
        """
        try:
            res: List[dict]
            res = []
            if 'tool_names' in request.query.keys():
                tool_names = request.query.getall('tool_names')
                tools = self.db.Gettool_descriptions(tool_names)
                for tool in tools:
                    res.append(tool.toDict())
                return web.json_response(res)
            else:
                return web.HTTPInternalServerError(text=self.json_error('tool_names cannot be absent'))
        except Exception as e:
            return web.HTTPInternalServerError(text=self.json_error(str(e)))

    ## Callback ##
    async def callback(self, request: web.Request):
        """
          Callback for agents to hit identifying them as still active.
          ---
          summary: Callback for agents to hit identifying them as still active.
          tags:
            - Callback
          requestBody:
            description: JSON document to describe callback activity.
            required: true
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Callback'

          responses:
            '200':
              description: Expected response to a valid request
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/Response'
        """
        try:
            body = await request.text()
            jsond_doc = json.loads(body)
            if 'type' in jsond_doc and 'ip' in jsond_doc:
                self.db.RegisterCallback(
                    primary_ip=jsond_doc['ip'],
                    tool_name=jsond_doc['type']
                )
            else:
                return web.HTTPInternalServerError(text=self.json_error('Tool Description must have "toolname", "poc", and "usage" keys.'))
            return web.Response(text=self.json_success('Callback registered.'))
        except Exception as e:
            return web.HTTPInternalServerError(text=self.json_error(f'{e}'))

    def start(self):
        print(
            f"Docs availabel at: http://{self.bind_host}:{self.port}{self.docs_path}")
        web.run_app(self.app, port=self.port, host=self.bind_host)

    def json_error(self, err_msg: str) -> dict:
        res = {}
        res['status'] = 'ERROR'
        res['message'] = err_msg
        return json.dumps(res)

    def json_success(self, err_msg: str) -> dict:
        res = {}
        res['status'] = 'SUCCESS'
        res['message'] = err_msg
        return json.dumps(res)

    # redirect api hits to / to docs.
    async def givedocs(self, _: web.Request) -> web.Response:
        if self.debug:
            raise web.HTTPFound('/docs')
        else:
            raise web.HTTPFound(self.redirect_url)

    def init_app(self):
        db = MongoConnection()
        app = web.Application()
        if not self.debug:
            self.docs_path = f"/{uuid4()}/"
        swagger = SwaggerDocs(
            app,
            swagger_ui_settings=SwaggerUiSettings(path=self.docs_path),
            title="Swagger pwnbord",
            version="1.0.0",
            components="./docs/components.yaml"
        )
        swagger.add_routes([
            web.get("/", self.givedocs, allow_head=False),
            web.post("/setboard", self.setboard),
            web.get("/getboard", self.getboard, allow_head=False),
            web.get("/getboardrows", self.getboardrows, allow_head=False),
            web.get("/getteamnames", self.getteamnames, allow_head=False),
            web.get("/getservicegroups",
                    self.getservicegroups, allow_head=False),
            web.get("/gettoolnames", self.gettoolnames, allow_head=False),
            web.post("/settooldescription",
                     self.settooldescription),
            web.get("/gettooldescription",
                    self.gettooldescription, allow_head=False),
            web.post("/generic",
                     self.callback),
            web.get("/generic",
                    self.callback, allow_head=False),
        ])
        return db, app, swagger


if __name__ == '__main__':
    pwnboardAPI = API(debug=True)
    pwnboardAPI.start()
    pwnboardAPI.start()
    pwnboardAPI.start()
