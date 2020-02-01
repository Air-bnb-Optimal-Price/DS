from flask import Flask, render_template, jsonify


def create_app():
    """Creates the app variables and all the functions to run the API"""
    app = Flask(__name__)


    @app.route("/")
    def index():
        return render_template("index.html")

    return app