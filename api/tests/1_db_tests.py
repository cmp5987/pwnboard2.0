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
            "tags": ["Linux", "Web", "HTTP"],
            "tools": [{
                "tool_name": "reptile",
                "last_seen": 1645500015,
                "first_seen": 1645500015,
                "total_beacons": 1
            }]
        },
        {
            "name": "Hulto  - mail-server",
            "primary_ip": "10.0.0.2",
            "os": "Windows",
            "service_group": "mail-server",
            "team_name": "Hulto",
            "tags": ["Windows", "mail"],
        },
        {
            "name": "Hulto  - ssh-server",
            "primary_ip": "10.0.0.3",
            "os": "LINUX",
            "service_group": "ssh-server",
            "team_name": "Hulto",
            "tags": ["Linux", "ssh"],
        },
        {
            "name": "squidli  - web-server",
            "primary_ip": "10.0.1.1",
            "os": "LINUX",
            "service_group": "web-server",
            "team_name": "squidli",
            "tags": ["Linux", "Web", "HTTP"],
        },
        {
            "name": "squidli  - mail-server",
            "primary_ip": "10.0.1.2",
            "os": "Windows",
            "service_group": "mail-server",
            "team_name": "squidli",
            "tags": ["Windows", "mail"],
        },
        {
            "name": "squidli  - ssh-server",
            "primary_ip": "10.0.1.3",
            "os": "LINUX",
            "service_group": "ssh-server",
            "team_name": "squidli",
            "tags": ["Linux", "ssh"],
        }
    ]
    _ = myconn.BuildBoardFromDictList(board)
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
    assert(two-one == 1)
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
    sleep(3)
    hosts = myconn.GetTimedOutToolHosts(["reptile", "goofkit"], 2)
    assert(len(set(hosts)) == 1)
    for host in hosts:
        assert(host.primary_ip == "10.0.0.1")


def test_query_installed_tool():
    myconn = MongoConnection()
    hosts = myconn.GetInstalledToolHosts(["reptile"])
    assert(len(set(hosts)) == 1)
    for host in hosts:
        assert(host.primary_ip == "10.0.0.1")


def test_create_tool_desc():
    myconn = MongoConnection()
    _ = myconn.Createtool_description(
        tool_name="goofkit", poc="Hulto", usage="kill -36 1")
    _ = myconn.Createtool_description(
        tool_name="reptile", poc="Hulto", usage="/root/reptile_up")

    tool_descs = myconn.Gettool_descriptions(["reptile", "goofkit"])
    assert(len(set(tool_descs)) == 2)
    for tool_desc in tool_descs:
        assert(tool_desc.tool_name in ["reptile", "goofkit"])


def test_update_tool_desc():
    myconn = MongoConnection()
    _ = myconn.Createtool_description(
        tool_name="reptile", poc="squidli", usage="/root/reptile_up")

    tool_descs = myconn.Gettool_descriptions(["reptile", "goofkit"])
    assert(len(set(tool_descs)) == 2)
    for tool_desc in tool_descs:
        assert(tool_desc.tool_name in ["reptile", "goofkit"])
        if tool_desc.tool_name == "reptile":
            assert(tool_desc.poc == "squidli")


def test_filter():
    myconn = MongoConnection()
    results = myconn.Filter(
        teams=["Hulto"], service_groups=["web-server"],
        oses=[], tool_names=[])
    assert(len(results) == 1)
    assert('primary_ip' in results[0])
    assert(results[0]['primary_ip'] == "10.0.0.1")


def test_filter_active():
    myconn = MongoConnection()
    results = myconn.Filter(
        teams=[], service_groups=[],
        oses=["LINUX"], tool_names=["reptile"], tool_match="active")
    assert(len(results) == 1)


def test_filter_inactive():
    myconn = MongoConnection()
    results = myconn.Filter(
        teams=[], service_groups=[],
        oses=["LINUX"], tool_names=["reptile"], tool_match="inactive")
    assert(len(results) == 4)


def test_filter_installed():
    myconn = MongoConnection()
    results = myconn.Filter(
        teams=[], service_groups=[],
        oses=["LINUX"], tool_names=["reptile"], tool_match="installed")
    assert(len(results) == 1)


def test_filter_never():
    myconn = MongoConnection()
    results = myconn.Filter(
        teams=[], service_groups=[],
        oses=["LINUX"], tool_names=["reptile"], tool_match="never")
    assert(len(results) == 3)


def test_callback_new_tool():
    myconn = MongoConnection()
    one = myconn.RegisterCallback("10.0.0.1", "newtool")
    assert(one == 0)


def test_get_hosts_by_os():
    myconn = MongoConnection()
    hosts = myconn.GetOsHosts(["LINUX"])
    assert(len(set(hosts)) == 4)
    for host in hosts:
        assert("10.0." in host.primary_ip)


def test_restore_board():
    myconn = MongoConnection()
    # Induce an error
    board = [
        {}
    ]
    # Make sure error is handled
    try:
        _ = myconn.BuildBoardFromDictList(board)
    except Exception as e:
        assert("Required fields not provided:" in str(e))
    # Make sure board is reset.
    board = myconn.GetBoard()
    assert(len(set(board)) == 6)
    for host in board:
        assert('10.0.' in host.primary_ip)


def test_get_host():
    myconn = MongoConnection()
    host = myconn.GetHost("10.0.0.1")
    assert(host.primary_ip == "10.0.0.1")


def test_get_host_errors():
    myconn = MongoConnection()
    with pytest.raises(Exception, match=r".*Expected type string for variable primary_ip.*") as exception:
        _ = myconn.GetHost(1)


def test_create_host_dict_errors_type():
    myconn = MongoConnection()
    with pytest.raises(Exception, match=r".*Expected dictionary recived.*") as exception:
        _ = myconn.createHostDict('not a dictionary')


def test_create_host_dict_errors_field():
    myconn = MongoConnection()
    with pytest.raises(Exception, match=r".*Required fields not provided.*") as exception:
        _ = myconn.createHostDict({"service_group": "test"})


def test_create_host_dict_errors_field():
    myconn = MongoConnection()
    with pytest.raises(Exception, match=r".*Missing required property tool_name.*") as exception:
        _ = myconn.createHost(primary_ip="1.2.3.4", name="test1",
                              team_name="teamtest", service_group="testgroup",
                              tools=[
                                  {"last_seen": 0, "first_seen": 0, "total_beacons": 0}],
                              fqdn='notset', os='notset', tags=[])


def test_get_all_service_groups():
    myconn = MongoConnection()
    expected_set_of_service_groups = [
        "mail-server", "web-server", "ssh-server"]
    expected_set_of_service_groups.sort()
    service_groups = myconn.GetAllServiceGroups()
    assert(service_groups == expected_set_of_service_groups)


def test_get_all_team_names():
    myconn = MongoConnection()
    expected_set_of_team_names = ['Hulto', 'squidli']
    expected_set_of_team_names.sort()
    team_names = myconn.GetAllTeamNames()
    assert(team_names == expected_set_of_team_names)


def test_get_all_tool_names():
    myconn = MongoConnection()
    expected_set_of_tool_names = ['newtool', 'reptile']
    expected_set_of_tool_names.sort()
    tool_names = myconn.GetAllToolNames()
    assert(tool_names == expected_set_of_tool_names)


@ pytest.fixture(scope="session", autouse=True)
def execute_before_any_test():
    test_wipe_db()


# if __name__ == '__main__':
#     test_wipe_db()
#     test_build_board()
#     test_get_all_service_groups()
    # print(f"TEST test_build_board():              {test_build_board()}")
    # print(f"TEST test_query_team():               {test_query_team()}")
    # print(
    #     f"TEST test_query_multiple_team():      {test_query_multiple_team()}")
    # print(
    #     f"TEST test_query_service_group():       {test_query_service_group()}")
    # print(
    #     f"TEST test_query_multi_service_group(): {test_query_multiple_service_group()}")

    # print(
    #     f"TEST test_callback():                 {test_callback()}")
    # print(
    #     f"TEST test_callback_update_poc():      {test_callback_update_poc()}")
    # print(
    #     f"TEST test_query_active_tool():        {test_query_active_tool()}")

    # print(
    #     f"TEST test_query_never_active_tool():  {test_query_never_active_tool()}")
    # sleep(2)
    # print(
    #     f"TEST test_query_timedout_tool():      {test_query_timedout_tool()}")
    # test_callback()
    # print(
    #     f"TEST test_query_active_tool():        {test_query_active_tool()}")
    # print(
    #     f"TEST test_create_tool_desc():         {test_create_tool_desc()}")
    # print(
    #     f"TEST test_update_tool_desc():         {test_update_tool_desc()}")
    # print(f"TEST test_filter():                   {test_filter()}")
