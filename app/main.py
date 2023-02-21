from flask import Flask, request, jsonify
from threading import Thread

from app.background_tasks import deleter, inserter, updater
from app.read_positions import Read
from app.read_controller import Read_controller
from app.insert_controller import Insert_controller
from app.delete_controller import Delete_controller
from app.update_controller import Update_controller


# Config
app = Flask(__name__)

@app.route("/read_positions", methods=["POST"])
def read_positions():
    
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

@app.route("/insert_positions", methods=["PUT"])
def insert_positions():
    
    if request.method == "PUT":

        body = request.get_json(force=True, silent=False, cache=True)

        controller = Insert_controller()

        flag, errors = controller.run(positions=body)
        if not flag: return jsonify(errors), 422

        thread = Thread(target=inserter, args=(body,))
        thread.daemon = True
        thread.start()

        return "inserting done successfully", 200

@app.route("/update_positions", methods=["PATCH"])
def update_positions():
    
    if request.method == "PATCH":

        body = request.get_json(force=True, silent=False, cache=True)

        controller = Update_controller()

        flag, errors = controller.run(positions=body)
        if not flag: return jsonify(errors), 422

        thread = Thread(target=updater, args=(body,))
        thread.daemon = True
        thread.start()

        return "updating done successfully", 200

@app.route("/delete_positions", methods=["DELETE"])
def delete_positions():
    
    if request.method == "DELETE":

        body = request.get_json(force=True, silent=False, cache=True)

        controller = Delete_controller()

        flag, errors = controller.run(body=body)
        if not flag: return jsonify(errors), 422

        thread = Thread(target=deleter, args=(body,))
        thread.daemon = True
        thread.start()

        return "deleting done successfully", 200

