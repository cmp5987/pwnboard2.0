import sys
from time import sleep

import pytest

sys.path.append('./')  # noqa
from connection.connection import MongoConnection  # noqa


def test_wipe_db():
    myconn = MongoConnection()
    myconn.WipeCollection()


def test_build_board():
    myconn = MongoConnection()

    board = [
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
            "os": "Windows",
            "service_group": "mail-server",
            "team_name": "Hulto",
            "tags": ["Windows", "mail"]
        },
        {
            "name": "Hulto  - ssh-server",
            "primary_ip": "10.0.0.3",
            "os": "LINUX",
            "service_group": "ssh-server",
            "team_name": "Hulto",
            "tags": ["Linux", "ssh"]
        },
        {
            "name": "squidli  - web-server",
            "primary_ip": "10.0.1.1",
            "os": "LINUX",
            "service_group": "web-server",
            "team_name": "squidli",
            "tags": ["Linux", "Web", "HTTP"]
        },
        {
            "name": "squidli  - mail-server",
            "primary_ip": "10.0.1.2",
            "os": "Windows",
            "service_group": "mail-server",
            "team_name": "squidli",
            "tags": ["Windows", "mail"]
        },
        {
            "name": "squidli  - ssh-server",
            "primary_ip": "10.0.1.3",
            "os": "LINUX",
            "service_group": "ssh-server",
            "team_name": "squidli",
            "tags": ["Linux", "ssh"]
        }
    ]
    _ = myconn.BuildBoard(board)
    board = myconn.GetBoard()
    assert(len(set(board)) == 6)
    for host in board:
        assert('10.0.' in host.primary_ip)


def test_query_team():
    myconn = MongoConnection()
    hosts = myconn.GetTeamHosts(["Hulto"])
    assert(len(set(hosts)) == 3)
    for host in hosts:
        assert("10.0.0." in host.primary_ip)


def test_query_multiple_team():
    myconn = MongoConnection()
    hosts = myconn.GetTeamHosts(["Hulto", "squidli"])
    assert(len(set(hosts)) == 6)
    for host in hosts:
        assert('10.0.' in host.primary_ip)


def test_query_service_group():
    myconn = MongoConnection()
    hosts = myconn.GetServiceHosts(["web-server"])
    assert(len(set(hosts)) == 2)
    for host in hosts:
        assert(".1" in host.primary_ip[-2:])


def test_query_multiple_service_group():
    myconn = MongoConnection()
    hosts = myconn.GetServiceHosts(["web-server", "mail-server"])
    assert(len(set(hosts)) == 4)
    for host in hosts:
        assert('10.0.' in host.primary_ip)


def test_callback():
    myconn = MongoConnection()
    one = myconn.RegisterCallback("10.0.0.1", "reptile")
    two = myconn.RegisterCallback("10.0.0.1", "reptile")
    assert(two-one == 1)


def test_callback_update_poc():
    myconn = MongoConnection()
    one = myconn.RegisterCallback("10.0.0.1", "reptile")
    two = myconn.RegisterCallback("10.0.0.1", "reptile")
    assert(two-one == 1)


def test_query_active_tool():
    myconn = MongoConnection()
    one = myconn.RegisterCallback("10.0.0.1", "reptile")
    two = myconn.RegisterCallback("10.0.0.1", "reptile")
    hosts = myconn.GetActiveToolHosts(["reptile", "goofkit"], 2)
    assert(len(set(hosts)) == 1)
    for host in hosts:
        assert(host.primary_ip == "10.0.0.1")
    return True


def test_query_never_active_tool():
    myconn = MongoConnection()
    hosts = myconn.GetNeverActiveToolHosts(["reptile", ])
    assert(len(set(hosts)) == 5)
    for host in hosts:
        assert(host.primary_ip != "10.0.0.1")

    hosts = myconn.GetNeverActiveToolHosts(["goofkit"])
    assert(len(set(hosts)) == 6)
    for host in hosts:
        assert('10.0.' in host.primary_ip)


def test_query_timedout_tool():
    myconn = MongoConnection()
    sleep(2)
    hosts = myconn.GetTimedOutToolHosts(["reptile", "goofkit"], 2)
    assert(len(set(hosts)) == 1)
    for host in hosts:
        assert(host.primary_ip == "10.0.0.1")


def test_query_active_tool():
    myconn = MongoConnection()
    hosts = myconn.GetActiveToolHosts(["reptile"], 5)
    assert(len(set(hosts)) == 1)
    for host in hosts:
        assert(host.primary_ip == "10.0.0.1")


def test_create_tool_desc():
    myconn = MongoConnection()
    _ = myconn.CreateToolDescription(
        tool_name="goofkit", poc="Hulto", usage="kill -36 1")
    _ = myconn.CreateToolDescription(
        tool_name="reptile", poc="Hulto", usage="/root/reptile_up")

    toolDescs = myconn.GetToolDescriptions(["reptile", "goofkit"])
    assert(len(set(toolDescs)) == 2)
    for toolDesc in toolDescs:
        assert(toolDesc.tool_name in ["reptile", "goofkit"])


def test_update_tool_desc():
    myconn = MongoConnection()
    _ = myconn.CreateToolDescription(
        tool_name="reptile", poc="squidli", usage="/root/reptile_up")

    toolDescs = myconn.GetToolDescriptions(["reptile", "goofkit"])
    assert(len(set(toolDescs)) == 2)
    for toolDesc in toolDescs:
        assert(toolDesc.tool_name in ["reptile", "goofkit"])
        if toolDesc.tool_name == "reptile":
            assert(toolDesc.poc == "squidli")


def test_filter():
    myconn = MongoConnection()
    results = myconn.Filter(
        teams=["Hulto"], service_groups=["web-server"],
        oses=[], tool_names=[])
    assert(len(results) == 1)
    assert('primary_ip' in results[0])
    assert(results[0]['primary_ip'] == "10.0.0.1")


@pytest.fixture(scope="session", autouse=True)
def execute_before_any_test():
    test_wipe_db()


if __name__ == '__main__':
    test_wipe_db()
    print(f"TEST test_build_board():              {test_build_board()}")
    print(f"TEST test_query_team():               {test_query_team()}")
    print(
        f"TEST test_query_multiple_team():      {test_query_multiple_team()}")
    print(
        f"TEST test_query_service_group():       {test_query_service_group()}")
    print(
        f"TEST test_query_multi_service_group(): {test_query_multiple_service_group()}")

    print(
        f"TEST test_callback():                 {test_callback()}")
    print(
        f"TEST test_callback_update_poc():      {test_callback_update_poc()}")
    print(
        f"TEST test_query_active_tool():        {test_query_active_tool()}")

    print(
        f"TEST test_query_never_active_tool():  {test_query_never_active_tool()}")
    sleep(2)
    print(
        f"TEST test_query_timedout_tool():      {test_query_timedout_tool()}")
    test_callback()
    print(
        f"TEST test_query_active_tool():        {test_query_active_tool()}")
    print(
        f"TEST test_create_tool_desc():         {test_create_tool_desc()}")
    print(
        f"TEST test_update_tool_desc():         {test_update_tool_desc()}")
    print(f"TEST test_filter():                   {test_filter()}")
