import json

from aiohttp import web

from connection.connection import MongoConnection

routes = web.RouteTableDef()

db = MongoConnection()


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


@ routes.get('/filter')
async def filter(request):
    board = db.GetBoardDict()
    return web.Response(text=json.dumps(board))


if __name__ == '__main__':
    db = MongoConnection()
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, port=5000)
