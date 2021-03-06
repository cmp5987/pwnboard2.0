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

    def start(self):
        print(
            f"Docs availabel at: http://{self.bind_host}:{self.port}{self.docs_path}")
        web.run_app(self.app, port=self.port, host=self.bind_host)

    def json_error(self, err_msg: str) -> dict:
        res = {}
        res['error'] = err_msg
        return json.dumps(res)

    def json_sucess(self, err_msg: str) -> dict:
        res = {}
        res['sucess'] = err_msg
        return json.dumps(res)

    # redirect api hits to / to docs.

    async def givedocs(self, _: web.Request) -> web.Response:
        if self.debug:
            raise web.HTTPFound('/docs')
        else:
            raise web.HTTPFound(self.redirect_url)

    ## Board setup ###

    async def setboard(self, request: web.Request) -> web.Response:
        """
        Create board a for event.
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
            return web.Response(text=json.dumps(board))
        except Exception as e:
            return web.HTTPInternalServerError(text=self.json_error(str(e)))

    async def getboard(self, request: web.Request) -> web.Response:
        """
        Get current board a for event.
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
        board = self.db.GetBoardDict()
        return web.Response(text=json.dumps(board))

    async def getboardrows(self, request: web.Request) -> web.Response:
        """
        Get current board a for event in row format
        The board will represent all the hosts.
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
                  $ref: '#/components/schemas/BoardRows'
        """
        board = self.db.GetBoardDict()

        rows = {}
        for host in board:
            if host['service_group'] not in rows.keys():
                rows[host['service_group']] = {}
                rows[host['service_group']]['service_group'] = host['service_group']
                rows[host['service_group']]['teams'] = {}

            rows[host['service_group']]['teams'][host['team_name']] = host

        res = []
        for row_key in rows.keys():
            res.append(rows[row_key])

        return web.Response(text=json.dumps(res))

    async def getservicegroups(self, request: web.Request) -> web.Response:
        """
        Get a list of all service groups
        ---
        summary: Get a list of all service groups.
        tags:
          - Board

        responses:
          '200':
            description: Expected response to a valid request
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Response'
        """
        res: List[str]
        res = []
        try:
            service_groups = self.db.GetAllServiceGroups()
            return web.json_response({"res": service_groups})
        except Exception as e:
            return web.HTTPInternalServerError(text=self.json_error(str(e)))

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
                  $ref: '#/components/schemas/Response'
        """
        res: List[str]
        res = []
        try:
            team_names = self.db.GetAllTeamNames()
            return web.json_response({"res": team_names})
        except Exception as e:
            return web.HTTPInternalServerError(text=self.json_error(str(e)))

    async def gettoolnames(self, request: web.Request) -> web.Response:
        """
        Get a list of all tool names.
        ---
        summary: Get a list of all tool names.
        tags:
          - Board

        responses:
          '200':
            description: Expected response to a valid request
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Response'
        """
        res: List[str]
        res = []
        try:
            tool_names = self.db.GetAllToolNames()
            return web.json_response({"res": tool_names})
        except Exception as e:
            return web.HTTPInternalServerError(text=self.json_error(str(e)))

    ### Tool desription registration ###

    async def settooldescription(self, request: web.Request) -> web.Response:
        """
        Create a tool description.
        This is used by users to better understand what a tool does and how to use it.
        ---
        summary: Create a tool description.
        tags:
          - Tool_description
        requestBody:
          description: JSON document to describe tool.
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Tool_description'

        responses:
          '200':
            description: Expected response to a valid request
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Response'
        """
        body = await request.text()
        try:
            jsond_doc = json.loads(body)
        except Exception as e:
            return web.HTTPInternalServerError(text=self.json_error(f'{e}'))
        if 'toolname' in jsond_doc and 'poc' in jsond_doc and 'usage' in jsond_doc:
            self.db.Createtool_description(
                tool_name=jsond_doc['toolname'],
                poc=jsond_doc['poc'],
                usage=jsond_doc['usage'],
            )
        else:
            return web.HTTPInternalServerError(text=self.json_error('Tool Description must have "toolname", "poc", and "usage" keys.'))
        return web.Response(text=self.json_sucess('Tool created.'))

    async def gettooldescription(self, request: web.Request) -> web.Response:
        """
        Get a list or single tool descriptions
        This is used by users to better understand what a tool does and how to use it.
        ---
        summary: Get a list or single tool descriptions
        tags:
          - Tool_description
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
                  $ref: '#/components/schemas/Response'
        """
        res: List[dict]
        res = []
        if 'tool_names' in request.rel_url.query.keys():
            tool_names = list(request.rel_url.query['tool_names'].split(","))
            tools = self.db.Gettool_descriptions(tool_names)
            for tool in tools:
                res.append(tool.toDict())
        else:
            return web.HTTPInternalServerError(text=self.json_error('tool_names cannot be absent'))

        return web.Response(text=json.dumps(res))

    ### Callback ###

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
        body = await request.text()
        try:
            jsond_doc = json.loads(body)
        except Exception as e:
            return web.HTTPInternalServerError(text=self.json_error(f'{e}'))
        if 'type' in jsond_doc and 'ip' in jsond_doc:
            self.db.RegisterCallback(
                primary_ip=jsond_doc['ip'],
                tool_name=jsond_doc['type']
            )
        else:
            return web.HTTPInternalServerError(text=self.json_error('Tool Description must have "toolname", "poc", and "usage" keys.'))
        return web.Response(text=self.json_sucess('Callback registered.'))

    ### Filtering ###

    async def filter(self, request: web.Request) -> web.Response:
        """
        Filter for specific hosts based on a numebr of fields.
        ---
        summary: Filter for specific hosts based on a numebr of fields.
        tags:
          - Filter
        parameters:
          - in: query
            name: teams
            schema:
              type: array
              items:
                type: string
            required: false
            description: The name or list of names of the team(s) to query.
          - in: query
            name: service_groups
            schema:
              type: array
              items:
                type: string
            required: false
            description: The name or list of names of the service_group(s) to query.
          - in: query
            name: oses
            schema:
              type: array
              items:
                type: string
            required: false
            description: The name or list of names of the os(es) to query.
          - in: query
            name: tool_names
            schema:
              type: array
              items:
                type: string
            required: false
            description: The name or list of names of the tool_name(s) to query.
          - in: query
            name: toolname
            schema:
              type: string
            required: false
            description: The type of tool matching to do. (active, inactive, installed, never)
          - in: query
            name: timeout
            schema:
              type: integer
            required: false
            description: The number of seconds to consider a callback timedout.

        responses:
          '200':
            description: Expected response to a valid request
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Response'
        """

        teams = service_groups = oses = tool_names = []
        tool_match = "active"  # never, inactive
        timeout = 480
        if 'teams' in request.rel_url.query.keys():
            teams = list(request.rel_url.query['teams'].split(","))

        if 'service_groups' in request.rel_url.query.keys():
            service_groups = list(
                request.rel_url.query['service_groups'].split(","))

        if 'oses' in request.rel_url.query.keys():
            oses = list(request.rel_url.query['oses'].split(","))

        if 'tool_names' in request.rel_url.query.keys():
            tool_names = list(request.rel_url.query['tool_names'].split(","))

        if 'tool_match' in request.rel_url.query.keys():
            tool_match = str(request.rel_url.query['tool_names'])

        if 'timeout' in request.rel_url.query.keys():
            tmp = str(request.rel_url.query['timeout'])
            if len(tmp) > 0:
                if tmp.isnumeric():
                    timeout = int(request.rel_url.query['timeout'])
                else:
                    return web.HTTPInternalServerError(text=self.json_error('Invalid filter. Timeout must be a nmuber.'))

        result = self.db.Filter(teams, service_groups, oses,
                                tool_names, tool_match, timeout)
        return web.Response(text=str(result))

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
            web.get("/filter", filter, allow_head=False),
            web.post("/setboard", self.setboard),
            web.get("/getboard", self.getboard, allow_head=False),
            web.get("/getboardrows", self.getboardrows, allow_head=False),
            web.post("/settooldesc", self.settooldescription),
            web.get("/gettooldesc", self.gettooldescription, allow_head=False),
            web.post("/generic", self.callback),
            web.get("/getservicegroups",
                    self.getservicegroups, allow_head=False),
            web.get("/getteamnames",
                    self.getteamnames, allow_head=False),
            web.get("/gettoolnames",
                    self.gettoolnames, allow_head=False),

        ])
        return db, app, swagger


if __name__ == '__main__':
    pwnboardAPI = API(debug=True)
    pwnboardAPI.start()
