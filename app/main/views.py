from flask import render_template,session,redirect,url_for,abort,flash
from flask_login import login_required
from . import main
from flask_login import current_user
from .forms import NameForm,EditProfileForm,PostForm
from ..import db
from ..models import User,Permission,Post
from ..decorators import admin_required,permission_required


@main.route("/",methods=['GET','POST'])
def home():
    form = PostForm()
    if form.validate_on_submit() and current_user.can(Permission.WRITE_ARTICLES):
        post = Post(body = form.post.data,author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for(".home"))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("index.html",form=form,posts=posts,form=form)

@main.route("/edit-profile",methods=["GET","POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location= form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash("Your profile has been updated")
        return redirect(url_for("main.user",username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template("edit_profile.html",form=form)


### Admin edit form 
@main.route("/edit-profile/<int:id>",methods=['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.useraname.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash("The profile has been updated")
        return redirect(url_for('main.user',username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template("edit_profile.html",form=form,user=user)



@main.route("/user/<username>")
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("The username does not exist")
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template("user.html",user=user,posts = posts)



@main.route("/admin")
@login_required
@admin_required
def for_admins_only():
    return  "For administrators"


