from flask import Flask, render_template, jsonify, request, url_for
import json

app = Flask(__name__)

values_list = ['id', 'summary', 'host_is_superhost', 'latitude', 'longitude',
               'property_type', 'room_type', 'accomodates', 'bathrooms',
               'bedrooms', 'beds', 'security_deposit', 'cleaning_fee',
               'extra_people', 'minimum_nights', 'cancellation_policy']


def create_json(code, description, dictionary=None):
    temp = {
        "meta": {
            "code": code,
            "description": description
        }
    }

    if dictionary is not None:
        temp['response'] = dictionary

    return temp


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is not None:
        func()


@app.route('/')
def home():
    return "Hello World"
    shutdown_server()


@app.route('/get-predict/<id>', methods=['GET'])
def get_predict(id=None):
    from models import get_listing
    id = id
    if id is None:
        return create_json(202, "No listing_id was passed")
    else:
        try:
            listing = get_listing(id)
        except Exception as e:
            f = open("listing.log", "a")
            f.write("No ID was found with ID: {}".format(id) + "\n")
            f.close()
            return create_json(201, "No listing found with ID: {}".format(id))
        else:
            f = open("listing.log", "a")
            f.write("Listing ID: {} Prediction: {}".format(listing[0],
                                                           listing[1]) + "\n")
            f.close()

            t = {"listing_id": listing[0], "listing_prediction": listing[1]}
            return create_json(200, "Listing Found", t)

    shutdown_server()


@app.route('/predict', methods=['POST'])
def index():
    if not request.is_json:
        return create_json(203, "Format is not a JSON. Check headers.")

    test = request.json
    missing = []

    for value in values_list:
        if value not in test.keys():
            missing.append(value)

    if len(missing) > 0:
        return create_json(204, "Missing values in request",
                           {"values": missing})

    from models import predict
    from keras.models import model_from_json
    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights("model.h5")

    try:
        req_data = request.get_json(force=True)
        id, summary, host, lat, lng, prop_type, room, accom, baths, bedrooms,\
        beds, dep, fee, extra, mini, cancel = \
        req_data['id'], req_data['summary'], req_data['host_is_superhost'], \
        req_data['latitude'], req_data['longitude'], req_data[
            'property_type'], \
        req_data['room_type'], req_data['accomodates'], req_data['bathrooms'], \
        req_data['bedrooms'], req_data['beds'], req_data['security_deposit'], \
        req_data['cleaning_fee'], req_data['extra_people'], req_data[
            'minimum_nights'], req_data['cancellation_policy']
    except Exception as e:
        return create_json(400, e)
    else:
        try:
            result = predict(id, summary, host, lat, lng, prop_type, room,
                             accom, baths, bedrooms, beds, dep, fee, extra,
                             mini, cancel, model)

            req_data['prediction'] = result[1]
            f = open("predict.log", "a")
            f.write(json.dumps(req_data) + "\n")
            f.close()
            t = {"listing_id": result[0], "listing_prediction": result[1]}
            return create_json(200, "Listing Updated", t)
        except Exception as e:
            return "{}".format(e)
    shutdown_server()
