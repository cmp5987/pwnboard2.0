
from flask import Flask, request

import connection

app = Flask(__name__)


# @app.route('/', methods=['GET', 'POST'])
# def helloworld():
#     return "Beep Boop API go away."
#     return "Beep Boop API go away."

@app.route('/define_board', methods=['POST'])
def defineboard(board_config=None):
    req_json = request.get_json()
    if board_config == None and req_json is not None:
        return req_json
    return "err"


@app.route('/<callback_type>', methods=['POST'])
def callback(callback_type):
    r = redis.Redis(connection_pool=pool)

    return callback_type


@app.route('/filter', methods=['GET'])
def filter():
    teams_to_query = None
    if request.args.get('teams') is not None:
        teams = list(set(request.args.get('teams').split(',')))
        teams_to_query = str(teams)

    hosts_to_query = None
    if request.args.get('hosts') is not None:
        hosts = list(set(request.args.get('hosts').split(',')))
        hosts_to_query = str(hosts)

    oses_to_query = None
    if request.args.get('oses') is not None:
        oses = list(set(request.args.get('oses').split(',')))
        oses_to_query = str(oses)

    tool_to_query = None
    if request.args.get('tools') is not None:
        tools = list(set(request.args.get('tools').split(',')))
        tools = str(tools)

    return f"{teams_to_query} && {hosts_to_query}"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
