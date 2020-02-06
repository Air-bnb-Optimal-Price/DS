from flask import Flask, render_template, jsonify, request, url_for
import json


app = Flask(__name__)


@app.route('/')
def home():
    return "Hello World"

@app.route('/get-predict/<id>', methods=['GET'])
def get_predict(id=None):
    from models import get_listing
    id = id
    if id is None:
        return {
            "meta":
                {
                    "code": 202,
                    "description": "No listing_id was passed"
                }
        }
    else:
        try:
            listing = get_listing(id)
        except Exception as e:
            f = open("listing.log", "a")
            f.write("No ID was found with ID: {}".format(id) + "\n")
            f.close()
            return {
                "meta": {
                    "code": 201,
                    "description": "No listing found with ID: {}".format(id)
                }
            }
        else:
            f = open("listing.log", "a")
            f.write("Listing ID: {} Prediction: {}".format(listing[0], listing[1]) + "\n")
            f.close()
            return {
                "meta":
                    {
                        "code": 200,
                        "description": "Listing Found"
                    },
                "response": {
                    "listing_id": listing[0],
                    "listing_prediction": listing[1]
                }
            }

@app.route('/predict', methods=['POST'])
def index():
    from models import predict
    from keras.models import model_from_json
    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights("model.h5")

    req_data = request.get_json()
    try:
        result = predict(req_data['id'], req_data['summary'],
                         req_data['host_is_superhost'],
                         req_data['latitude'], req_data['longitude'],
                         req_data['property_type'],
                         req_data['room_type'], req_data['accomodates'],
                         req_data['bathrooms'],
                         req_data['bedrooms'], req_data['beds'],
                         req_data['security_deposit'],
                         req_data['cleaning_fee'], req_data['extra_people'],
                         req_data['minimum_nights'],
                         req_data['cancellation_policy'], model)

        req_data['prediction'] = result[1]
        f = open("predict.log", "a")
        f.write(json.dumps(req_data) + "\n")
        f.close()
        return {
            "meta":
                {
                    "code": 200,
                    "description": "Listing Updated"
                },
            "response": {
                "listing_id": result[0],
                "listing_prediction": result[1]
            }
        }
    except Exception as e:
        return "{}".format(e)
