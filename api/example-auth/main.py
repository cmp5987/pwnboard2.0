# main.py

from flask import Blueprint, render_template
from flask_login import current_user, login_required

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


# @app.route('/')
# @app.route('/define_board', methods=['POST'])
# def defineboard(board_config=None):
#     req_json = request.get_json()
#     if board_config == None and req_json is not None:
#         return req_json
#     return "err"
# @app.route('/<callback_type>', methods=['POST'])
# def callback(callback_type):
#     r = redis.Redis(connection_pool=pool)
#     return callback_type
# @app.route('/filter', methods=['GET'])
# def filter():
#     teams_to_query = None
#     if request.args.get('teams') is not None:
#         teams = list(set(request.args.get('teams').split(',')))
#         teams_to_query = str(teams)
#     hosts_to_query = None
#     if request.args.get('hosts') is not None:
#         hosts = list(set(request.args.get('hosts').split(',')))
#         hosts_to_query = str(hosts)
#     oses_to_query = None
#     if request.args.get('oses') is not None:
#         oses = list(set(request.args.get('oses').split(',')))
#         oses_to_query = str(oses)
#     tool_to_query = None
#     if request.args.get('tools') is not None:
#         tools = list(set(request.args.get('tools').split(',')))
#         tools = str(tools)
#     return f"{teams_to_query} && {hosts_to_query}"
