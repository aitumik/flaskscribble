from flask import jsonify

def forbidden(message):
    response = jsonify({"error":'forbidden',"message":message})
    return response

def unauthorized(message):
    return jsonify({"error":message})
