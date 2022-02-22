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
        async with session.get('/gettool_desc') as resp:
            pass
        async with session.get('/filter') as resp:
            pass
        async with session.post('/setboard', data=b'data') as resp:
            pass
        async with session.post('/settool_desc', data=b'data') as resp:
            pass
        async with session.post('/generic', data=b'data') as resp:
            pass

API_URL = 'http://localhost:5000/'


async def test_settool_desc(session):
    TEST_tool_desc = {"toolname": "reptile",
                      "poc": "squidli", "usage": "/root/reptile_up"}
    SUCCESS_DICT = {"sucess": "Tool created."}
    async with session.post(API_URL + 'settooldesc', json=TEST_tool_desc) as resp:
        resp_text = await resp.text()
        print(resp_text)
        assert(SUCCESS_DICT == json.loads(resp_text))


async def test_gettool_desc(session):
    TEST_tool_desc = [{"tool_name": "reptile",
                      "poc": "squidli", "usage": "/root/reptile_up"}]
    async with session.get(API_URL+'gettooldesc?tool_names=reptile') as resp:
        resp_text = await resp.text()
        assert(TEST_tool_desc == json.loads(resp_text))


async def test_setboard(session):
    TEST_BOARD = [{"primary_ip": "10.0.0.1", "name": "Hulto - web-server", "fqdn": "notset", "os": "LINUX", "team_name": "Hulto", "service_group": "web-server", "tags": ["Linux", "Web", "HTTP"], "tools": [{"tool_name": "reptile", "last_seen": "1645500015", "first_seen": "1645500015", "total_beacons": "1"}]}, {"primary_ip": "10.0.0.2", "name": "Hulto  - mail-server", "fqdn": "notset", "os": "Windows", "team_name": "Hulto", "service_group": "mail-server", "tags": ["Windows", "mail"], "tools": []}, {"primary_ip": "10.0.0.3", "name": "Hulto  - ssh-server", "fqdn": "notset", "os": "LINUX", "team_name": "Hulto",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      "service_group": "ssh-server", "tags": ["Linux", "ssh"], "tools": []}, {"primary_ip": "10.0.1.1", "name": "squidli  - web-server", "fqdn": "notset", "os": "LINUX", "team_name": "squidli", "service_group": "web-server", "tags": ["Linux", "Web", "HTTP"], "tools": []}, {"primary_ip": "10.0.1.2", "name": "squidli  - mail-server", "fqdn": "notset", "os": "Windows", "team_name": "squidli", "service_group": "mail-server", "tags": ["Windows", "mail"], "tools": []}, {"primary_ip": "10.0.1.3", "name": "squidli  - ssh-server", "fqdn": "notset", "os": "LINUX", "team_name": "squidli", "service_group": "ssh-server", "tags": ["Linux", "ssh"], "tools": []}]
    async with session.post(API_URL+'setboard', json=TEST_BOARD) as resp:
        resp_text = await resp.text()
        for host_dict in TEST_BOARD:
            for tool_dict in host_dict['tools']:
                tool_dict['last_seen'] = int(tool_dict['last_seen'])
                tool_dict['first_seen'] = int(tool_dict['first_seen'])
                tool_dict['total_beacons'] = int(tool_dict['total_beacons'])
        assert(TEST_BOARD == json.loads(resp_text))


async def test_getboard(session):
    TEST_BOARD = [{"primary_ip": "10.0.0.1", "name": "Hulto - web-server", "fqdn": "notset", "os": "LINUX", "team_name": "Hulto", "service_group": "web-server", "tags": ["Linux", "Web", "HTTP"], "tools": [{"tool_name": "reptile", "last_seen": 1645500015, "first_seen": 1645500015, "total_beacons": 1}]}, {"primary_ip": "10.0.0.2", "name": "Hulto  - mail-server", "fqdn": "notset", "os": "Windows", "team_name": "Hulto", "service_group": "mail-server", "tags": ["Windows", "mail"], "tools": []}, {"primary_ip": "10.0.0.3", "name": "Hulto  - ssh-server", "fqdn": "notset", "os": "LINUX", "team_name": "Hulto",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                "service_group": "ssh-server", "tags": ["Linux", "ssh"], "tools": []}, {"primary_ip": "10.0.1.1", "name": "squidli  - web-server", "fqdn": "notset", "os": "LINUX", "team_name": "squidli", "service_group": "web-server", "tags": ["Linux", "Web", "HTTP"], "tools": []}, {"primary_ip": "10.0.1.2", "name": "squidli  - mail-server", "fqdn": "notset", "os": "Windows", "team_name": "squidli", "service_group": "mail-server", "tags": ["Windows", "mail"], "tools": []}, {"primary_ip": "10.0.1.3", "name": "squidli  - ssh-server", "fqdn": "notset", "os": "LINUX", "team_name": "squidli", "service_group": "ssh-server", "tags": ["Linux", "ssh"], "tools": []}]
    async with session.get(API_URL+'getboard') as resp:
        resp_text = await resp.text()
        resp_dict = json.loads(resp_text)
        for host_dict in resp_dict:
            for tool_dict in host_dict['tools']:
                tool_dict['last_seen'] = 1645500015
        assert(TEST_BOARD == resp_dict)


async def test_callback(session):
    TEST_BOARD = [{"primary_ip": "10.0.0.1", "name": "Hulto - web-server", "fqdn": "notset", "os": "LINUX", "team_name": "Hulto", "service_group": "web-server", "tags": ["Linux", "Web", "HTTP"], "tools": [{"tool_name": "reptile", "last_seen": "TEST", "first_seen": "TEST", "total_beacons": 2}]}, {"primary_ip": "10.0.0.2", "name": "Hulto  - mail-server", "fqdn": "notset", "os": "Windows", "team_name": "Hulto", "service_group": "mail-server", "tags": ["Windows", "mail"], "tools": []}, {"primary_ip": "10.0.0.3", "name": "Hulto  - ssh-server", "fqdn": "notset", "os": "LINUX", "team_name": "Hulto", "service_group": "ssh-server",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        "tags": ["Linux", "ssh"], "tools": []}, {"primary_ip": "10.0.1.1", "name": "squidli  - web-server", "fqdn": "notset", "os": "LINUX", "team_name": "squidli", "service_group": "web-server", "tags": ["Linux", "Web", "HTTP"], "tools": []}, {"primary_ip": "10.0.1.2", "name": "squidli  - mail-server", "fqdn": "notset", "os": "Windows", "team_name": "squidli", "service_group": "mail-server", "tags": ["Windows", "mail"], "tools": []}, {"primary_ip": "10.0.1.3", "name": "squidli  - ssh-server", "fqdn": "notset", "os": "LINUX", "team_name": "squidli", "service_group": "ssh-server", "tags": ["Linux", "ssh"], "tools": []}]

    CALLBACK = {'type': 'reptile', 'ip': '10.0.0.1'}
    CALLBACK_SUCCESS = {"sucess": "Callback registered."}
    async with session.post(API_URL+'generic', json=CALLBACK) as resp:
        resp_text = await resp.text()
        assert(CALLBACK_SUCCESS == json.loads(resp_text))
    async with session.get(API_URL+'getboard') as resp:
        resp_text = await resp.text()
        resp_dict_list = json.loads(resp_text)
        assert(len(resp_dict_list) == 6)
        for resp_dict in resp_dict_list:
            for tool_dict in resp_dict['tools']:
                tool_dict['first_seen'] = 'TEST'
                tool_dict['last_seen'] = 'TEST'

        assert(TEST_BOARD == resp_dict_list)


@ pytest.fixture
async def session():
    return aiohttp.ClientSession()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_settool_desc(aiohttp.ClientSession()))
    loop.close()
