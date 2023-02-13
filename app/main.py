
import json
from scipy.stats import beta
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from app.questionnaire_controller import Mifid_controller
from app.questionnaire_main import Questionnaire


# Config
app = Flask(__name__)

@app.route("/questionnaire_interpreter", methods=["POST"])
def questionnaire_interpreter():
    
    if request.method == "POST":

        body = request.get_json(force=True, silent=False, cache=True)

        controller = Mifid_controller()

        response = controller.run(people=body)
        if response[0] == []: return jsonify(response[1]), 422

        interpreter = Questionnaire()
        answer = interpreter.run(response[0])

        return jsonify(answer), 200

@app.route("/", methods=["GET"])
def test():
    
    if request.method == "GET":

        return "app is working", 200
