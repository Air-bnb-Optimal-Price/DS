from flask import Flask, render_template, jsonify, request
from .models import add_update, get_listing


def create_app():
    """Creates the app variables and all the functions to run the API"""
    app = Flask(__name__)

    @app.route('/<listing_id>', methods=['GET'])
    @app.route('/', methods=['POST'])
    def index(listing_id=None):
        if request.method == 'POST':
            req_data = request.get_json()
            try:
                listing_id, listing_name, listing_desc = req_data['listing_id'], \
                                                         req_data['listing_name'], \
                                                         req_data['listing_desc']
                result = add_update(listing_id, listing_name, listing_desc)
                return result
            except Exception as e:
                return f'{e}'
        else:
            listing_id = listing_id
            if listing_id is None:
                return "Get Request Doesn't Have A User ID"
            else:
                try:
                    listing = get_listing(listing_id)
                except Exception as e:
                    return f'{e}'
                else:
                    return f'{listing}'

    return app
