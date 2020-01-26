from flask import render_template,session,redirect,url_for
from flask_login import login_required
from . import main
from .forms import NameForm
from ..import db
from ..models import User,Permission
from ..decorators import admin_required,permission_required


@main.route("/",methods=['GET','POST'])
def home():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False 
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ""
        return redirect(url_for(".home"))
    return render_template("index.html",form=form,name=session.get('name'),known=session.get('known',False))


@main.route("/admin")
@login_required
@admin_required
def for_admins_only():
    return  "For administrators"


