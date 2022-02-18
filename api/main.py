import json
import re
from distutils.log import debug
from typing import List
from urllib.request import Request
from uuid import uuid4

from aiohttp import request, web
from aiohttp_swagger3 import SwaggerDocs, SwaggerUiSettings

from connection.connection import MongoConnection


class API():
    db = MongoConnection()
    app = None
    swagger = None
    routes = web.RouteTableDef()
    redirect_url = "https://cdn.akamai.steamstatic.com"
    port = 5000
    debug = False
    bind_host = "0.0.0.0"

    def __init__(self, port: int = 5000, bind_host: str = "0.0.0.0",
                 debug: bool = False, redirect_url: str = "https://cdn.akamai.steamstatic.com"):
        self.port = port
        self.debug = debug
        self.bind_host = bind_host
        self.redirect_url = redirect_url
        self.db, self.app, self.swagger = self.init_app()

    def start(self):
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

    async def givedocs(self, request):
        if self.debug:
            raise web.HTTPFound('/docs')
        else:
            raise web.HTTPFound(self.redirect_url)

    ## Board setup ###

    async def setboard(self, request):
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
                $ref: '#/components/schemas/BoardInit'

        responses:
          '200':
            description: Expected response to a valid request
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Board'
        """
        body = await request.text()
        jsondDoc = json.loads(body)
        _ = self.db.BuildBoard(jsondDoc)
        board = self.db.GetBoardDict()
        return web.Response(text=json.dumps(board))

    async def getboard(self, request):
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

    ### Tool desription registration ###

    async def settooldescription(self, request):
        """
        Create a tool description.
        This is used by users to better understand what a tool does and how to use it.
        ---
        summary: Create a tool description.
        tags:
          - ToolDescription
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
        body = await request.text()
        try:
            jsondDoc = json.loads(body)
        except Exception as e:
            return web.HTTPInternalServerError(text=self.json_error(f'{e}'))
        if 'toolname' in jsondDoc and 'poc' in jsondDoc and 'usage' in jsondDoc:
            self.db.CreateToolDescription(
                tool_name=jsondDoc['toolname'],
                poc=jsondDoc['poc'],
                usage=jsondDoc['usage'],
            )
        else:
            return web.HTTPInternalServerError(text=self.json_error('Tool Description must have "toolname", "poc", and "usage" keys.'))
        return web.Response(text=self.json_sucess('Tool created.'))

    async def gettooldescription(self, request):
        """
        Get a list or single tool descriptions
        This is used by users to better understand what a tool does and how to use it.
        ---
        summary: Get a list or single tool descriptions
        tags:
          - ToolDescription
        parameters:
          - in: query
            name: toolnames
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
        if 'toolnames' in request.rel_url.query.keys():
            toolnames = list(request.rel_url.query['toolnames'].split(","))
            tools = self.db.GetToolDescriptions(toolnames)
            for tool in tools:
                res.append(tool.toDict())
        else:
            return web.HTTPInternalServerError(text=self.json_error('toolnames cannot be absent'))

        return web.Response(text=json.dumps(res))

    ### Callback ###

    async def callback(self, request):
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
            jsondDoc = json.loads(body)
        except Exception as e:
            return web.HTTPInternalServerError(text=self.json_error(f'{e}'))
        if 'toolname' in jsondDoc and 'poc' in jsondDoc and 'usage' in jsondDoc:
            self.db.CreateToolDescription(
                tool_name=jsondDoc['toolname'],
                poc=jsondDoc['poc'],
                usage=jsondDoc['usage'],
            )
        else:
            return web.HTTPInternalServerError(text=self.json_error('Tool Description must have "toolname", "poc", and "usage" keys.'))
        return web.Response(text=self.json_sucess('Tool created.'))

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
        docs_path = "/docs/"
        if not self.debug:
            docs_path = f"/{uuid4()}/"
        swagger = SwaggerDocs(
            app,
            swagger_ui_settings=SwaggerUiSettings(path=docs_path),
            title="Swagger pwnbord",
            version="1.0.0",
            components="./docs/components.yaml"
        )
        swagger.add_routes([
            web.get("/", self.givedocs, allow_head=False),
            web.get("/filter", filter, allow_head=False),
            web.post("/setboard", self.setboard),
            web.get("/getboard", self.getboard, allow_head=False),
            web.post("/settooldesc", self.settooldescription),
            web.get("/gettooldesc", self.gettooldescription, allow_head=False),
            web.post("/generic", self.callback),
        ])
        return db, app, swagger


if __name__ == '__main__':
    pwnboardAPI = API(debug=True)
    pwnboardAPI.start()
