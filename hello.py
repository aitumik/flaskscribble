##initialization
from flask import Flask,render_template,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_bootstrap import Bootstrap
from flask_script import Manager,Shell
from flask_mail import Mail,Message
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Required
import os
from threading import Thread

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] ='nathankimutai'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(base_dir,'data.sqlite3')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['BLOGGING_MAIL_SUBJECT_PREFIX'] = '[Blogging]'
app.config['BLOGGING_MAIL_SENDER'] = 'Talent Aquisition <hr@bloggin.com'
app.config['BLOGGING_ADMIN'] = os.environ.get('BLOGGING_ADMIN')


db=SQLAlchemy(app)
manager = Manager(app)
mail = Mail(app)
bootstrap = Bootstrap(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)



def send_mail(to,subject,template, **kwargs):
    msg = Message(app.config['BLOGGING_MAIL_SUBJECT_PREFIX']+subject,
            app.config['BLOGGING_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + ".txt",**kwargs)
    msg.html = render_template(template + '.hmtl',**kwargs)
    thread = Thread(target=send_async_mail,args=[app,msg])
    thread.start()
    return thread

def send_async_mail(app,msg):
    with app.app_context():
        mail.send(msg)

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)

manager.add_command('shell',Shell(make_context=make_shell_context))




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
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False 
            if app.config['BLOGGING_ADMIN']:
                send_email(app.config['BLOGGING_ADMIN'],'New user','mail/new_user',user=user)
        else:
            session['known'] = True
        # old_name = session.get('name')
        # if old_name is not None and old_name != form.name.data:
        #     flash("Looks like you have chaged your name")
        session['name'] = form.name.data
        form.name.data = ""
        return redirect(url_for('home'))

    return render_template("index.html",form=form,name=session.get('name'),known=session.get('known',False))


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


