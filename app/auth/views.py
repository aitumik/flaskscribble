from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from .. import db, login_manager
from ..email import send_email
from ..models import User
from . import auth
from .forms import LoginForm, RegistrationForm


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.home'))
    if current_user.confirm(token):
        flash("You have confirmed you account. Thanks!")
    else:
        flash("The confirmation link is invalid or has expired")
    return redirect(url_for('main.home'))

## We are going to filter uncofirmed accounts

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint[:5] !='auth.':
            return redirect(url_for('auth.unconfirmed'))


@auth.route("/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.home'))
    return render_template("auth/unconfirmed.html")

@auth.route("/confirm")
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    user = current_user
    send_email(user.email,'Confirm your account','auth/email/confirm',user=user,token=token)
    flash("A new confirmation link has been sent to you by email.")
    return redirect(url_for('main.home'))


@auth.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user= User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.home'))
        flash("Invalid username and/or password")
    return render_template("auth/login.html",form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('main.home'))


@auth.route("/register",methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email,'Confirm your account','auth/email/confirm',user=user,token=token)
        flash("A confirmation email has been sent to you by email")
        return redirect(url_for('main.home'))
    return render_template("auth/register.html",form=form)
