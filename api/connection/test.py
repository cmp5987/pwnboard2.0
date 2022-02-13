from time import sleep

if __package__ is None or __package__ == '':
    from connection import MongoConnection
else:
    from connection.connection import MongoConnection


def test_wipe_db():
    myconn = MongoConnection()
    myconn.WipeCollection()


def test_build_board():
    myconn = MongoConnection()

    board = [
        {
            "name": "Hulto - web-server",
            "primaryIP": "10.0.0.1",
            "os": "LINUX",
            "serviceGroup": "web-server",
            "teamName": "Hulto",
            "tags": ["Linux", "Web", "HTTP"]
        },
        {
            "name": "Hulto  - mail-server",
            "primaryIP": "10.0.0.2",
            "os": "LINUX",
            "serviceGroup": "mail-server",
            "teamName": "Hulto",
            "tags": ["Linux", "mail"]
        },
        {
            "name": "Hulto  - ssh-server",
            "primaryIP": "10.0.0.3",
            "os": "LINUX",
            "serviceGroup": "ssh-server",
            "teamName": "Hulto",
            "tags": ["Linux", "ssh"]
        },
        {
            "name": "squidli  - web-server",
            "primaryIP": "10.0.1.1",
            "os": "LINUX",
            "serviceGroup": "web-server",
            "teamName": "squidli",
            "tags": ["Linux", "Web", "HTTP"]
        },
        {
            "name": "squidli  - mail-server",
            "primaryIP": "10.0.1.2",
            "os": "LINUX",
            "serviceGroup": "mail-server",
            "teamName": "squidli",
            "tags": ["Linux", "mail"]
        },
        {
            "name": "squidli  - ssh-server",
            "primaryIP": "10.0.1.3",
            "os": "LINUX",
            "serviceGroup": "ssh-server",
            "teamName": "squidli",
            "tags": ["Linux", "ssh"]
        }
    ]
    _ = myconn.BuildBoard(board)
    board = myconn.GetBoard()
    for host in board:
        if host.os != "LINUX":
            return False
    return True


def test_query_team():
    myconn = MongoConnection()
    hosts = myconn.GetTeamHosts(["Hulto"])
    if len(set(hosts)) != 3:
        # raise Exception(f"Incorrect number of hosts:\n{len(set(hosts))}/3")
        return False
    for host in hosts:
        if "10.0.0." not in host.primary_ip:
            # raise Exception(
            #     f"Incorrect primary_ip {host.primary_ip}\nExpected 10.0.0.X")
            return False
    return True


def test_query_multiple_team():
    myconn = MongoConnection()
    hosts = myconn.GetTeamHosts(["Hulto", "squidli"])
    if len(set(hosts)) != 6:
        return False
        # raise Exception(f"Incorrect number of hosts:\n{len(set(hosts))}/6")
    for host in hosts:
        if host.os != "LINUX":
            return False
            # raise Exception(
            #     f"Incorrect primary_ip {host.primary_ip}\nExpected 10.0.0.X")

    return True


def test_query_servicegroup():
    myconn = MongoConnection()
    hosts = myconn.GetServiceHosts(["web-server"])
    if len(set(hosts)) != 2:
        return False
    for host in hosts:
        if ".1" not in host.primary_ip[-2:]:
            return False
    return True


def test_query_multiple_servicegroup():
    myconn = MongoConnection()
    hosts = myconn.GetServiceHosts(["web-server", "mail-server"])
    if len(set(hosts)) != 4:
        return False
    for host in hosts:
        if host.os != "LINUX":
            return False
    return True


def test_callback():
    myconn = MongoConnection()
    one = myconn.RegisterCallback("10.0.0.1", "reptile")
    two = myconn.RegisterCallback("10.0.0.1", "reptile")
    return (two-one == 1)


def test_callback_update_poc():
    myconn = MongoConnection()
    one = myconn.RegisterCallback("10.0.0.1", "reptile")
    two = myconn.RegisterCallback("10.0.0.1", "reptile")
    return (two-one == 1)


def test_query_active_tool():
    myconn = MongoConnection()
    hosts = myconn.GetInstalledToolHosts(["reptile", "goofkit"])
    if len(set(hosts)) != 1:
        return False
    for host in hosts:
        if host.primary_ip != "10.0.0.1":
            return False
    return True


def test_query_never_active_tool():
    myconn = MongoConnection()
    hosts = myconn.GetNeverActiveToolHosts(["reptile", ])
    if len(set(hosts)) != 5:
        # return False
        raise Exception(f"Expected 5 host got {len(set(hosts))}")
    for host in hosts:
        if host.primary_ip == "10.0.0.1":
            # return False
            raise Exception(f"Expected not 10.0.0.1 got {host.primary_ip}")

    hosts = myconn.GetNeverActiveToolHosts(["goofkit"])
    if len(set(hosts)) != 6:
        return False
    for host in hosts:
        if host.os != "LINUX":
            return False
    return True


def test_query_timedout_tool():
    myconn = MongoConnection()
    hosts = myconn.GetTimedOutToolHosts(["reptile", "goofkit"], 2)
    if len(set(hosts)) != 1:
        return False
    for host in hosts:
        if host.primary_ip != "10.0.0.1":
            return False
    return True


def test_query_active_tool():
    myconn = MongoConnection()
    hosts = myconn.GetActiveToolHosts(["reptile"], 5)
    if len(set(hosts)) != 1:
        return False
    for host in hosts:
        if host.primary_ip != "10.0.0.1":
            return False
    return True


def test_create_tool_desc():
    myconn = MongoConnection()
    _ = myconn.CreateToolDescription(
        tool_name="goofkit", poc="Hulto", usage="kill -36 1")
    _ = myconn.CreateToolDescription(
        tool_name="reptile", poc="Hulto", usage="/root/reptile_up")

    toolDescs = myconn.GetToolDescription(["reptile", "goofkit"])
    if len(set(toolDescs)) != 2:
        return False
    for toolDesc in toolDescs:
        if toolDesc.tool_name not in ["reptile", "goofkit"]:
            return False
    return True


def test_update_tool_desc():
    myconn = MongoConnection()
    _ = myconn.CreateToolDescription(
        tool_name="reptile", poc="squidli", usage="/root/reptile_up")

    toolDescs = myconn.GetToolDescription(["reptile", "goofkit"])
    if len(set(toolDescs)) != 2:
        return False
    for toolDesc in toolDescs:
        if toolDesc.tool_name not in ["reptile", "goofkit"]:
            return False
        if toolDesc.tool_name == "reptile":
            if toolDesc.poc != "squidli":
                return False
    return True


if __name__ == '__main__':
    test_wipe_db()
    print(f"TEST test_build_board():              {test_build_board()}")
    print(f"TEST test_query_team():               {test_query_team()}")
    print(
        f"TEST test_query_multiple_team():      {test_query_multiple_team()}")
    print(
        f"TEST test_query_servicegroup():       {test_query_servicegroup()}")
    print(
        f"TEST test_query_multi_servicegroup(): {test_query_multiple_servicegroup()}")

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
