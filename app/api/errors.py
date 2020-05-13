from flask import jsonify
from app.exceptions import ValidationError
from . import api

@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])

def forbidden(message):
    response = jsonify({"error":'forbidden',"message":message})
    return response

def unauthorized(message):
    return jsonify({"error":message})
