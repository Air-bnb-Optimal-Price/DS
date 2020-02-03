from flask import Flask, render_template, jsonify, request
from .models import add_update, get_listing


def create_app():
    """Creates the app variables and all the functions to run the API"""
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    @app.route('/<listing_id>', methods=['GET'])
    @app.route('/', methods=['POST'])
    def index(listing_id=None):
        if request.method == 'POST':
            req_data = request.get_json()
            try:
                id, summary, superhost, lat, lng, prop_type, room_type, accom, baths, \
                bedrooms, beds, deposit, cleaning, extra_ppl, min_nights, cancel = req_data['id'], \
                    req_data['summary'], req_data['host_is_superhost'], \
                    req_data['latitude'], req_data['longitude'], req_data['property_type'], \
                    req_data['room_type'], req_data['accomodates'], req_data['bathrooms'], \
                    req_data['bedrooms'], req_data['beds'], req_data['security_deposit'], \
                    req_data['cleaning_fee'], req_data['extra_people'], req_data['minimum_nights'], \
                    req_data['cancellation_policy']

                result = add_update(listing_id, listing_name, listing_desc)
                return result
            except Exception as e:
                return f'{e}'
        else:
            listing_id = listing_id
            if listing_id is None:
                return {
                    "meta":
                            {
                                "code": 202,
                                "description": "No listing_id was passed"
                            }
                        }
            else:
                try:
                    listing = get_listing(listing_id)
                except Exception as e:
                    return {
                            "meta": {
                                "code": 201,
                                "description": f'No listing found with ID: '
                                               f'{listing_id}'
                            }
                        }
                else:
                    return {
                        "meta":
                            {
                                "code": 200,
                                "description": "Listing Found"
                            },
                        "response": {
                            "listing_id": listing_id,
                            "listing_prediction": 254.24
                        }
                    }

    return app
