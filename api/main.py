import json
from distutils.log import debug

from aiohttp import web

from connection.connection import MongoConnection

routes = web.RouteTableDef()

db = MongoConnection()


def json_error(err_msg: str) -> dict:
    res = {}
    res['error'] = err_msg
    return json.dumps(res)

## Board setup ###


@routes.post('/setboard')
async def setboard(request):
    """
    curl -X POST http://localhost:5000/setboard -H 'Content-Type: application/json' -d '[{"name": "Hulto - web-server", "primaryIP": "10.0.0.1", "os": "LINUX", "serviceGroup": "web-server", "teamName": "Hulto", "tags": ["Linux", "Web", "HTTP"]}, {"name": "Hulto  - mail-server", "primaryIP": "10.0.0.2", "os": "LINUX", "serviceGroup": "mail-server", "teamName": "Hulto", "tags": ["Linux", "mail"]}, {"name": "Hulto  - ssh-server", "primaryIP": "10.0.0.3", "os": "LINUX", "serviceGroup": "ssh-server", "teamName": "Hulto", "tags": ["Linux", "ssh"]}, {"name": "squidli  - web-server", "primaryIP": "10.0.1.1", "os": "LINUX", "serviceGroup": "web-server", "teamName": "squidli", "tags": ["Linux", "Web", "HTTP"]}, {"name": "squidli  - mail-server", "primaryIP": "10.0.1.2", "os": "LINUX", "serviceGroup": "mail-server", "teamName": "squidli", "tags": ["Linux", "mail"]}, {"name": "squidli  - ssh-server", "primaryIP": "10.0.1.3", "os": "LINUX", "serviceGroup": "ssh-server", "teamName": "squidli", "tags": ["Linux", "ssh"]}]'
    """
    body = await request.text()
    jsondDoc = json.loads(body)
    _ = db.BuildBoard(jsondDoc)
    board = db.GetBoardDict()
    return web.Response(text=json.dumps(board))


@ routes.get('/getboard')
async def getboard(request):
    """
    curl localhost:5000/getboard
    """
    board = db.GetBoardDict()
    return web.Response(text=json.dumps(board))

### Tool desription registration ###


@routes.post('/settooldesc')
async def setboard(request):
    """
    """
    body = await request.text()
    jsondDoc = json.loads(body)
    _ = db.BuildBoard(jsondDoc)
    board = db.GetBoardDict()
    return web.Response(text=json.dumps(board))


@ routes.get('/gettooldesc')
async def getboard(request):
    """
    curl localhost:5000/getboard
    """
    if 'toolnames' in request.rel_url.query.keys():
        toolnames = list(request.rel_url.query['toolnames'].split(","))
    return web.Response(text=json.dumps(board))


### Filtering ###

@ routes.get('/filter')
async def filter(request):
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
                return web.HTTPInternalServerError(text=json_error('Invalid filter. Timeout must be a nmuber.'))

    result = db.Filter(teams, service_groups, oses,
                       tool_names, tool_match, timeout)
    return web.Response(text=str(result))


if __name__ == '__main__':
    db = MongoConnection()
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, port=5000)
