from flask import request,jsonify
from . import api

@api.route("/users")
def users():
    data = {}
    return jsonify(data)



