
import json
from scipy.stats import beta
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from modules.questionnaire_controller import Mifid_controller
from modules.questionnaire_main import Questionnaire


# Config
app = Flask(__name__)
app.config['ENV'] = 'development'

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
