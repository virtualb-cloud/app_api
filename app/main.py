from flask import Flask, request, jsonify
from read_customers import Read
from read_controller import Read_controller
from insert_customers import Insert
from insert_controller import Insert_controller
from delete_customers import Delete
from delete_controller import Delete_controller
from update_customers import Update
from update_controller import Update_controller


# Config
app = Flask(__name__)

@app.route("/read_customers", methods=["POST"])
def read_customers():
    
    if request.method == "POST":

        body = request.get_json(force=True, silent=False, cache=True)

        controller = Read_controller()

        flag, errors = controller.run(body=body)
        if not flag: return jsonify(errors), 422

        try:
            read = Read()
            answer = read.run(body=body)
        except:
            answer = []
        return jsonify(answer), 200

@app.route("/insert_customers", methods=["PUT"])
def insert_customers():
    
    if request.method == "PUT":

        body = request.get_json(force=True, silent=False, cache=True)

        controller = Insert_controller()

        flag, errors = controller.run(customers=body)
        if not flag: return jsonify(errors), 422

        try:
            insert = Insert()
            answer = insert.run(customers=body)
        except:
            answer = []
        return jsonify(answer), 200

@app.route("/update_customers", methods=["PATCH"])
def update_customers():
    
    if request.method == "PATCH":

        body = request.get_json(force=True, silent=False, cache=True)

        controller = Update_controller()

        flag, errors = controller.run(customers=body)
        if not flag: return jsonify(errors), 422

        try:
            update = Update()
            answer = update.run(customers=body)
        except:
            answer = []
        return jsonify(answer), 200

@app.route("/questionnaire_interpreter", methods=["DELETE"])
def questionnaire_interpreter():
    
    if request.method == "DELETE":

        body = request.get_json(force=True, silent=False, cache=True)

        controller = Delete_controller()

        flag, errors = controller.run(body=body)
        if not flag: return jsonify(errors), 422

        try:
            delete = Delete()
            answer = delete.run(body=body)
        except:
            answer = []
        return jsonify(answer), 200
