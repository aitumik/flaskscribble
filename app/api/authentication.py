from flask import g,jsonify
from flask_httpauth import HTTPBasicAuth

from ..models import User
from . import api
from .errors import forbidden, unauthorized

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email,password):
    if email == "":
        return False
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)

@auth.error_handler
def auth_error():
    return unauthorized("Invalid credentials")

# @api.route('/posts')
# @auth.login_required
# def get_posts():
#     pass

@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
        return forbidden("Unconfirmed account")

@api.route("/")
def index():
    return jsonify({"message":"hello"})
