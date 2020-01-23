##initialization
from flask import Flask,render_template,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Required
import os

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] ='nathankimutai'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(base_dir,'data.sqlite3')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db=SQLAlchemy(app)
manager = Manager(app)
bootstrap = Bootstrap(app)



####### Model #######
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer,primary_key =True)
    name = db.Column(db.String(66),unique=True)
    users = db.relationship('User',backref='roles')

    def __repr__(self):
        return "<Role %r>" % self.name

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return "<User %r>" % self.username


class NameForm(FlaskForm):
    name = StringField("What is your name?",validators=[Required()])
    submit = SubmitField('Submit')


@app.route("/",methods=['GET','POST'])
def home():
    # browser = request.headers.get("User_Agent")
    # print(browser)
    # return "<h1>Your browser is {}</h1>".format(browser)

    # response = make_response("<h1>This doc contains cookie</h1>")
    # response.set_cookie("answ",'42')

    name = None
    form = NameForm()
    
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash("Looks like you have chaged your name")
        session['name'] = form.name.data
        return redirect(url_for('home'))

    return render_template("index.html",form=form,name=session.get('name'))


@app.route("/user/<name>")
def user(name):
    return render_template("user.html",name=name)


#Lets us define custom error pages
@app.errorhandler(404)
def page_not_found(err):
    return render_template("404.html"),404


@app.errorhandler(500)
def internal_server(err):
    return render_template("505.html"),500

if __name__ == "__main__":
    manager.run()


