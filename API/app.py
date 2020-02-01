from flask import Flask, render_template, jsonify, request
from .users import add_user, User, init_db


def create_app():
    """Creates the app variables and all the functions to run the API"""
    app = Flask(__name__)
    init_db()

    @app.route('/')
    @app.route('/<host_id>', methods=['GET'])
    @app.route('/', methods=['POST'])
    def index(host_id=None):
        if request.method == 'POST':
            req_data = request.get_json()
            try:
                list_id, host_id = req_data['list_id'], req_data['host_id']
                add_user(list_id, host_id)
                return "Successful"
            except Exception as e:
                return f'this? {e}'
        else:
            host_id = host_id
            if host_id is None:
                return "Get Request Doesn't Have A User ID"
            else:
                try:
                    list_id = User.query.filter(User.host_id ==
                                                host_id).first()\
                        .list_id
                except Exception as e:
                    return f'This host doesn\'t exist. {e}'
                else:
                    return f'First listing is {list_id}'

    return app
