from aiohttp import request
from aiohttp.test_utils import TestClient, TestServer, loop_context

import main

db = None
app = None
swagger = None
# async def hello(request):
#     return web.Response(text='Hello, world')


async def test_get_board(aiohttp_client):
    client = await aiohttp_client(app)
    resp = await client.get('/getboard')
    assert resp.status == 200
    print(resp)


# def test_set_board(request):
#     print(request.text())


if __name__ == '__main__':
    testClient = TestClient(app)
    print(test_get_board(testClient))
