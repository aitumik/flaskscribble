from flask import render_template
from . import auth
from flask_login import login_user
from ..models import User
from .forms import LoginForm

@auth.route("/",methods=['GET','POST'])
def login():
    return render_template("auth/login.html",form=form)

