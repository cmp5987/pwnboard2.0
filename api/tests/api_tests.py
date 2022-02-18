import asyncio
import json

import aiohttp
import pytest
from aiohttp import ClientSession


async def main2():
    async with ClientSession('http://httpbin.org') as session:
        async with session.get('/') as resp:
            print(resp)
        async with session.get('/getboard') as resp:
            pass
        async with session.get('/gettooldesc') as resp:
            pass
        async with session.get('/filter') as resp:
            pass
        async with session.post('/setboard', data=b'data') as resp:
            pass
        async with session.post('/settooldesc', data=b'data') as resp:
            pass
        async with session.post('/generic', data=b'data') as resp:
            pass

API_URL = 'http://localhost:5000/'


async def test_settooldesc(session):
    TEST_TOOLDESC = {"toolname": "reptile",
                     "poc": "squidli", "usage": "/root/reptile_up"}
    SUCCESS_DICT = {"sucess": "Tool created."}
    async with session.post(API_URL + 'settooldesc', json=TEST_TOOLDESC) as resp:
        respText = await resp.text()
        print(respText)
        assert(SUCCESS_DICT == json.loads(respText))


async def test_gettooldesc(session):
    TEST_TOOLDESC = [{"tool_name": "reptile",
                      "poc": "squidli", "usage": "/root/reptile_up"}]
    async with session.get(API_URL+'gettooldesc?toolnames=reptile') as resp:
        respText = await resp.text()
        assert(TEST_TOOLDESC == json.loads(respText))


async def test_setboard(session):
    TEST_BOARD = [{"primary_ip": "10.0.0.1", "name": "Hulto - web-server", "fqdn": "notset", "os": "LINUX", "team_name": "Hulto", "service_group": "web-server", "tags": ["Linux", "Web", "HTTP"], "tools": []}, {"primary_ip": "10.0.0.2", "name": "Hulto  - mail-server", "fqdn": "notset", "os": "Windows", "team_name": "Hulto", "service_group": "mail-server", "tags": ["Windows", "mail"], "tools": []}, {"primary_ip": "10.0.0.3", "name": "Hulto  - ssh-server", "fqdn": "notset", "os": "LINUX", "team_name": "Hulto",
                                                                                                                                                                                                                                                                                                                                                                                                                 "service_group": "ssh-server", "tags": ["Linux", "ssh"], "tools": []}, {"primary_ip": "10.0.1.1", "name": "squidli  - web-server", "fqdn": "notset", "os": "LINUX", "team_name": "squidli", "service_group": "web-server", "tags": ["Linux", "Web", "HTTP"], "tools": []}, {"primary_ip": "10.0.1.2", "name": "squidli  - mail-server", "fqdn": "notset", "os": "Windows", "team_name": "squidli", "service_group": "mail-server", "tags": ["Windows", "mail"], "tools": []}, {"primary_ip": "10.0.1.3", "name": "squidli  - ssh-server", "fqdn": "notset", "os": "LINUX", "team_name": "squidli", "service_group": "ssh-server", "tags": ["Linux", "ssh"], "tools": []}]
    async with session.post(API_URL+'setboard', json=TEST_BOARD) as resp:
        respText = await resp.text()
        assert(TEST_BOARD == json.loads(respText))


async def test_getboard(session):
    TEST_BOARD = [{"primary_ip": "10.0.0.1", "name": "Hulto - web-server", "fqdn": "notset", "os": "LINUX", "team_name": "Hulto", "service_group": "web-server", "tags": ["Linux", "Web", "HTTP"], "tools": []}, {"primary_ip": "10.0.0.2", "name": "Hulto  - mail-server", "fqdn": "notset", "os": "Windows", "team_name": "Hulto", "service_group": "mail-server", "tags": ["Windows", "mail"], "tools": []}, {"primary_ip": "10.0.0.3", "name": "Hulto  - ssh-server", "fqdn": "notset", "os": "LINUX", "team_name": "Hulto",
                                                                                                                                                                                                                                                                                                                                                                                                                 "service_group": "ssh-server", "tags": ["Linux", "ssh"], "tools": []}, {"primary_ip": "10.0.1.1", "name": "squidli  - web-server", "fqdn": "notset", "os": "LINUX", "team_name": "squidli", "service_group": "web-server", "tags": ["Linux", "Web", "HTTP"], "tools": []}, {"primary_ip": "10.0.1.2", "name": "squidli  - mail-server", "fqdn": "notset", "os": "Windows", "team_name": "squidli", "service_group": "mail-server", "tags": ["Windows", "mail"], "tools": []}, {"primary_ip": "10.0.1.3", "name": "squidli  - ssh-server", "fqdn": "notset", "os": "LINUX", "team_name": "squidli", "service_group": "ssh-server", "tags": ["Linux", "ssh"], "tools": []}]
    async with session.get(API_URL+'getboard') as resp:
        respText = await resp.text()
        assert(TEST_BOARD == json.loads(respText))


async def test_callback(session):
    TEST_BOARD = [{"primary_ip": "10.0.0.1", "name": "Hulto - web-server", "fqdn": "notset", "os": "LINUX", "team_name": "Hulto", "service_group": "web-server", "tags": ["Linux", "Web", "HTTP"], "tools": [{"tool_name": "reptile", "lastseen": "TEST", "firstseen": "TEST", "totalbeacons": 0}]}, {"primary_ip": "10.0.0.2", "name": "Hulto  - mail-server", "fqdn": "notset", "os": "Windows", "team_name": "Hulto", "service_group": "mail-server", "tags": ["Windows", "mail"], "tools": []}, {"primary_ip": "10.0.0.3", "name": "Hulto  - ssh-server", "fqdn": "notset", "os": "LINUX", "team_name": "Hulto", "service_group": "ssh-server",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     "tags": ["Linux", "ssh"], "tools": []}, {"primary_ip": "10.0.1.1", "name": "squidli  - web-server", "fqdn": "notset", "os": "LINUX", "team_name": "squidli", "service_group": "web-server", "tags": ["Linux", "Web", "HTTP"], "tools": []}, {"primary_ip": "10.0.1.2", "name": "squidli  - mail-server", "fqdn": "notset", "os": "Windows", "team_name": "squidli", "service_group": "mail-server", "tags": ["Windows", "mail"], "tools": []}, {"primary_ip": "10.0.1.3", "name": "squidli  - ssh-server", "fqdn": "notset", "os": "LINUX", "team_name": "squidli", "service_group": "ssh-server", "tags": ["Linux", "ssh"], "tools": []}]

    CALLBACK = {'type': 'reptile', 'ip': '10.0.0.1'}
    CALLBACK_SUCCESS = {"sucess": "Callback registered."}
    async with session.post(API_URL+'generic', json=CALLBACK) as resp:
        respText = await resp.text()
        assert(CALLBACK_SUCCESS == json.loads(respText))
    async with session.get(API_URL+'getboard') as resp:
        respText = await resp.text()
        respDictList = json.loads(respText)
        assert(len(respDictList) == 6)
        for respDict in respDictList:
            for toolDict in respDict['tools']:
                toolDict['firstseen'] = 'TEST'
                toolDict['lastseen'] = 'TEST'

        assert(TEST_BOARD == respDictList)


@ pytest.fixture
async def session():
    return aiohttp.ClientSession()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_settooldesc(aiohttp.ClientSession()))
    loop.close()
