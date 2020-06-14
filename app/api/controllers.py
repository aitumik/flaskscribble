from flask import Blueprint,request,url_for,jsonify

api = Blueprint('api',__name__)

@api.route("/",methods=['GET','POST'])
def api_home():
  return jsonify({"msg":"working api"})


