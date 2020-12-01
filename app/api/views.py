from flask import request,jsonify
from . import api
from ..decorators import admin_required


@api.route("/users")
@admin_required
def users():
    data = {}
    return jsonify(data)



